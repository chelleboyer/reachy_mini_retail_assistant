"""Vector storage abstraction with optional Qdrant runtime adapter."""


class VectorStore:
    def __init__(self, backend: str = "sqlite", qdrant_url: str = "http://localhost:6333", collection: str = "pi_entities"):
        self.backend = backend
        self.qdrant_url = qdrant_url
        self.collection = collection
        self.client = None
        if backend == "qdrant":
            try:
                from qdrant_client import QdrantClient  # type: ignore
                self.client = QdrantClient(url=qdrant_url)
            except Exception:
                self.client = None

    def stats(self) -> dict:
        return {
            "backend": self.backend,
            "enabled": self.client is not None if self.backend == "qdrant" else True,
        }
