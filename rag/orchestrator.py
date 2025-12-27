"""
RAG Orchestrator - Coordinates retrieval and LLM generation using llama-cpp-python.

Features:
- Automatic context injection from retrieved documents
- Support for disabling RAG via system message keyword
- Multi-model support (separate embedding and chat models)
- Streaming and non-streaming responses
"""

import json
import os
from typing import List, Dict, Any, Optional, Generator

class RAGOrchestrator:
    """
    Orchestrates RAG pipeline: retrieval + LLM generation.
    
    Usage:
        orchestrator = RAGOrchestrator(config_path="./configs/rag_config.json")
        response = orchestrator.chat(
            messages=[{"role": "user", "content": "How does auth work?"}]
        )
    """
    
    def __init__(self, config_path: str = "./configs/rag_config.json"):
        self.config_path = config_path
        self._load_config()
        
        # Initialize components
        from .model_manager import get_model_manager, ModelConfig
        from .retriever import get_retriever
        
        try:
            self._manager = get_model_manager()  
            self._retriever = get_retriever(config_path)
            
            # Register chat model if configured and it's a local model
            if self.chat_model_path and self.chat_model_name in self._manager._registry:
                config = self._manager._registry[self.chat_model_name]
                if not config.is_external:
                    self._register_chat_model()
                
        except Exception as e:
            print(f"Warning: Failed to initialize orchestrator dependencies: {e}")
    
    def _load_config(self) -> None:
        """Load configuration."""
        # Defaults
        self.rag_enabled = True
        self.top_k = 3
        self.disable_keyword = "disable-rag"
        self.chat_model_path = ""
        self.chat_model_name = "chat"
        self.n_ctx = 32768
        self.n_gpu_layers = -1
        self.temperature = 0.7
        self.max_tokens = 2048
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    
                self.rag_enabled = config.get("rag_enabled", True)
                self.top_k = config.get("top_k", 3)
                self.disable_keyword = config.get("rag_disable_keyword", "disable-rag")
                self.chat_model_path = config.get("chat_model_path", "")
                self.chat_model_name = config.get("chat_model_name", "chat")
                self.n_ctx = config.get("chat_n_ctx", 32768)
                self.n_gpu_layers = config.get("chat_n_gpu_layers", -1)
                self.temperature = config.get("temperature", 0.7)
                self.max_tokens = config.get("max_tokens", 2048)
        except Exception as e:
            print(f"Warning: Failed to load orchestrator config: {e}")
    
    def _register_chat_model(self) -> None:
        """Register chat model with model manager."""
        if not self.chat_model_path or not os.path.exists(self.chat_model_path):
            return
            
        from .model_manager import ModelConfig

        config = ModelConfig(
            path=self.chat_model_path,
            model_type="chat",
            n_ctx=self.n_ctx,
            n_gpu_layers=self.n_gpu_layers,
            embedding=False,
            verbose=False
        )
        self._manager.register_model(self.chat_model_name, config)
    
    def set_chat_model(self, model_path: str, model_name: str = "chat") -> None:
        """
        Set the chat model to use.
        
        Args:
            model_path: Path to GGUF model file
            model_name: Name identifier for the model
        """
        self.chat_model_path = model_path
        self.chat_model_name = model_name
        
        if os.path.exists(model_path):
            self._register_chat_model()
        else:
            raise FileNotFoundError(f"Model file not found: {model_path}")
    
    def _should_use_rag(self, messages: List[Dict[str, str]]) -> bool:
        """Check if RAG should be used based on messages."""
        if not self.rag_enabled:
            return False
        
        # Check system message for disable keyword
        for msg in messages:
            if msg.get("role") == "system":
                content = msg.get("content", "").lower()
                if self.disable_keyword.lower() in content:
                    return False
        
        return True
    
    def _extract_query(self, messages: List[Dict[str, str]]) -> str:
        """Extract the query from messages (last user message)."""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                return msg.get("content", "")
        return ""
    
    def _inject_context(
        self,
        messages: List[Dict[str, str]],
        context: str
    ) -> List[Dict[str, str]]:
        """Inject retrieved context into messages."""
        if not context:
            return messages
        
        # Create augmented messages
        augmented = []
        
        # Add or augment system message with context
        has_system = any(m.get("role") == "system" for m in messages)
        
        if has_system:
            for msg in messages:
                if msg.get("role") == "system":
                    augmented.append({
                        "role": "system",
                        "content": f"{msg['content']}\n\n---\nRelevant Context:\n{context}"
                    })
                else:
                    augmented.append(msg)
        else:
            # Add new system message with context
            augmented.append({
                "role": "system",
                "content": f"Use the following context to help answer questions:\n\n{context}"
            })
            augmented.extend(messages)
        
        return augmented

    def chat(
        self,
        messages: List[Dict[str, str]],
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_rag: Optional[bool] = None,
        metadata_filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a chat response with optional RAG augmentation.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            use_rag: Override RAG usage (None = auto-detect)
            metadata_filters: Filters for document retrieval
            
        Returns:
            Response dict with 'content', 'rag_context', 'sources'
        """
        # Use specified model or default
        model_to_use = model_name or self.chat_model_name

        # Check if the model is registered
        if model_to_use not in self._manager._registry:
            raise ValueError(
                f"Model '{model_to_use}' not registered. "
                "Configure in models_config.json or register with model manager."
            )
        
        # Determine if RAG should be used
        should_rag = use_rag if use_rag is not None else self._should_use_rag(messages)
        
        # Retrieve context if RAG is enabled
        context = ""
        sources = []
        
        if should_rag:
            query = self._extract_query(messages)
            if query:
                context, sources = self._retriever.search_with_context(
                    query,
                    top_k=self.top_k,
                    metadata_filters=metadata_filters
                )
        
        # Inject context into messages
        augmented_messages = self._inject_context(messages, context) if context else messages
        
        # Generate response
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        try:
            response = self._manager.chat_completion(
                model_to_use,
                augmented_messages,
                temperature=temp,
                max_tokens=tokens
            )
            
            # Extract content from response  
            content = ""
            if response and isinstance(response, dict):
                choices = response.get("choices", [])
                if choices:
                    choice = choices[0]
                    if "message" in choice:
                        content = choice["message"].get("content", "")
                    elif "text" in choice:
                        content = choice["text"]
            
            return {
                "content": content,
                "rag_used": should_rag and bool(context),
                "rag_context": context,
                "sources": sources,
                "model": model_to_use,
                "raw_response": response
            }
        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                "content": f"Error: {str(e)}",
                "rag_used": False,
                "rag_context": "",
                "sources": [],
                "model": model_to_use,
                "raw_response": None
            }

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_rag: Optional[bool] = None,
        metadata_filters: Optional[Dict[str, Any]] = None
    ) -> Generator[str, None, None]:
        """
        Generate a streaming chat response.
        
        Yields:
            Content tokens as they are generated
        """
        if not self.chat_model_path:
            raise ValueError("Chat model not configured.")
        
        # Use specified model or default
        model_to_use = model_name or self.chat_model_name

        # Check if the model is registered
        if model_to_use not in self._manager._registry:
            raise ValueError(f"Model '{model_to_use}' not registered.")

        # Determine if RAG should be used
        should_rag = use_rag if use_rag is not None else self._should_use_rag(messages)

        # Retrieve context if RAG is enabled
        context = ""

        if should_rag:
            query = self._extract_query(messages)
            if query:
                context, _ = self._retriever.search_with_context(
                    query,
                    top_k=self.top_k,
                    metadata_filters=metadata_filters
                )

        # Inject context into messages
        augmented_messages = self._inject_context(messages, context) if context else messages

        # Get model and stream
        try:
            model = self._manager.get_model(model_to_use)
            
            temp = temperature if temperature is not None else self.temperature
            tokens = max_tokens if max_tokens is not None else self.max_tokens
            
            for chunk in model.create_chat_completion(
                messages=augmented_messages,
                temperature=temp,
                max_tokens=tokens,
                stream=True
            ):
                if "choices" in chunk and len(chunk["choices"]) > 0:
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield content
                        
        except Exception as e:
            print(f"Stream error: {e}")

    def preload_models(self) -> None:
        """Preload both chat and embedding models."""
        if self.chat_model_path:
            self._manager.load_model(self.chat_model_name)
        # For now we don't have access to the retriever's embedded service directly

    def unload_models(self) -> None:
        """Unload all models to free memory."""
        self._manager.unload_all()

    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        return {
            "rag_enabled": self.rag_enabled,
            "chat_model": self.chat_model_name,
            "model_manager": str(type(self._manager)) 
        }

# Singleton instance
_orchestrator: Optional[RAGOrchestrator] = None


def get_orchestrator(config_path: str = "./configs/rag_config.json") -> RAGOrchestrator:
    """Get or create the orchestrator singleton."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = RAGOrchestrator(config_path)
    return _orchestrator
