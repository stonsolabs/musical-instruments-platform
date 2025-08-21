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

def get_local_image_paths(sku, image_count=4):
    """Generate local image paths for a product."""
    local_images = []
    for i in range(image_count):
        filename = f"{sku.lower().replace('-', '_')}_{i + 1}.jpg"
        local_images.append(f"/product-images/{filename}")
    return local_images

async def update_image_paths():
    """Update all product image paths to use local paths."""
    
    print("Connecting to database...")
    print(f"Database: {DATABASE_URL.split('@')[1].split('/')[0]}")
    
    # Create async engine
    engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
    
    try:
        async with engine.begin() as conn:
            # Get all products
            result = await conn.execute(text("""
                SELECT id, sku, name, images 
                FROM products 
                ORDER BY id;
            """))
            
            products = result.fetchall()
            print(f"📊 Found {len(products)} products to update")
            
            updated_count = 0
            skipped_count = 0
            
            for product in products:
                product_id, sku, name, current_images = product
                
                print(f"\n🆔 Product ID: {product_id}")
                print(f"📦 SKU: {sku}")
                print(f"📝 Name: {name}")
                
                # Generate new local image paths
                new_images = get_local_image_paths(sku)
                
                # Check if images are already local
                if current_images and all(img.startswith('/product-images/') for img in current_images):
                    print("   ✅ Already using local paths - skipping")
                    skipped_count += 1
                    continue
                
                # Update the images
                await conn.execute(
                    text("UPDATE products SET images = :images WHERE id = :id"),
                    {"images": new_images, "id": product_id}
                )
                
                print(f"   🔄 Updated images:")
                for i, img in enumerate(new_images, 1):
                    print(f"      {i}. {img}")
                
                updated_count += 1
            
            print(f"\n" + "="*80)
            print("UPDATE SUMMARY:")
            print("="*80)
            print(f"📊 Total products processed: {len(products)}")
            print(f"✅ Updated: {updated_count}")
            print(f"⏭️  Skipped (already local): {skipped_count}")
            
            if updated_count > 0:
                print(f"\n🎉 Successfully updated {updated_count} products with local image paths!")
            else:
                print(f"\nℹ️  All products already have local image paths.")
                
    except Exception as e:
        print(f"❌ Error updating database: {e}")
    finally:
        await engine.dispose()

async def main():
    """Main function."""
    print("🔄 Updating database image paths to local paths...")
    await update_image_paths()
    print("\n✅ Update completed!")

if __name__ == "__main__":
    asyncio.run(main())
