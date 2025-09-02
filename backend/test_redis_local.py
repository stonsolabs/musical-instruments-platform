#!/usr/bin/env python3
"""
Local Redis connection test for Azure Cache for Redis
"""
import asyncio
import sys

def test_redis_sync():
    """Test Redis connection using synchronous client"""
    try:
        import redis
        print("✅ Redis library imported successfully")
    except ImportError:
        print("❌ Redis library not installed. Run: pip install redis")
        return False
    
    # Get Redis password from user input
    redis_password = input("Enter your Redis Primary Access Key: ").strip()
    if not redis_password:
        print("❌ No password provided")
        return False
    
    print(f"\n🔍 Testing connection to: getyourmusicgear-redis.redis.cache.windows.net:6380")
    
    try:
        # Create Redis client
        client = redis.Redis(
            host="getyourmusicgear-redis.redis.cache.windows.net",
            port=6380,
            password=redis_password,
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True,
            socket_connect_timeout=10,
            socket_timeout=10
        )
        
        print("✅ Redis client created")
        
        # Test connection
        response = client.ping()
        print(f"✅ PING successful: {response}")
        
        # Test set/get
        client.set("test_key_local", "test_value_from_local", ex=60)
        value = client.get("test_key_local")
        print(f"✅ SET/GET successful: {value}")
        
        # Test delete
        client.delete("test_key_local")
        print("✅ DELETE successful")
        
        # Get Redis info
        info = client.info()
        print(f"✅ Redis info: version={info.get('redis_version')}, connected_clients={info.get('connected_clients')}")
        
        client.close()
        print("\n🎉 All tests passed! Your Redis connection works perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {type(e).__name__}: {e}")
        return False

async def test_redis_async():
    """Test Redis connection using async client (same as your app)"""
    try:
        import redis.asyncio as redis
        print("\n🔄 Testing async Redis connection (same as your app uses)...")
    except ImportError:
        print("❌ Redis asyncio not available")
        return False
    
    # Get Redis password from user input
    redis_password = input("Enter your Redis Primary Access Key: ").strip()
    if not redis_password:
        print("❌ No password provided")
        return False
    
    try:
        # Create async Redis client
        client = redis.Redis(
            host="getyourmusicgear-redis.redis.cache.windows.net",
            port=6380,
            password=redis_password,
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True,
            socket_connect_timeout=10,
            socket_timeout=10
        )
        
        print("✅ Async Redis client created")
        
        # Test connection
        response = await client.ping()
        print(f"✅ Async PING successful: {response}")
        
        # Test set/get
        await client.set("test_key_async", "test_value_async", ex=60)
        value = await client.get("test_key_async")
        print(f"✅ Async SET/GET successful: {value}")
        
        # Test delete
        await client.delete("test_key_async")
        print("✅ Async DELETE successful")
        
        await client.aclose()
        print("🎉 Async tests passed! Your app should work with Redis!")
        return True
        
    except Exception as e:
        print(f"❌ Async connection failed: {type(e).__name__}: {e}")
        return False

def test_connection_string():
    """Test using connection string format"""
    try:
        import redis
    except ImportError:
        print("❌ Redis library not installed")
        return False
    
    redis_password = input("Enter your Redis Primary Access Key: ").strip()
    if not redis_password:
        print("❌ No password provided")
        return False
    
    # Test connection string format
    connection_string = f"rediss://:{redis_password}@getyourmusicgear-redis.redis.cache.windows.net:6380"
    print(f"\n🔗 Testing connection string format...")
    print(f"Connection string: rediss://:***@getyourmusicgear-redis.redis.cache.windows.net:6380")
    
    try:
        client = redis.from_url(connection_string, decode_responses=True)
        response = client.ping()
        print(f"✅ Connection string PING successful: {response}")
        
        client.set("test_connection_string", "works", ex=60)
        value = client.get("test_connection_string")
        print(f"✅ Connection string SET/GET successful: {value}")
        
        client.delete("test_connection_string")
        client.close()
        
        print("🎉 Connection string format works!")
        print(f"\n📋 Use this in your Azure App Service:")
        print(f"REDIS_URL=rediss://:{redis_password}@getyourmusicgear-redis.redis.cache.windows.net:6380")
        return True
        
    except Exception as e:
        print(f"❌ Connection string failed: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Azure Cache for Redis Local Connection Test")
    print("=" * 50)
    
    # Test 1: Synchronous connection
    print("\n1️⃣ Testing synchronous Redis connection...")
    sync_success = test_redis_sync()
    
    if sync_success:
        # Test 2: Asynchronous connection (same as your app)
        print("\n2️⃣ Testing asynchronous Redis connection...")
        async_success = asyncio.run(test_redis_async())
        
        if async_success:
            # Test 3: Connection string format
            print("\n3️⃣ Testing connection string format...")
            connection_success = test_connection_string()
            
            if connection_success:
                print("\n🎊 ALL TESTS PASSED!")
                print("Your Redis is working perfectly. The issue might be in your Azure App Service configuration.")
            else:
                print("\n⚠️ Connection string test failed, but direct connection works.")
        else:
            print("\n⚠️ Async test failed, but sync works. Check async redis library.")
    else:
        print("\n❌ Basic connection failed. Check your access key and network connectivity.")
