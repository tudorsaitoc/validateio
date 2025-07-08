import secrets
from typing import Any, List, Optional, Union

from pydantic import AnyHttpUrl, Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "ValidateIO"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="PYTHON_ENV")
    
    # Server
    HOST: str = Field(default="0.0.0.0", env="API_HOST")
    PORT: int = Field(default=8000, env="API_PORT")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Security
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=["http://localhost:3000", "http://localhost:3001"]
    )
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return v
    
    # Database
    DATABASE_URL: Optional[PostgresDsn] = Field(default=None, env="DATABASE_URL")
    
    # Supabase Configuration
    SUPABASE_URL: Optional[str] = Field(default=None, env="SUPABASE_URL")
    SUPABASE_ANON_KEY: Optional[str] = Field(default=None, env="SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_KEY: Optional[str] = Field(default=None, env="SUPABASE_SERVICE_KEY")
    SUPABASE_JWT_SECRET: Optional[str] = Field(default=None, env="SUPABASE_JWT_SECRET")
    USE_SUPABASE_AUTH: bool = Field(default=False, env="USE_SUPABASE_AUTH")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0", env="CELERY_RESULT_BACKEND")
    
    # AI/LLM
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    LANGCHAIN_API_KEY: Optional[str] = Field(default=None, env="LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2: bool = Field(default=True, env="LANGCHAIN_TRACING_V2")
    LANGCHAIN_PROJECT: str = Field(default="validateio", env="LANGCHAIN_PROJECT")
    
    # Vector Store
    CHROMA_HOST: str = Field(default="localhost", env="CHROMA_HOST")
    CHROMA_PORT: int = Field(default=8001, env="CHROMA_PORT")
    CHROMA_PERSIST_DIRECTORY: str = Field(default="./.chroma", env="CHROMA_PERSIST_DIRECTORY")
    
    # External APIs
    SERPER_API_KEY: Optional[str] = Field(default=None, env="SERPER_API_KEY")
    RESEND_API_KEY: Optional[str] = Field(default=None, env="RESEND_API_KEY")
    
    # Feature Flags
    ENABLE_MARKETING_AGENT: bool = Field(default=False, env="ENABLE_MARKETING_AGENT")
    ENABLE_EXPERIMENT_AGENT: bool = Field(default=True, env="ENABLE_EXPERIMENT_AGENT")
    ENABLE_RESEARCH_AGENT: bool = Field(default=True, env="ENABLE_RESEARCH_AGENT")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_REQUESTS_PER_MINUTE")
    RATE_LIMIT_REQUESTS_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_REQUESTS_PER_HOUR")
    
    # Agent Configuration
    AGENT_MAX_EXECUTION_TIME: int = 180  # 3 minutes in seconds
    AGENT_MAX_RETRIES: int = 3
    AGENT_TIMEOUT_SECONDS: int = 30
    
    # Cost Configuration
    MAX_COST_PER_VALIDATION: float = 2.00  # $2.00 USD
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()