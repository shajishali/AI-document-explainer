"""
Configuration settings for the AI Legal Document Explainer application.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    app_name: str = "AI Legal Document Explainer"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API settings
    api_prefix: str = "/api/v1"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # OpenAI settings
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    openai_max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
    
    # ChromaDB settings
    chroma_db_path: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    chroma_db_persist: bool = os.getenv("CHROMA_DB_PERSIST", "True").lower() == "true"
    
    # Document processing settings
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    supported_formats: list[str] = ["pdf", "docx", "txt", "rtf"]
    temp_dir: str = os.getenv("TEMP_DIR", "./temp")
    
    # Logging settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security settings
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    api_key_header: str = os.getenv("API_KEY_HEADER", "X-API-Key")
    
    # AI model settings
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the application settings."""
    return settings

def validate_settings() -> bool:
    """Validate that all required settings are present."""
    required_settings = [
        "openai_api_key",
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting):
            missing_settings.append(setting)
    
    if missing_settings:
        print(f"Warning: Missing required settings: {', '.join(missing_settings)}")
        print("Some features may not work without these settings.")
        return False
    
    return True

# Validate settings on import
if __name__ == "__main__":
    validate_settings()
