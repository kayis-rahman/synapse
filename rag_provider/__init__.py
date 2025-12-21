try:
    from .provider import RagLocalProvider
except Exception:
    class RagLocalProvider:  # fallback stub
        def __init__(self, *args, **kwargs):
            raise RuntimeError("RagLocalProvider is not available in this environment yet.")
        def query(self, *args, **kwargs):
            raise RuntimeError("RagLocalProvider is not available in this environment yet.")

__all__ = ["RagLocalProvider"]
