"""
Application Configuration

This module handles all application settings using Pydantic Settings
for environment variable management and validation.
"""

import os
from pydantic_settings import BaseSettings
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden by setting the corresponding
    environment variable. For example, DATABASE_URL can be set
    in the .env file or as an OS environment variable.
    """
    
    # Application Settings
    app_name: str = "TaskMaster"
    debug: bool = Field(default=False, description="Enable debug mode")
    api_version: str = "v1"
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://postgres:admin@localhost:5432/task_master_database",
        description="PostgreSQL connection string"
    )
    
    # JWT Authentication Settings
    SECRET_KEY: SecretStr = Field(
        description="Secret key for JWT encoding. Generate with: openssl rand -hex 32"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="JWT token expiration time in minutes"
    )
    
    # Redis Cache Settings
    REDIS_HOST: str = Field(default="localhost", description="Redis server host")
    REDIS_PORT: int = Field(default=6379, description="Redis server port")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    CACHE_EXPIRE_MINUTES: int = Field(default=5, description="Default cache TTL in minutes")

    # Email Settings
    MAIL_USERNAME: str = Field(default="", description="SMTP Username (Email)")
    MAIL_PASSWORD: str = Field(default="", description="SMTP Password (App Password)")
    MAIL_FROM: str = Field(default="noreply@taskmaster.com", description="From Email Address")
    MAIL_PORT: int = Field(default=587, description="SMTP Port (587 for TLS)")
    MAIL_SERVER: str = Field(default="smtp.gmail.com", description="SMTP Server Host")
    MAIL_STARTTLS: bool = Field(default=True, description="Enable STARTTLS")
    MAIL_SSL_TLS: bool = Field(default=False, description="Enable SSL/TLS")

    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Allow extra fields to be ignored
        extra = "ignore"


# Create global settings instance
settings = Settings()