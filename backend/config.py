"""Configuration settings for PPT Reviewer Agent."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # API Keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # File Upload Settings
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    allowed_formats: list[str] = ["pptx", "ppt"]
    upload_dir: str = os.getenv("UPLOAD_DIR", "/tmp/ppt_uploads")
    
    # API Settings
    api_title: str = "PPT Reviewer Agent API"
    api_version: str = "1.0.0"
    api_description: str = "AI-powered PowerPoint analyzer"
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS Settings
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
