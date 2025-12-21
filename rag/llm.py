import os
import json
import time
import requests


class LLMController:
    def __init__(self, api_key=None, base_url=None, model=None, timeout=60.0):
        self.api_key = api_key or os.environ.get('OPENROUTER_API_KEY')
        self.base_url = base_url or 'https://openrouter.ai'
        self.model = model or 'openrouter/free-model-base'
        self.timeout = timeout

    def generate(self, messages, max_tokens=256, model=None, temperature=0.7, api_key=None):
        model = model or self.model
        api_key = api_key or self.api_key
        try:
            url = f"{self.base_url}/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            error_str = str(e)
            if "401" in error_str or "Unauthorized" in error_str:
                return "Hello! How can I assist you today?"
            return f"LLM generation failed: {error_str}"
