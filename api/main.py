"""
RAG API - FastAPI endpoint for RAG-augmented chat completions.

Provides OpenAI-compatible API endpoints with RAG augmentation.
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.orchestrator import get_orchestrator, RAGOrchestrator
from rag.retriever import get_retriever
from rag.model_manager import get_model_manager


# ============================================================================
# Pydantic Models
# ============================================================================

class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = Field(default="chat")
    messages: List[Message]
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=2048, ge=1, le=32768)
    stream: Optional[bool] = Field(default=False)
    use_rag: Optional[bool] = Field(default=None, description="Override RAG usage")
    metadata_filters: Optional[Dict[str, Any]] = Field(default=None)


class ChatCompletionChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    model: str
    choices: List[ChatCompletionChoice]
    rag_used: bool = False
    sources: List[Dict[str, Any]] = []


class IngestRequest(BaseModel):
    text: str
    source_name: str = "api"
    chunk_size: int = Field(default=500, ge=100, le=2000)
    chunk_overlap: int = Field(default=50, ge=0, le=500)
    metadata: Optional[Dict[str, Any]] = None


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=3, ge=1, le=20)
    metadata_filters: Optional[Dict[str, Any]] = None


class ModelInfo(BaseModel):
    name: str
    path: str
    type: str
    loaded: bool


# ============================================================================
# Application Lifecycle
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle handler."""
    print("Starting RAG API...")
    
    # Load config
    config_path = os.environ.get("RAG_CONFIG", "./configs/rag_config.json")
    
    # Initialize orchestrator (lazy loads models)
    app.state.orchestrator = get_orchestrator(config_path)
    app.state.retriever = get_retriever(config_path)
    app.state.model_manager = get_model_manager()
    
    print("RAG API ready")
    
    yield
    
    # Cleanup
    print("Shutting down RAG API...")
    app.state.model_manager.unload_all()
    print("Models unloaded")


# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="pi-rag API",
    description="RAG-augmented chat completions using llama-cpp-python",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "pi-rag"}


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "models_loaded": app.state.model_manager.get_loaded_models(),
        "index_stats": app.state.retriever.vector_store.get_stats()
    }


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible chat completions with RAG augmentation.
    """
    try:
        orchestrator: RAGOrchestrator = app.state.orchestrator
        
        # Convert messages to dict format
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        # Handle streaming
        if request.stream:
            async def generate():
                for chunk in orchestrator.chat_stream(
                    messages=messages,
                    model_name=request.model,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                    use_rag=request.use_rag,
                    metadata_filters=request.metadata_filters
                ):
                    data = {
                        "id": "chatcmpl-stream",
                        "object": "chat.completion.chunk",
                        "model": request.model,
                        "choices": [{
                            "index": 0,
                            "delta": {"content": chunk},
                            "finish_reason": None
                        }]
                    }
                    yield f"data: {json.dumps(data)}\n\n"
                
                # Final chunk
                yield f"data: {json.dumps({'choices': [{'finish_reason': 'stop'}]})}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream"
            )
        
        # Non-streaming response
        result = orchestrator.chat(
            messages=messages,
            model_name=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            use_rag=request.use_rag,
            metadata_filters=request.metadata_filters
        )
        
        return ChatCompletionResponse(
            id="chatcmpl-" + os.urandom(8).hex(),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(role="assistant", content=result["content"]),
                    finish_reason="stop"
                )
            ],
            rag_used=result["rag_used"],
            sources=result["sources"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/v1/search")
async def search(request: SearchRequest):
    """
    Search the RAG index directly.
    """
    try:
        retriever = app.state.retriever
        results = retriever.search(
            query=request.query,
            top_k=request.top_k,
            metadata_filters=request.metadata_filters
        )
        
        return {
            "query": request.query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/ingest")
async def ingest(request: IngestRequest):
    """
    Ingest text into the RAG index.
    """
    try:
        from rag.ingest import ingest_text
        
        count = ingest_text(
            text=request.text,
            source_name=request.source_name,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
            metadata=request.metadata
        )
        
        return {
            "status": "success",
            "chunks_created": count,
            "source": request.source_name
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/models")
async def list_models():
    """
    List available models.
    """
    manager = app.state.model_manager
    stats = manager.get_stats()
    
    models = []
    for name in stats["registered_models"]:
        info = manager.get_model_info(name)
        if info:
            models.append(ModelInfo(
                name=info["name"],
                path=info["path"],
                type=info["type"],
                loaded=info["loaded"]
            ))
    
    return {"models": models}


@app.post("/v1/models/{model_name}/load")
async def load_model(model_name: str):
    """
    Load a model into memory.
    """
    try:
        manager = app.state.model_manager
        manager.load_model(model_name)
        return {"status": "loaded", "model": model_name}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/models/{model_name}/unload")
async def unload_model(model_name: str):
    """
    Unload a model from memory.
    """
    manager = app.state.model_manager
    if manager.unload_model(model_name):
        return {"status": "unloaded", "model": model_name}
    else:
        return {"status": "not_loaded", "model": model_name}


@app.get("/v1/stats")
async def get_stats():
    """
    Get system statistics.
    """
    return {
        "orchestrator": app.state.orchestrator.get_stats(),
        "retriever": app.state.retriever.get_stats(),
        "models": app.state.model_manager.get_stats()
    }


@app.delete("/v1/index")
async def clear_index():
    """
    Clear the RAG index.
    """
    app.state.retriever.clear_index()
    return {"status": "cleared"}


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.environ.get("RAG_HOST", "0.0.0.0")
    port = int(os.environ.get("RAG_PORT", "8001"))
    
    uvicorn.run(app, host=host, port=port)
