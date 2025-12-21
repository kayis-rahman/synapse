from typing import List


class RagOrchestrator:
    def __init__(self, embedding_service, vector_store, retriever, llm_controller, top_k: int = 5):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.retriever = retriever
        self.llm_controller = llm_controller
        self.top_k = top_k

    def answer(self, messages, model=None, temperature=0.7, api_key=None) -> dict:
        # Convert messages to dicts if needed
        if messages and hasattr(messages[0], 'role'):
            messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        # Extract the last user message for retrieval
        user_messages = [msg for msg in messages if msg["role"] == "user"]
        if not user_messages:
            return {"answer": "No user message found.", "sources": [], "score": 0.0, "context": ""}
        query = user_messages[-1]["content"]

        # Step 1: Check logs (retrieve log-related entries)
        log_results = self.retriever.retrieve([query], metadata_filters={"type": "log"}) if self.retriever else []
        log_context = "\n".join([d for d, _s, _md in log_results]) if log_results else "No relevant logs found."

        # Step 2: Match features (extract entities, retrieve)
        entities = self._extract_entities(query)
        feature_filters = {k: v for k, v in entities.items() if k in ["project", "service", "feature", "device"]}
        feature_results = self.retriever.retrieve([query], metadata_filters=feature_filters) if self.retriever else []
        feature_context = "\n".join([d for d, _s, _md in feature_results]) if feature_results else "No matching features found."

        # Combine contexts
        full_context = f"Logs:\n{log_context}\n\nFeatures:\n{feature_context}"

        # Step 3: Orchestrate LLM prompt - prepend context to messages
        context_message = {"role": "system", "content": f"Based on the following context:\n{full_context}\n\nAnswer the user's questions."}
        augmented_messages = [context_message] + messages
        answer = self.llm_controller.generate(augmented_messages, model=model, temperature=temperature, api_key=api_key)

        # Collect sources and scores
        all_results = log_results + feature_results
        docs = [d for d, _s, _md in all_results]
        score = max((s for _d, s, _md in all_results), default=0.0) if all_results else 0.0

        return {
            "answer": answer,
            "sources": docs,
            "score": score,
            "context": full_context,
        }

    def _extract_entities(self, query: str) -> dict:
        """Simple entity extraction: map keywords to tags."""
        entities = {}
        lower_query = query.lower()
        # Define mappings (expand as needed)
        mappings = {
            "project": ["pi-rag", "project"],
            "service": ["rag", "server", "llm", "embedding"],
            "feature": ["auth", "llm", "vector", "api"],
            "device": ["macos", "ios", "backend", "linux"]
        }
        for tag, keywords in mappings.items():
            for word in keywords:
                if word in lower_query:
                    entities[tag] = word
                    break
        return entities
