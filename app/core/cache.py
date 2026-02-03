"""
Redis Cache Utility Module

Provides a simple interface for caching operations using Redis.
Supports JSON serialization for storing complex data structures.
"""

import redis
import json
from datetime import timedelta
from typing import Any, Optional

from app.core.config import settings


class CacheClient:
    """
    Redis cache client wrapper with connection management.
    
    This class provides a singleton-like pattern for Redis connections
    and handles JSON serialization/deserialization automatically.
    """
    
    _instance: Optional[redis.Redis] = None
    
    @classmethod
    def get_client(cls) -> redis.Redis:
        """
        Get or create a Redis client connection.
        
        Returns:
            Redis client instance
        """
        if cls._instance is None:
            cls._instance = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True
            )
        return cls._instance
    
    @classmethod
    def close(cls) -> None:
        """Close the Redis connection."""
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None


# Create default client
redis_client = CacheClient.get_client()


def get_cache(key: str) -> Optional[Any]:
    """
    Retrieve data from cache.
    
    Args:
        key: Cache key to lookup
        
    Returns:
        Cached data (JSON deserialized) or None if not found
    """
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except redis.ConnectionError:
        # Log error in production, silently fail for now
        return None


def set_cache(key: str, value: Any, expire_minutes: int = None) -> bool:
    """
    Store data in cache with optional expiration.
    
    Args:
        key: Cache key
        value: Data to cache (will be JSON serialized)
        expire_minutes: TTL in minutes (defaults to settings)
        
    Returns:
        True if successful, False otherwise
    """
    if expire_minutes is None:
        expire_minutes = settings.CACHE_EXPIRE_MINUTES
    
    try:
        redis_client.setex(
            key, 
            timedelta(minutes=expire_minutes), 
            json.dumps(value)
        )
        return True
    except redis.ConnectionError:
        return False


def delete_cache(key: str) -> bool:
    """
    Delete a key from cache.
    
    Args:
        key: Cache key to delete
        
    Returns:
        True if deleted, False otherwise
    """
    try:
        redis_client.delete(key)
        return True
    except redis.ConnectionError:
        return False


def clear_pattern(pattern: str) -> int:
    """
    Delete all keys matching a pattern.
    
    Args:
        pattern: Key pattern (e.g., "tasks:user:*")
        
    Returns:
        Number of keys deleted
    """
    try:
        keys = redis_client.keys(pattern)
        if keys:
            return redis_client.delete(*keys)
        return 0
    except redis.ConnectionError:
        return 0


def cache_exists(key: str) -> bool:
    """
    Check if a key exists in cache.
    
    Args:
        key: Cache key to check
        
    Returns:
        True if exists, False otherwise
    """
    try:
        return redis_client.exists(key) > 0
    except redis.ConnectionError:
        return False