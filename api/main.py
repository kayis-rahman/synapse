# ============================================================================
# RAG API - FastAPI endpoint for RAG-augmented chat completions.
#
# Provides OpenAI-compatible API endpoints with RAG augmentation.
#
# Changes:
# - Added multipart file upload endpoint
# - Updated ingest request/response models to support file paths
# - Two-step workflow: Upload (HTTP) + Ingest (MCP tool)
# ============================================================================

import os
import sys
import json
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


# ============================================================================
# Pydantic Models
# ============================================================================

class IngestRequest(BaseModel):
    """Ingestion request with support for file path or text."""
    text: str = Field(default="", description="Text content to ingest (for backward compatibility)")
    file_path: Optional[str] = None  # New field for file path ingestion
    source_name: str = "api"
    chunk_size: int = Field(default=500, ge=100, le=2000)
    chunk_overlap: int = Field(default=50, ge=0, le=500)
    metadata: Optional[Dict[str, Any]] = None


class IngestResponse(BaseModel):
    """Ingestion response with source path support."""
    status: str
    chunks_created: int
    source: str  # Will be file_path if file ingestion


class UploadFileResponse(BaseModel):
    """Response model for file upload endpoint."""
    status: str
    file_path: str
    original_filename: str
    message: str


# ============================================================================
# Add parent directory to path for imports
# ============================================================================

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.orchestrator import get_orchestrator, RAGOrchestrator
from rag.retriever import get_retriever
from rag.model_manager import get_model_manager
from rag.memory_store import MemoryStore, MemoryFact, get_memory_store
from rag.memory_writer import MemoryWriter, extract_and_store
from rag.memory_reader import MemoryReader, get_memory_reader, inject_memory_context


# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="pi-rag API",
    description="RAG-augmented chat completions using llama-cpp-python",
    version="1.0.0",
)


# ============================================================================
# Ingestion Endpoints
# ============================================================================

@app.post("/v1/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload file to temp directory for later ingestion.

    Returns file path for MCP ingestion.
    """
    import shutil
    import uuid
    import logging

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Read config for upload directory
    config_path = os.environ.get("RAG_CONFIG_PATH", "./configs/rag_config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)

    upload_dir = config.get("remote_upload_directory", "/tmp/rag-uploads")
    max_size_bytes = config.get("remote_upload_max_file_size_mb", 50) * 1024 * 1024

    # Validate file size
    file_size = 0
    await file.seek(0, 2)
    chunk = await file.read(1024 * 1024)
    while chunk:
        file_size += len(chunk)
        chunk = await file.read(1024 * 1024)

    logger.info(f"Received file: {file.filename}, size: {file_size / (1024*1024):.2f} MB")

    # Check file size
    if file_size > max_size_bytes:
        logger.warning(f"File too large: {file_size / (1024*1024):.2f} MB > {max_size_bytes / (1024*1024):.2f} MB")
        raise HTTPException(
            status_code=413,
            detail=f"File too large (max {max_size_bytes / (1024*1024):.2f} MB)"
        )

    # Generate unique filename to avoid conflicts
    unique_filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    target_path = os.path.join(upload_dir, unique_filename)

    # Save file
    with open(target_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    logger.info(f"File uploaded: {target_path}")

    return UploadFileResponse(
        status="success",
        file_path=target_path,
        original_filename=file.filename,
        message="File uploaded successfully"
    )

    except Exception as e:
        logger.error(f"Upload failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/ingest")
async def ingest(request: IngestRequest):
    """
    Ingest text or file path into RAG index.
    """
    try:
        from rag.ingest import ingest_file, ingest_text

        if request.file_path:
            # Ingest from file path (uploaded file)
            count = ingest_file(
                file_path=request.file_path,
                chunk_size=request.chunk_size,
                chunk_overlap=request.chunk_overlap,
                metadata=request.metadata
            )
            source = request.file_path
        elif request.text:
            # Ingest from text (existing behavior)
            count = ingest_text(
                text=request.text,
                source_name=request.source_name,
                chunk_size=request.chunk_size,
                chunk_overlap=request.chunk_overlap,
                metadata=request.metadata
            )
            source = request.source_name
        else:
            raise HTTPException(
                status_code=400,
                detail="Either 'text' or 'file_path' must be provided"
            )

        return {
            "status": "success",
            "chunks_created": count,
            "source": source
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Existing Endpoints (Unchanged)
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


@app.post("/v1/chat/completions", response_model=None)
async def chat_completions(request):
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


# ============================================================================
# Memory Endpoints (Unchanged)
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
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/memory", response_model=List[MemoryFactResponse])
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
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


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
            source=f.source,
            created_at=fact.created_at,
            updated_at=f.updated_at
        )

    except HTTPException:
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

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise HTTPException(status_code=500, detail=str(e))


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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/memory/extract")
async def extract_memory(request: MemoryExtractRequest):
    """
    Extract memory facts from an interaction.
    """
    try:
        writer = MemoryWriter()
        store = get_memory_store()

        # Extract facts
        facts = writer.extract_memory(request.interaction, scope=request.scope)
        store_facts = []
        if request.store:
            for fact in facts:
                try:
                    stored = store.store_memory(fact)
                    if stored:
                        store_facts.append(stored.to_dict())
                except Exception as e:
                    print(f"Error storing fact: {e}")

        return {
            "extracted_count": len(facts),
            "stored_count": len(store_facts),
            "facts": [f.to_dict() for f in facts]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


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
# Model Management Endpoints (Unchanged)
# ============================================================================

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
    try:
        manager = app.state.model_manager
        if manager.unload_model(model_name):
            return {"status": "unloaded", "model": model_name}
        else:
            return {"status": "not_loaded", "model": model_name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/stats")
async def get_stats():
    """
    Get system statistics.
    """
    try:
        orchestrator = app.state.orchestrator
        retriever = app.state.retriever
        models = app.state.model_manager

        return {
            "orchestrator": orchestrator.get_stats(),
            "retriever": retriever.get_stats(),
            "models": models.get_stats()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/v1/index")
async def clear_index():
    """
    Clear RAG index.
    """
    try:
        app.state.retriever.clear_index()
        return {"status": "cleared"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("RAG_HOST", "0.0.0.0")
    port = int(os.environ.get("RAG_PORT", "8001"))

    uvicorn.run(app, host=host, port=port)
