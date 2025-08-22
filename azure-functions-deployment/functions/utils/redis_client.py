import redis
import json
import os
import logging
from typing import Optional, Any, Dict, List

logger = logging.getLogger(__name__)

# Initialize Redis client
try:
    redis_client = redis.Redis.from_url(
        os.getenv("REDIS_CONNECTION_STRING"),
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True
    )
    
    # Test connection
    redis_client.ping()
    logger.info("Redis connection established successfully")
    
except Exception as e:
    logger.error(f"Failed to connect to Redis: {str(e)}")
    redis_client = None

class RedisCache:
    """Redis cache utility class"""
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        if not redis_client:
            return None
            
        try:
            value = redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {str(e)}")
            return None
    
    @staticmethod
    def set(key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache with expiration"""
        if not redis_client:
            return False
            
        try:
            redis_client.setex(key, expire, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {str(e)}")
            return False
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete key from cache"""
        if not redis_client:
            return False
            
        try:
            redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {str(e)}")
            return False
    
    @staticmethod
    def exists(key: str) -> bool:
        """Check if key exists in cache"""
        if not redis_client:
            return False
            
        try:
            return redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {str(e)}")
            return False
    
    @staticmethod
    def incr(key: str, expire: int = 60) -> Optional[int]:
        """Increment counter (useful for rate limiting)"""
        if not redis_client:
            return None
            
        try:
            pipe = redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, expire)
            result = pipe.execute()
            return result[0]
        except Exception as e:
            logger.error(f"Error incrementing cache key {key}: {str(e)}")
            return None

# Cache decorator
def cache_result(expire: int = 3600):
    """Decorator to cache function results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = RedisCache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            RedisCache.set(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator

# Rate limiting utility
def check_rate_limit(identifier: str, limit: int = 100, window: int = 60) -> bool:
    """Check rate limit for given identifier"""
    key = f"rate_limit:{identifier}"
    current = RedisCache.incr(key, window)
    
    if current is None:
        return True  # Allow if Redis is unavailable
    
    return current <= limit
