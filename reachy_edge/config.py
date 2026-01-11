"""Configuration management for Reachy Edge Backend."""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    api_version: str = "0.1.0"
    
    # Identity
    reachy_id: str = "RCH-DEV-001"
    store_id: str = "STORE-DEV"
    zone_id: str = "ENTRANCE"
    
    # LLM Configuration
    llm_mode: str = "openai"  # "openai" | "local"
    openai_api_key: str | None = None
    local_model_path: str = "./models/llama-3b.gguf"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 100
    
    # π (Second Brain) Integration
    pi_url: str = "https://pi.example.com"
    pi_api_key: str = "dev-key"
    event_batch_size: int = 50
    event_batch_interval_s: int = 5
    pi_enabled: bool = False  # Set to True when π backend is ready
    
    # Cache Configuration
    l2_db_path: str = "./data/cache.db"
    l1_ttl_seconds: int = 300
    l1_max_size: int = 1000
    
    # Performance Tuning
    max_response_words: int = 35
    timeout_s: float = 1.0
    clarification_limit: int = 1
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure data directory exists
DATA_DIR = Path(settings.l2_db_path).parent
DATA_DIR.mkdir(parents=True, exist_ok=True)
