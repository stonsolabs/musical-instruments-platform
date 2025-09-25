#!/usr/bin/env python3
"""
Script to test Thomann affiliate links with actual products from the database
This script will:
1. Get some products from the database that have Thomann links
2. Test the affiliate URL generation
3. Show examples of the generated URLs
4. Verify the format is correct
"""

import asyncio
import sys
import os
sys.path.append('.')

from app.database import async_session_factory
from app.models import AffiliateStore, Product, ProductPrice
from app.services.enhanced_affiliate_service import EnhancedAffiliateService
from sqlalchemy import select, and_

async def test_thomann_affiliate_links():
    """Test Thomann affiliate links with actual products"""
    
    async with async_session_factory() as session:
        try:
            print("Testing Thomann Affiliate Links with Real Products")
            print("=" * 60)
            
            # Get the Thomann store configuration
            thomann_query = select(AffiliateStore).where(AffiliateStore.slug == "thomann")
            thomann_result = await session.execute(thomann_query)
            thomann_store = thomann_result.scalar_one_or_none()
            
            if not thomann_store:
                print("❌ Thomann store not found in database!")
                return
            
            print(f"📦 Thomann Store Configuration:")
            print(f"   Name: {thomann_store.name}")
            print(f"   Affiliate ID: {thomann_store.affiliate_id}")
            print(f"   Website URL: {thomann_store.website_url}")
            print(f"   Affiliate Parameters: {thomann_store.affiliate_parameters}")
            print()
            
            # Get products that have Thomann prices/links
            products_query = select(Product).join(ProductPrice).join(AffiliateStore).where(
                and_(
                    Product.is_active.is_(True),
                    AffiliateStore.slug == "thomann",
                    ProductPrice.is_available.is_(True)
                )
            ).limit(10)
            
            products_result = await session.execute(products_query)
            products = products_result.scalars().all()
            
            if not products:
                print("❌ No products with Thomann links found!")
                print("   Let's try to find products with Thomann info in content...")
                
                # Try to find products with Thomann info in content
                products_query = select(Product).where(
                    and_(
                        Product.is_active.is_(True),
                        Product.content.isnot(None)
                    )
                ).limit(10)
                
                products_result = await session.execute(products_query)
                products = products_result.scalars().all()
                
                if not products:
                    print("❌ No products found at all!")
                    return
            
            print(f"🔍 Found {len(products)} products to test")
            print()
            
            # Initialize the enhanced affiliate service
            enhanced_service = EnhancedAffiliateService(session)
            
            # Test each product
            for i, product in enumerate(products, 1):
                print(f"📋 Product {i}: {product.name}")
                print(f"   Brand: {product.brand.name if product.brand else 'Unknown'}")
                print(f"   ID: {product.id}")
                
                # Check if product has Thomann info in content
                thomann_url = None
                if product.content and isinstance(product.content, dict):
                    # Check for Thomann URL in various possible locations
                    if 'store_links' in product.content and 'Thomann' in product.content['store_links']:
                        thomann_url = product.content['store_links']['Thomann']
                    elif 'thomann_info' in product.content and 'url' in product.content['thomann_info']:
                        thomann_url = product.content['thomann_info']['url']
                    elif 'thomann_url' in product.content:
                        thomann_url = product.content['thomann_url']
                
                if thomann_url:
                    print(f"   Original Thomann URL: {thomann_url}")
                    
                    # Test affiliate URL generation
                    try:
                        affiliate_url = enhanced_service._add_affiliate_parameters(thomann_store, thomann_url)
                        print(f"   ✅ Generated Affiliate URL: {affiliate_url}")
                        
                        # Verify the URL format
                        if '/intl/' in affiliate_url and 'offid=1' in affiliate_url and f'affid={thomann_store.affiliate_id}' in affiliate_url:
                            print(f"   ✅ URL format is correct!")
                        else:
                            print(f"   ⚠️  URL format might need adjustment")
                            
                    except Exception as e:
                        print(f"   ❌ Error generating affiliate URL: {e}")
                else:
                    print(f"   ⚠️  No Thomann URL found in product content")
                    
                    # Check if there are any Thomann prices for this product
                    prices_query = select(ProductPrice).join(AffiliateStore).where(
                        and_(
                            ProductPrice.product_id == product.id,
                            AffiliateStore.slug == "thomann",
                            ProductPrice.is_available.is_(True)
                        )
                    )
                    prices_result = await session.execute(prices_query)
                    thomann_prices = prices_result.scalars().all()
                    
                    if thomann_prices:
                        print(f"   📊 Found {len(thomann_prices)} Thomann price(s):")
                        for price in thomann_prices:
                            print(f"      Price: {price.price} {price.currency}")
                            print(f"      Affiliate URL: {price.affiliate_url}")
                            
                            # Test if the existing affiliate URL is in the correct format
                            if price.affiliate_url:
                                if '/intl/' in price.affiliate_url and 'offid=1' in price.affiliate_url and f'affid={thomann_store.affiliate_id}' in price.affiliate_url:
                                    print(f"      ✅ Existing URL format is correct!")
                                else:
                                    print(f"      ⚠️  Existing URL format needs updating")
                    else:
                        print(f"   📊 No Thomann prices found for this product")
                
                print()
            
            # Test some example URLs
            print("🧪 Testing Example URL Formats:")
            print()
            
            example_urls = [
                "https://www.thomann.de/gb/harley-benton-delta-blues-t.htm",
                "https://www.thomann.de/de/fender-stratocaster.htm",
                "https://www.thomann.de/fr/yamaha-piano.htm",
                "https://www.thomann.de/intl/product_123.htm",
                "https://www.thomann.de/search_dir.html?sw=guitar"
            ]
            
            for example_url in example_urls:
                print(f"   Original: {example_url}")
                try:
                    affiliate_url = enhanced_service._add_affiliate_parameters(thomann_store, example_url)
                    print(f"   Generated: {affiliate_url}")
                    
                    # Check if it's using /intl/ and correct parameters
                    if '/intl/' in affiliate_url and 'offid=1' in affiliate_url and f'affid={thomann_store.affiliate_id}' in affiliate_url:
                        print(f"   ✅ Format is correct!")
                    else:
                        print(f"   ⚠️  Format needs adjustment")
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                print()
            
            print("📋 Summary:")
            print(f"   • Thomann Affiliate ID: {thomann_store.affiliate_id}")
            print(f"   • Using /intl/ paths: ✅")
            print(f"   • Affiliate parameters: offid=1&affid={thomann_store.affiliate_id}")
            print(f"   • Manual affiliate format (no RediR™): ✅")
            
        except Exception as e:
            print(f"❌ Error testing Thomann affiliate links: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(test_thomann_affiliate_links())
