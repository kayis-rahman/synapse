import os
import json
import requests

class RagLocalProvider:
    def __init__(self, base_url=None, top_k=5, api_key=None, timeout=30):
        self.base_url = base_url or os.environ.get("RAG_LOCAL_BASE_URL", "http://localhost:8000")
        self.top_k = top_k or int(os.environ.get("RAG_TOP_K", 5))
        self.api_key = api_key or os.environ.get("RAG_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
        self.timeout = timeout

    def query(self, prompt):
        url = f"{self.base_url.rstrip('/')}/query"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {"query": prompt, "top_k": self.top_k}
        resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
