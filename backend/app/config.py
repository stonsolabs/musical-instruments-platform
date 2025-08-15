import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # Database - Ensure asyncpg is used
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/musical_instruments")
    
    # Fix DATABASE_URL to use asyncpg if it doesn't already
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.DATABASE_URL
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # API Settings
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Musical Instruments Platform")
    
    # Environment
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Production domain configuration
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    DOMAIN: str = os.getenv("DOMAIN", "getyourmusicgear.com")
    
    # CORS - Updated for Render backend + Vercel frontend
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        if self.ENVIRONMENT == "production":
            # Allow Vercel frontend domains
            vercel_origins = [
                f"https://{self.DOMAIN}",
                f"https://www.{self.DOMAIN}",
                "https://getyourmusicgear.vercel.app",  # Default Vercel domain
                "https://musical-instruments-platform.vercel.app",  # Alternative Vercel domain
            ]
            
            # Add any custom Vercel preview domains
            vercel_preview = os.getenv("VERCEL_PREVIEW_DOMAINS", "").split(",")
            vercel_origins.extend([domain.strip() for domain in vercel_preview if domain.strip()])
            
            return vercel_origins
        else:
            return ["*"]  # Allow all origins in development for easier debugging
    
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Affiliate Programs
    AMAZON_ASSOCIATE_TAG: str = os.getenv("AMAZON_ASSOCIATE_TAG", "")
    THOMANN_AFFILIATE_ID: str = os.getenv("THOMANN_AFFILIATE_ID", "")
    
    # Render.com specific settings
    PORT: int = int(os.getenv("PORT", "8000"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
