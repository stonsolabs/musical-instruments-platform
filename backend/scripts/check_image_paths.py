import asyncio
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database connection string
DATABASE_URL = "postgresql://admin:qQqqDgXlIuBSZDUlgqzQEcoTPBkrCjVD@dpg-d2er32qdbo4c738oofng-a.frankfurt-postgres.render.com/musicgear_db"

# Convert to async URL
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

async def check_image_paths():
    """Check the current image paths in the products table."""
    
    print("Connecting to database...")
    print(f"Database: {DATABASE_URL.split('@')[1].split('/')[0]}")
    
    # Create async engine
    engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
    
    try:
        async with engine.begin() as conn:
            # Check if products table exists
            result = await conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'products'
                );
            """))
            table_exists = result.scalar()
            
            if not table_exists:
                print("❌ Products table does not exist!")
                return
            
            print("✅ Products table found")
            
            # Get total number of products
            result = await conn.execute(text("SELECT COUNT(*) FROM products;"))
            total_products = result.scalar()
            print(f"📊 Total products in database: {total_products}")
            
            # Get products with images
            result = await conn.execute(text("""
                SELECT id, sku, name, images 
                FROM products 
                WHERE images IS NOT NULL AND array_length(images, 1) > 0
                ORDER BY id;
            """))
            
            products_with_images = result.fetchall()
            print(f"📸 Products with images: {len(products_with_images)}")
            
            if not products_with_images:
                print("❌ No products with images found!")
                return
            
            print("\n" + "="*80)
            print("CURRENT IMAGE PATHS IN DATABASE:")
            print("="*80)
            
            local_paths = 0
            external_urls = 0
            empty_images = 0
            
            for product in products_with_images:
                product_id, sku, name, images = product
                print(f"\n🆔 Product ID: {product_id}")
                print(f"📦 SKU: {sku}")
                print(f"📝 Name: {name}")
                
                if not images:
                    print("❌ No images")
                    empty_images += 1
                    continue
                
                print(f"🖼️  Images ({len(images)}):")
                for i, image_path in enumerate(images, 1):
                    if image_path.startswith('/product-images/'):
                        print(f"   {i}. ✅ LOCAL: {image_path}")
                        local_paths += 1
                    elif image_path.startswith('http'):
                        print(f"   {i}. 🌐 EXTERNAL: {image_path}")
                        external_urls += 1
                    else:
                        print(f"   {i}. ❓ UNKNOWN: {image_path}")
            
            print("\n" + "="*80)
            print("SUMMARY:")
            print("="*80)
            print(f"📊 Total products checked: {len(products_with_images)}")
            print(f"✅ Local image paths: {local_paths}")
            print(f"🌐 External URLs: {external_urls}")
            print(f"❌ Empty images: {empty_images}")
            
            if local_paths > 0:
                print(f"\n🎉 {local_paths} local image paths found!")
            else:
                print(f"\n⚠️  No local image paths found. All images are external URLs.")
                
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
    finally:
        await engine.dispose()

async def main():
    """Main function."""
    print("🔍 Checking image paths in deployed database...")
    await check_image_paths()
    print("\n✅ Check completed!")

if __name__ == "__main__":
    asyncio.run(main())
