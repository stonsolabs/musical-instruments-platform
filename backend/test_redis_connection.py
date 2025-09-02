#!/usr/bin/env python3
"""
Test script to debug Redis connection issues
"""
import asyncio
import os
import sys
from typing import Optional

# Add the app directory to the path
sys.path.insert(0, '/app')

try:
    import redis.asyncio as redis
    print("✅ Redis asyncio imported successfully")
except ImportError as e:
    print(f"❌ Failed to import redis: {e}")
    sys.exit(1)

async def test_redis_connection():
    """Test different Redis connection formats"""
    
    # Get Redis URL from environment
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    print(f"🔍 Testing Redis URL: {redis_url}")
    
    # Test formats (using environment variable for password)
    redis_password = os.getenv("REDIS_PASSWORD", "")
    test_urls = [
        redis_url,  # Current setting
        f"rediss://:{redis_password}@getyourmusicgear-redis.redis.cache.windows.net:6380" if redis_password else None,
        f"redis://:{redis_password}@getyourmusicgear-redis.redis.cache.windows.net:6380" if redis_password else None,
    ]
    # Filter out None values
    test_urls = [url for url in test_urls if url]
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n🧪 Test {i}: {url}")
        try:
            # Create Redis client
            client = redis.from_url(url, decode_responses=True)
            print("✅ Client created successfully")
            
            # Test connection
            await client.ping()
            print("✅ PING successful")
            
            # Test set/get
            await client.set("test_key", "test_value", ex=30)
            value = await client.get("test_key")
            print(f"✅ SET/GET successful: {value}")
            
            # Clean up
            await client.delete("test_key")
            await client.close()
            print("✅ Connection test PASSED")
            return url
            
        except Exception as e:
            print(f"❌ Connection failed: {type(e).__name__}: {e}")
            try:
                await client.close()
            except:
                pass
    
    return None

async def test_manual_connection():
    """Test manual Redis connection with explicit parameters"""
    print("\n🔧 Testing manual connection...")
    
    redis_password = os.getenv("REDIS_PASSWORD")
    if not redis_password:
        print("❌ REDIS_PASSWORD environment variable not set")
        return
    
    try:
        client = redis.Redis(
            host="getyourmusicgear-redis.redis.cache.windows.net",
            port=6380,
            password=redis_password,
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True
        )
        
        await client.ping()
        print("✅ Manual connection successful")
        
        await client.set("test_key_manual", "test_value", ex=30)
        value = await client.get("test_key_manual")
        print(f"✅ Manual SET/GET successful: {value}")
        
        await client.delete("test_key_manual")
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ Manual connection failed: {type(e).__name__}: {e}")
        try:
            await client.close()
        except:
            pass
        return False

if __name__ == "__main__":
    print("🚀 Starting Redis connection tests...")
    print(f"📋 Environment REDIS_URL: {os.getenv('REDIS_URL', 'Not set')}")
    
    try:
        # Test URL-based connections
        working_url = asyncio.run(test_redis_connection())
        
        if working_url:
            print(f"\n🎉 SUCCESS! Working Redis URL: {working_url}")
        else:
            print("\n⚠️ URL-based connections failed, trying manual connection...")
            success = asyncio.run(test_manual_connection())
            
            if success:
                print("\n🎉 Manual connection works! URL format issue detected.")
            else:
                print("\n❌ All connection attempts failed!")
                
    except Exception as e:
        print(f"\n💥 Test script failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()