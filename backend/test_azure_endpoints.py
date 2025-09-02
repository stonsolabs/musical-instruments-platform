#!/usr/bin/env python3
"""
Azure Backend Diagnostic Script
Tests various endpoints to identify issues with database connectivity, Redis, etc.
"""

import asyncio
import httpx
import json
from typing import Dict, Any

# Azure backend configuration
BASE_URL = "https://getyourmusicgear-api.azurewebsites.net"
API_KEY = "de798fd16f6a38539f9d590dd72c4a02f20afccd782e91bbbdc34037482632db"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

async def test_endpoint(client: httpx.AsyncClient, endpoint: str, description: str) -> Dict[str, Any]:
    """Test a single endpoint and return results"""
    url = f"{BASE_URL}{endpoint}"
    print(f"🔍 Testing {description}")
    print(f"   URL: {url}")
    
    try:
        response = await client.get(url, headers=headers, timeout=30.0)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Success - Response length: {len(str(data))}")
                return {"success": True, "status": response.status_code, "data": data}
            except json.JSONDecodeError:
                print(f"   ⚠️  Success but invalid JSON response")
                return {"success": False, "status": response.status_code, "error": "Invalid JSON"}
        else:
            error_text = response.text[:200] + "..." if len(response.text) > 200 else response.text
            print(f"   ❌ Error - {error_text}")
            return {"success": False, "status": response.status_code, "error": error_text}
            
    except Exception as e:
        print(f"   💥 Exception - {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Run all diagnostic tests"""
    print("🚀 Starting Azure Backend Diagnostics")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        
        # Test endpoints in order of importance
        tests = [
            ("/health", "Health Check (no auth)"),
            ("/api/v1/categories", "Categories API"),
            ("/api/v1/brands", "Brands API"),
            ("/api/v1/products?limit=3", "Products API (limit 3)"),
            ("/api/v1/products/1", "Single Product API"),
            ("/api/v1/search/autocomplete?q=guitar&limit=3", "Search Autocomplete"),
            ("/api/v1/trending/instruments?limit=3", "Trending Instruments"),
            ("/api/v1/affiliate-stores", "Affiliate Stores"),
        ]
        
        results = {}
        
        for endpoint, description in tests:
            print()
            result = await test_endpoint(client, endpoint, description)
            results[endpoint] = result
            
            # Add delay between requests to avoid overwhelming the server
            await asyncio.sleep(1)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 50)
        
        successful = 0
        failed = 0
        
        for endpoint, result in results.items():
            status = "✅ PASS" if result.get("success") else "❌ FAIL"
            print(f"{status} {endpoint}")
            if not result.get("success"):
                error = result.get("error", "Unknown error")
                print(f"      Error: {error}")
            
            if result.get("success"):
                successful += 1
            else:
                failed += 1
        
        print(f"\nResults: {successful} passed, {failed} failed")
        
        # Specific diagnostics
        print("\n" + "=" * 50)
        print("🔧 SPECIFIC DIAGNOSTICS")
        print("=" * 50)
        
        # Check if Redis is working (trending endpoint)
        trending_result = results.get("/api/v1/trending/instruments?limit=3")
        if trending_result and not trending_result.get("success"):
            print("❌ Redis/Trending Issues detected:")
            print("   - Trending endpoint failing")
            print("   - Likely Redis connection or trending service issues")
        
        # Check if database is working (products endpoint)
        products_result = results.get("/api/v1/products?limit=3")
        if products_result and not products_result.get("success"):
            print("❌ Database Issues detected:")
            print("   - Products endpoint failing")
            print("   - Likely PostgreSQL connection issues")
        
        # Check if basic functionality works (categories)
        categories_result = results.get("/api/v1/categories")
        if categories_result and categories_result.get("success"):
            print("✅ Basic database connectivity working (categories succeed)")
        
        print("\n🏁 Diagnostics complete!")

if __name__ == "__main__":
    asyncio.run(main())
