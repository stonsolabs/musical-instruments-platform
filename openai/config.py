import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration for Azure OpenAI batch processing."""
    
    def __init__(self):
        # Load from .env file if it exists
        self._load_env_file()
    
    def _load_env_file(self):
        """Load environment variables from .env file."""
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
    
    @property
    def AZURE_OPENAI_ENDPOINT(self) -> str:
        """Azure OpenAI endpoint for regular API calls."""
        return os.getenv("AZURE_OPENAI_ENDPOINT", "https://getyourmusicgear-openai.openai.azure.com/")
    
    @property
    def AZURE_OPENAI_DEPLOYMENT_NAME(self) -> str:
        """Azure OpenAI deployment name for regular API calls."""
        return os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4.1")
    
    @property
    def AZURE_OPENAI_BATCH_ENDPOINT(self) -> str:
        """Azure OpenAI endpoint for batch processing."""
        return os.getenv("AZURE_OPENAI_BATCH_ENDPOINT", "https://getyourmusicgear-openai.openai.azure.com/")
    
    @property
    def AZURE_OPENAI_BATCH_DEPLOYMENT_NAME(self) -> str:
        """Azure OpenAI deployment name for batch processing."""
        return os.getenv("AZURE_OPENAI_BATCH_DEPLOYMENT_NAME", "gpt-4.1")
    
    @property
    def OPENAI_API_KEY(self) -> str:
        """Azure OpenAI API key."""
        return os.getenv("OPENAI_API_KEY", "")
    
    @property
    def DATABASE_URL(self) -> str:
        """Database connection URL."""
        return os.getenv("DATABASE_URL", "")
    
    # Azure Storage Configuration
    @property
    def AZURE_STORAGE_CONNECTION_STRING(self) -> str:
        """Azure Storage connection string."""
        return os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    
    @property
    def AZURE_STORAGE_CONTAINER_NAME(self) -> str:
        """Azure Storage container name for batch results."""
        return os.getenv("AZURE_STORAGE_CONTAINER_NAME", "openai-batch-results")
    
    @property
    def AZURE_STORAGE_ACCOUNT_NAME(self) -> str:
        """Azure Storage account name."""
        return os.getenv("AZURE_STORAGE_ACCOUNT_NAME", "")
    
    @property
    def AZURE_STORAGE_ACCOUNT_KEY(self) -> str:
        """Azure Storage account key."""
        return os.getenv("AZURE_STORAGE_ACCOUNT_KEY", "")
    
    @property
    def BATCH_MAX_TOKENS(self) -> int:
        """Maximum tokens for batch processing."""
        return int(os.getenv("BATCH_MAX_TOKENS", "21000"))
    
    @property
    def BATCH_TEMPERATURE(self) -> float:
        """Temperature for batch processing."""
        return float(os.getenv("BATCH_TEMPERATURE", "0.1"))
    
    @property
    def BATCH_COMPLETION_WINDOW(self) -> str:
        """Completion window for batch processing."""
        return os.getenv("BATCH_COMPLETION_WINDOW", "24h")


# Global config instance
config = Config()
