"""Configuration for π backend."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_version: str = "0.1.0"
    db_path: str = "./pi_backend/data/pi.db"
    host: str = "0.0.0.0"
    port: int = 8100

    inference_provider: str = "openai"
    inference_model: str = "gpt-4.1-mini"
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    vector_backend: str = "sqlite"  # sqlite | qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "pi_entities"

    class Config:
        env_file = ".env"
        env_prefix = "PI_"


settings = Settings()
