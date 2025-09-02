#!/usr/bin/env python3
"""
Check image URL patterns and accessibility
"""

import asyncio
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Product

async def check_image_urls():
    """Check different image URL patterns and their accessibility"""
    
    print("🖼️  Checking Image URL Patterns")
    print("=" * 50)
    
    database_url = "postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear"
    async_db_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    engine = create_async_engine(async_db_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Get sample products with images
            query = (
                select(Product)
                .where(
                    Product.is_active == True,
                    Product.images.isnot(None)
                )
                .limit(20)
            )
            
            result = await session.execute(query)
            products = result.scalars().all()
            
            print(f"📊 Checking {len(products)} products with images...")
            
            # Analyze image URL patterns
            url_patterns = {}
            all_urls = []
            
            for i, product in enumerate(products):
                print(f"\n{i+1}. {product.name}")
                
                if product.images:
                    for key, image_data in product.images.items():
                        if isinstance(image_data, dict) and "url" in image_data:
                            url = image_data["url"]
                        elif isinstance(image_data, str):
                            url = image_data
                        else:
                            print(f"  ❓ Unknown image format: {key} = {type(image_data)}")
                            continue
                        
                        print(f"  📷 {key}: {url}")
                        all_urls.append(url)
                        
                        # Categorize URL patterns
                        if "getyourmusicgear.blob.core.windows.net" in url:
                            url_patterns["azure_blob"] = url_patterns.get("azure_blob", 0) + 1
                        elif "thomann.de" in url:
                            url_patterns["thomann_direct"] = url_patterns.get("thomann_direct", 0) + 1
                        elif url.startswith("http"):
                            domain = url.split("/")[2] if len(url.split("/")) > 2 else url
                            url_patterns[f"other_{domain}"] = url_patterns.get(f"other_{domain}", 0) + 1
                        else:
                            url_patterns["invalid"] = url_patterns.get("invalid", 0) + 1
            
            print("\n" + "=" * 50)
            print("📊 URL Pattern Analysis")
            print("=" * 50)
            
            for pattern, count in sorted(url_patterns.items(), key=lambda x: x[1], reverse=True):
                print(f"  {pattern}: {count} URLs")
            
            print(f"\nTotal URLs analyzed: {len(all_urls)}")
            
            # Test accessibility of different URL types
            print("\n" + "=" * 50)
            print("🌐 URL Accessibility Test")
            print("=" * 50)
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Test a few URLs from each pattern
                for pattern in ["azure_blob", "thomann_direct"]:
                    pattern_urls = [url for url in all_urls if 
                                  (pattern == "azure_blob" and "getyourmusicgear.blob.core.windows.net" in url) or
                                  (pattern == "thomann_direct" and "thomann.de" in url)]
                    
                    if pattern_urls:
                        print(f"\n🔍 Testing {pattern} URLs:")
                        for url in pattern_urls[:3]:  # Test first 3 of each type
                            try:
                                response = await client.head(url)
                                status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
                                print(f"  {status} {url}")
                            except Exception as e:
                                print(f"  💥 ERROR {url}: {str(e)[:100]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_image_urls())
