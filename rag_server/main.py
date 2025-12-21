import os
import json
import logging
from typing import List, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from rag.embedding import EmbeddingService
from rag.vectorstore import VectorStore
from rag.retriever import Retriever
from rag.llm import LLMController
from rag.orchestrator import RagOrchestrator

logging.basicConfig(filename='rag_server.log', level=logging.DEBUG)

app = FastAPI()

# Lazy initialization to avoid heavy startup if not used
_embedding = None
_store = None
_retriever = None
_llm = None
_orchestrator = None


def ensure_components():
    global _embedding, _store, _retriever, _llm, _orchestrator
    if _embedding is not None:
        return
    index_path = os.environ.get("RAG_INDEX_PATH", "./rag_index")
    os.makedirs(index_path, exist_ok=True)
    _embedding = EmbeddingService()
    _store = VectorStore(index_path=index_path)
    _retriever = Retriever(_embedding, _store, top_k=int(os.environ.get("RAG_TOP_K", "5")))
    _llm = LLMController()
    _orchestrator = RagOrchestrator(_embedding, _store, _retriever, _llm, top_k=int(os.environ.get("RAG_TOP_K", "5")))


class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = None
    context: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    score: float
    context: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]


class CompletionChoice(BaseModel):
    text: str
    index: int
    logprobs: Optional[dict] = None
    finish_reason: str


class CompletionResponse(BaseModel):
    id: str
    object: str = "text_completion"
    created: int
    model: str
    choices: List[CompletionChoice]


class CompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.7


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str = "rag"


class ModelsResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/v1/models")
def list_models():
    logging.info("Models endpoint called")
    import time
    return ModelsResponse(
        data=[
            ModelInfo(
                id="mistralai/devstral-2512:free",
                created=int(time.time()),
                owned_by="rag"
            )
        ]
    )


@app.post("/v1/chat/completions")
def chat_completions(request: Request, req: ChatCompletionRequest):
    try:
        logging.info("Chat completions called with model: " + req.model + ", stream: " + str(getattr(req, 'stream', False)))
        ensure_components()
        logging.info("Components ensured")
        global _orchestrator
        if _orchestrator is None:
            return {"error": "server not initialized"}
        # Extract the last user message as the query
        user_messages = [msg for msg in req.messages if msg.role == "user"]
        if not user_messages:
            return {"error": "no user message"}
        query = user_messages[-1].content
        logging.info("Query: " + query)
        result = _orchestrator.answer(query, model=req.model, temperature=req.temperature or 0.7)
        logging.info("Result: " + str(result))
        answer = result.get("answer", "") if isinstance(result, dict) else str(result)
        if answer.startswith("LLM generation failed"):
            return {"error": answer}
        import time
        if req.stream:
            import json
            def generate():
                yield "data: " + json.dumps({
                    "id": f"rag-{hash(query)}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": req.model,
                    "choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}, "finish_reason": None}]
                }) + "\n\n"
                yield "data: " + json.dumps({
                    "id": f"rag-{hash(query)}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": req.model,
                    "choices": [{"index": 0, "delta": {"content": answer}, "finish_reason": None}]
                }) + "\n\n"
                yield "data: " + json.dumps({
                    "id": f"rag-{hash(query)}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": req.model,
                    "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]
                }) + "\n\n"
                yield "data: [DONE]\n\n"
            return StreamingResponse(generate(), media_type="text/plain")
        else:
            return {
                "id": "rag-" + str(hash(query)),
                "object": "chat.completion",
                "created": int(time.time()),
                "model": req.model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": answer
                        },
                        "finish_reason": "stop"
                    }
                ]
            }
    except Exception as e:
        logging.error("Error in chat_completions: " + str(e))
        return {"error": str(e)}


@app.post("/v1/completions")
def completions(request: Request, req: CompletionRequest):
    ensure_components()
    global _orchestrator
    if _orchestrator is None:
        return {"error": "server not initialized"}
    query = req.prompt
    result = _orchestrator.answer(query, model=req.model, temperature=req.temperature or 0.7)
    answer = result.get("answer", "") if isinstance(result, dict) else str(result)
    if answer.startswith("LLM generation failed"):
        return {"error": answer}
    import time
    return {
        "id": "rag-" + str(hash(query)),
        "object": "text_completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "text": answer,
                "index": 0,
                "finish_reason": "stop"
            }
        ]
    }


# Run instructions (for developers): uvicorn rag_server.main:app --reload --port 8000
