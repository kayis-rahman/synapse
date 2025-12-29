"""
RAG API - FastAPI endpoint for RAG-augmented chat completions.

Provides OpenAI-compatible API endpoints with RAG augmentation.
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.orchestrator import get_orchestrator, RAGOrchestrator
from rag.retriever import get_retriever
from rag.model_manager import get_model_manager
from rag.memory_store import MemoryStore, MemoryFact, get_memory_store
from rag.memory_writer import MemoryWriter, extract_and_store
from rag.memory_reader import MemoryReader, get_memory_reader, inject_memory_context


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
# Memory Models
# ============================================================================

class MemoryFactCreate(BaseModel):
    scope: str = Field(default="session")
    category: str
    key: str
    value: Any
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    source: str = Field(default="user")


class MemoryFactUpdate(BaseModel):
    id: str
    scope: Optional[str] = None
    category: Optional[str] = None
    key: Optional[str] = None
    value: Optional[Any] = None
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    source: Optional[str] = None


class MemoryFactResponse(BaseModel):
    id: str
    scope: str
    category: str
    key: str
    value: Any
    confidence: float
    source: str
    created_at: str
    updated_at: str


class MemoryQueryRequest(BaseModel):
    scope: Optional[str] = None
    category: Optional[str] = None
    key: Optional[str] = None
    min_confidence: float = Field(default=0.7, ge=0.0, le=1.0)
    limit: Optional[int] = Field(default=None, ge=1, le=100)


class MemoryExtractRequest(BaseModel):
    interaction: Dict[str, str]
    scope: Optional[str] = Field(default="session")
    store: bool = Field(default=True, description="Automatically store extracted facts")


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
# Memory Endpoints
# ============================================================================

@app.post("/v1/memory", response_model=MemoryFactResponse)
async def create_memory(fact_data: MemoryFactCreate):
    """
    Create a new memory fact.
    """
    try:
        store = get_memory_store()

        fact = MemoryFact(
            scope=fact_data.scope,
            category=fact_data.category,
            key=fact_data.key,
            value=fact_data.value,
            confidence=fact_data.confidence,
            source=fact_data.source
        )

        stored_fact = store.store_memory(fact)
        if not stored_fact:
            raise HTTPException(status_code=500, detail="Failed to store memory fact")

        return MemoryFactResponse(
            id=stored_fact.id,
            scope=stored_fact.scope,
            category=stored_fact.category,
            key=stored_fact.key,
            value=stored_fact.to_dict()["value"],
            confidence=stored_fact.confidence,
            source=stored_fact.source,
            created_at=stored_fact.created_at,
            updated_at=stored_fact.updated_at
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/v1/memory", response_model=List[MemoryFactResponse])
async def query_memory(
    scope: Optional[str] = None,
    category: Optional[str] = None,
    key: Optional[str] = None,
    min_confidence: float = 0.7,
    limit: Optional[int] = None
):
    """
    Query memory facts with optional filters.
    """
    try:
        reader = get_memory_reader()

        facts = reader.query_memory(
            scope=scope,
            category=category,
            key=key,
            min_confidence=min_confidence,
            limit=limit
        )

        return [
            MemoryFactResponse(
                id=f.id,
                scope=f.scope,
                category=f.category,
                key=f.key,
                value=f.to_dict()["value"],
                confidence=f.confidence,
                source=f.source,
                created_at=f.created_at,
                updated_at=f.updated_at
            )
            for f in facts
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/memory/{fact_id}", response_model=MemoryFactResponse)
async def get_memory(fact_id: str):
    """
    Retrieve a specific memory fact by ID.
    """
    try:
        store = get_memory_store()
        fact = store.get_memory(fact_id)

        if not fact:
            raise HTTPException(status_code=404, detail="Memory fact not found")

        return MemoryFactResponse(
            id=fact.id,
            scope=fact.scope,
            category=fact.category,
            key=fact.key,
            value=fact.to_dict()["value"],
            confidence=fact.confidence,
            source=fact.source,
            created_at=fact.created_at,
            updated_at=fact.updated_at
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/v1/memory/{fact_id}", response_model=MemoryFactResponse)
async def update_memory(fact_id: str, update_data: MemoryFactUpdate):
    """
    Update an existing memory fact.
    """
    try:
        store = get_memory_store()

        # Get existing fact
        existing = store.get_memory(fact_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Memory fact not found")

        # Update with provided fields
        updated_fact = MemoryFact(
            id=fact_id,
            scope=update_data.scope if update_data.scope else existing.scope,
            category=update_data.category if update_data.category else existing.category,
            key=update_data.key if update_data.key else existing.key,
            value=update_data.value if update_data.value is not None else existing.to_dict()["value"],
            confidence=update_data.confidence if update_data.confidence is not None else existing.confidence,
            source=update_data.source if update_data.source else existing.source,
            created_at=existing.created_at,
            updated_at=existing.updated_at
        )

        result = store.update_memory(updated_fact)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to update memory fact")

        return MemoryFactResponse(
            id=result.id,
            scope=result.scope,
            category=result.category,
            key=result.key,
            value=result.to_dict()["value"],
            confidence=result.confidence,
            source=result.source,
            created_at=result.created_at,
            updated_at=result.updated_at
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.delete("/v1/memory/{fact_id}")
async def delete_memory(fact_id: str):
    """
    Delete a memory fact.
    """
    try:
        store = get_memory_store()
        deleted = store.delete_memory(fact_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Memory fact not found")

        return {"status": "deleted", "fact_id": fact_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/memory/extract")
async def extract_memory(request: MemoryExtractRequest):
    """
    Extract memory facts from an interaction.

    If store=True, automatically stores extracted facts.
    """
    try:
        writer = MemoryWriter()
        store = get_memory_store()

        # Extract facts
        facts = writer.extract_memory(request.interaction, scope=request.scope)

        # Store if requested
        stored_facts = []
        if request.store:
            for fact in facts:
                try:
                    stored = store.store_memory(fact)
                    if stored:
                        stored_facts.append(stored.to_dict())
                except Exception as e:
                    print(f"Error storing fact: {e}")

        return {
            "extracted_count": len(facts),
            "stored_count": len(stored_facts),
            "facts": [f.to_dict() for f in facts]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/memory/inject")
async def inject_memory(query_request: Dict[str, Any]):
    """
    Inject memory context into a user query.
    """
    try:
        user_query = query_request.get("query", "")
        scope = query_request.get("scope", "session")
        min_confidence = query_request.get("min_confidence", 0.7)
        max_facts = query_request.get("max_facts", 10)

        # Inject memory context
        augmented = inject_memory_context(
            user_query,
            scope=scope,
            min_confidence=min_confidence,
            max_facts=max_facts
        )

        return {
            "original_query": user_query,
            "augmented_query": augmented
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/memory/stats")
async def get_memory_stats():
    """
    Get memory subsystem statistics.
    """
    try:
        store = get_memory_store()
        stats = store.get_stats()
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/memory/scopes")
async def list_memory_scopes():
    """
    List all available scopes.
    """
    return {
        "scopes": list(MemoryStore.VALID_SCOPES),
        "categories": list(MemoryStore.VALID_CATEGORIES),
        "sources": list(MemoryStore.VALID_SOURCES)
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.environ.get("RAG_HOST", "0.0.0.0")
    port = int(os.environ.get("RAG_PORT", "8001"))
    
    uvicorn.run(app, host=host, port=port)
