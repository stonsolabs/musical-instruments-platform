#!/usr/bin/env python3
"""
Very simple test script
"""

import os
import asyncio

async def main():
    print("🚀 Simple test starting...")
    
    # Check environment variables
    print(f"IPROYAL_PROXY_URL: {'SET' if os.getenv('IPROYAL_PROXY_URL') else 'NOT SET'}")
    print(f"DATABASE_URL: {'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")
    print(f"ASSIGNED_CATEGORIES: {os.getenv('ASSIGNED_CATEGORIES', 'NOT SET')}")
    print(f"TEST_MODE: {os.getenv('TEST_MODE', 'NOT SET')}")
    
    # Check if thomann_urls.txt exists
    if os.path.exists('thomann_urls.txt'):
        print("✅ thomann_urls.txt exists")
        with open('thomann_urls.txt', 'r') as f:
            urls = f.readlines()
            print(f"✅ Loaded {len(urls)} URLs")
    else:
        print("❌ thomann_urls.txt not found")
    
    print("✅ Test completed")

if __name__ == "__main__":
    asyncio.run(main())
