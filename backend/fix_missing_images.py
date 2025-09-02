#!/usr/bin/env python3
"""
Fix Missing Product Images Job
- List all products with broken/missing Azure blob images
- Check if alternative images exist in blob storage
- Provide fix commands and suggestions
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Product

async def find_missing_images():
    """Find products with broken Azure blob images"""
    
    print("🔧 Finding Products with Missing Azure Blob Images")
    print("=" * 60)
    
    database_url = "postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear"
    async_db_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    engine = create_async_engine(async_db_url)
    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Load the detailed audit report
    try:
        # Find the latest audit report
        audit_files = [f for f in os.listdir('.') if f.startswith('image_audit_report_') and f.endswith('.json')]
        if not audit_files:
            print("❌ No audit report found. Run audit_product_images.py first.")
            return
        
        latest_report = sorted(audit_files)[-1]
        print(f"📋 Loading audit report: {latest_report}")
        
        with open(latest_report, 'r') as f:
            audit_data = json.load(f)
        
        broken_azure_images = [
            img for img in audit_data['broken_images'] 
            if img['category'] == 'azure_blob'
        ]
        
        print(f"🚨 Found {len(broken_azure_images)} broken Azure blob images")
        print()
        
        # Group by product for easier fixing
        products_with_broken_images = {}
        for img in broken_azure_images:
            product_id = img['product_id']
            if product_id not in products_with_broken_images:
                products_with_broken_images[product_id] = {
                    'name': img['product_name'],
                    'broken_images': []
                }
            products_with_broken_images[product_id]['broken_images'].append(img)
        
        print(f"📊 {len(products_with_broken_images)} products affected")
        print()
        
        # Sample broken products
        print("🔍 SAMPLE PRODUCTS WITH BROKEN IMAGES")
        print("-" * 45)
        
        sample_count = 0
        for product_id, info in products_with_broken_images.items():
            if sample_count >= 20:  # Show first 20
                break
                
            print(f"\n{sample_count + 1}. Product ID: {product_id}")
            print(f"   Name: {info['name']}")
            print(f"   Broken images: {len(info['broken_images'])}")
            
            for img in info['broken_images']:
                # Extract filename from URL
                url = img['url']
                filename = url.split('/')[-1] if '/' in url else url
                print(f"     ❌ {img['image_key']}: {filename}")
            
            sample_count += 1
        
        # Generate Azure CLI commands to check blob storage
        print(f"\n💡 FIXING SUGGESTIONS")
        print("-" * 25)
        print("1. Check what images actually exist in Azure blob storage:")
        print("   az storage blob list --container-name product-images --account-name getyourmusicgear --output table")
        print()
        
        print("2. Check if images exist with different names:")
        print("   az storage blob list --container-name product-images --account-name getyourmusicgear --prefix thomann/ --output table")
        print()
        
        print("3. Sample commands to check specific missing images:")
        sample_images = broken_azure_images[:5]
        for img in sample_images:
            url = img['url']
            blob_name = url.split('/product-images/')[-1] if '/product-images/' in url else url.split('/')[-1]
            print(f"   az storage blob show --container-name product-images --name '{blob_name}' --account-name getyourmusicgear")
        
        print(f"\n4. If images are missing, check the crawler/uploader logs")
        print("5. Consider re-running the image crawler for missing products")
        
        # Generate SQL update commands for products without images
        async with session_maker() as session:
            products_without_images_query = select(Product).where(
                Product.is_active == True,
                Product.images.is_(None)
            )
            
            result = await session.execute(products_without_images_query)
            products_without_images = result.scalars().all()
            
            if products_without_images:
                print(f"\n📷 PRODUCTS WITHOUT ANY IMAGES: {len(products_without_images)}")
                print("-" * 40)
                
                for i, product in enumerate(products_without_images[:10]):
                    print(f"  {i+1}. ID: {product.id} - {product.name}")
                
                if len(products_without_images) > 10:
                    print(f"  ... and {len(products_without_images) - 10} more")
        
        # Save list of broken products for further processing
        broken_products_data = {
            "timestamp": datetime.now().isoformat(),
            "total_broken_products": len(products_with_broken_images),
            "products_with_broken_images": dict(list(products_with_broken_images.items())[:100])  # Sample
        }
        
        filename = f"broken_images_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(broken_products_data, f, indent=2, default=str)
        
        print(f"\n💾 Broken products list saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(find_missing_images())
