"""
Application configuration and settings
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "AI Legal Document Explainer"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    reload: bool = Field(default=True, env="RELOAD")
    
    # OpenAI
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_max_tokens: int = Field(default=2000, env="OPENAI_MAX_TOKENS")
    
    # Database
    database_url: str = Field(default="sqlite:///./legal_docs.db", env="DATABASE_URL")
    mongodb_url: Optional[str] = Field(default=None, env="MONGODB_URL")
    
    # File Upload
    max_file_size: int = Field(default=50 * 1024 * 1024, env="MAX_FILE_SIZE")  # 50MB
    allowed_file_types: list = ["application/pdf"]
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # AI Processing
    chunk_size: int = Field(default=1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, env="CHUNK_OVERLAP")
    max_chunks: int = Field(default=100, env="MAX_CHUNKS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that all required settings are present"""
    if not settings.openai_api_key:
        print("⚠️  Warning: OPENAI_API_KEY not set. AI features will be limited.")
    
    if not settings.mongodb_url:
        print("ℹ️  Info: MONGODB_URL not set. Using SQLite only.")
    
    print(f"✅ Configuration loaded successfully")
    print(f"   App: {settings.app_name} v{settings.app_version}")
    print(f"   Server: {settings.host}:{settings.port}")
    print(f"   Debug: {settings.debug}")
    print(f"   Database: {settings.database_url}")

# Validate settings on import
if __name__ == "__main__":
    validate_settings()
