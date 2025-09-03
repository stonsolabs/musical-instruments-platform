import os
import secrets
import logging
from pydantic_settings import BaseSettings
from typing import Optional, List

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Database - Secure configuration with validation
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        if not self.DATABASE_URL:
            if self.ENVIRONMENT == "development":
                return "postgresql+asyncpg://user:password@localhost:5432/database"
            else:
                raise ValueError("DATABASE_URL environment variable is required in production")
        
        if self.DATABASE_URL.startswith("postgresql://"):
            # Add SSL requirement for production
            base_url = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
            if self.ENVIRONMENT == "production" and "sslmode=" not in base_url:
                connector = "&" if "?" in base_url else "?"
                return f"{base_url}{connector}sslmode=require"
            return base_url
        return self.DATABASE_URL
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security - Generate secure defaults, require strong values in production
    SECRET_KEY: str = os.getenv("SECRET_KEY") or secrets.token_urlsafe(64)
    API_KEY: str = os.getenv("API_KEY", "")
    
    # API Settings
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "getyourmusicgear")
    
    # Environment
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Production domain configuration
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    DOMAIN: str = os.getenv("DOMAIN", "getyourmusicgear.com")
    
    # CORS - Secure configuration for App Service deployment
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        if self.ENVIRONMENT == "production":
            # Production: Explicit allowlist for security
            production_origins = [
                f"https://{self.DOMAIN}",
                f"https://www.{self.DOMAIN}",
                "https://getyourmusicgear.vercel.app",
                "https://musical-instruments-platform.vercel.app",
            ]
            
            # Add verified Vercel preview domains from environment
            vercel_domains = os.getenv("ALLOWED_VERCEL_DOMAINS", "").split(",")
            for domain in vercel_domains:
                if domain.strip() and domain.strip().endswith(".vercel.app"):
                    production_origins.append(f"https://{domain.strip()}")
            
            logger.info(f"Production CORS origins: {len(production_origins)} domains")
            return production_origins
        else:
            # Development: Restricted to localhost only
            dev_origins = [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                self.FRONTEND_URL
            ]
            logger.info("Development CORS: localhost only")
            return dev_origins
    
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Affiliate Programs
    AMAZON_ASSOCIATE_TAG: str = os.getenv("AMAZON_ASSOCIATE_TAG", "")
    THOMANN_AFFILIATE_ID: str = os.getenv("THOMANN_AFFILIATE_ID", "")
    
    # Render.com specific settings
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Validation methods
    def validate_production_settings(self):
        """Validate critical settings for production deployment"""
        errors = []
        
        if self.ENVIRONMENT == "production":
            if not self.API_KEY:
                errors.append("API_KEY is required in production")
            elif len(self.API_KEY) < 16:
                errors.append("API_KEY must be at least 16 characters long")
                
            if not self.DATABASE_URL:
                errors.append("DATABASE_URL is required in production")
        
        if errors:
            logger.error(f"Configuration validation failed: {errors}")
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        logger.info(f"Configuration validated for {self.ENVIRONMENT} environment")

    class Config:
        env_file = ".env"
        case_sensitive = True

# Initialize settings
settings = Settings()

# Validate configuration on startup
try:
    settings.validate_production_settings()
except ValueError as e:
    logger.error(f"Startup configuration error: {e}")
    # Don't raise in development to allow easier setup
    if settings.ENVIRONMENT == "production":
        raise
