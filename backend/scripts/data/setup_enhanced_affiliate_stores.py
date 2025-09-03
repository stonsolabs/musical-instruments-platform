#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append('.')

from app.database import get_async_session
from app.models import AffiliateStore, BrandExclusivity
from sqlalchemy.ext.asyncio import AsyncSession

async def setup_enhanced_affiliate_stores():
    """Set up enhanced affiliate stores with regional preferences and brand exclusivity"""
    
    async for session in get_async_session():
        try:
            print("Setting up Enhanced Affiliate Stores...")
            print("=" * 50)
            
            # Clear existing stores
            await session.execute("DELETE FROM brand_exclusivities")
            await session.execute("DELETE FROM affiliate_stores")
            await session.commit()
            
            # Create enhanced affiliate stores
            stores_data = [
                {
                    "name": "Thomann",
                    "slug": "thomann",
                    "website_url": "https://www.thomann.de",
                    "logo_url": "https://thumbs.static-thomann.de/thumb/original/pics/bdb/_58/585150/19376401_800.jpg",
                    "description": "Europe's largest online music store (uses RediR™ for regional redirects)",
                    "commission_rate": 5.0,
                    "has_affiliate_program": True,
                    "affiliate_id": "your-thomann-default-affiliate-id",
                    "domain_affiliate_ids": {
                        "DE": "your-thomann-de-affiliate-id",
                        "UK": "your-thomann-uk-affiliate-id",
                        "FR": "your-thomann-fr-affiliate-id",
                        "IT": "your-thomann-it-affiliate-id",
                        "ES": "your-thomann-es-affiliate-id",
                        "US": "your-thomann-us-affiliate-id"
                    },
                    "affiliate_parameters": {
                        "partner": "your-thomann-partner-id",
                        "redir": "1"  # Enable RediR™ redirect system
                    },
                    "show_affiliate_buttons": True,
                    "priority": 10,
                    "available_regions": ["EU", "UK", "DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH"],
                    "primary_region": "EU",
                    "regional_priority": {"EU": 10, "DE": 15, "UK": 8, "FR": 7, "IT": 6},
                    "use_store_fallback": True,
                    "store_fallback_url": "https://www.thomann.de/gb/search.html?sw=",
                },
                {
                    "name": "Amazon",
                    "slug": "amazon",
                    "website_url": "https://www.amazon.com",
                    "logo_url": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
                    "description": "Global e-commerce platform",
                    "commission_rate": 4.0,
                    "has_affiliate_program": True,
                    "affiliate_id": "your-amazon-default-affiliate-id",
                    "domain_affiliate_ids": {
                        "US": "your-amazon-us-affiliate-id",
                        "UK": "your-amazon-uk-affiliate-id",
                        "DE": "your-amazon-de-affiliate-id",
                        "FR": "your-amazon-fr-affiliate-id",
                        "IT": "your-amazon-it-affiliate-id",
                        "ES": "your-amazon-es-affiliate-id",
                        "CA": "your-amazon-ca-affiliate-id",
                        "JP": "your-amazon-jp-affiliate-id"
                    },
                    "affiliate_parameters": {"tag": "your-amazon-tag", "ref": "your-amazon-ref"},
                    "show_affiliate_buttons": True,
                    "priority": 5,
                    "available_regions": ["US", "UK", "DE", "FR", "IT", "ES", "CA", "JP"],
                    "primary_region": "US",
                    "regional_priority": {"US": 10, "UK": 8, "DE": 7, "CA": 6},
                    "use_store_fallback": True,
                    "store_fallback_url": "https://www.amazon.com/s?k=",
                },
                {
                    "name": "Gear4Music",
                    "slug": "gear4music",
                    "website_url": "https://www.gear4music.com",
                    "logo_url": "https://www.gear4music.com/media/logo.png",
                    "description": "UK-based music equipment retailer",
                    "commission_rate": 3.5,
                    "has_affiliate_program": True,
                    "affiliate_id": "your-gear4music-default-affiliate-id",
                    "domain_affiliate_ids": {
                        "UK": "your-gear4music-uk-affiliate-id",
                        "DE": "your-gear4music-de-affiliate-id",
                        "FR": "your-gear4music-fr-affiliate-id"
                    },
                    "affiliate_parameters": {"aff": "your-gear4music-aff-id"},
                    "show_affiliate_buttons": True,
                    "priority": 8,
                    "available_regions": ["UK", "EU"],
                    "primary_region": "UK",
                    "regional_priority": {"UK": 10, "EU": 5},
                    "use_store_fallback": True,
                    "store_fallback_url": "https://www.gear4music.com/search?search=",
                },
                {
                    "name": "Sweetwater",
                    "slug": "sweetwater",
                    "website_url": "https://www.sweetwater.com",
                    "logo_url": "https://www.sweetwater.com/images/logo.png",
                    "description": "US-based music equipment retailer",
                    "commission_rate": 4.5,
                    "has_affiliate_program": True,
                    "affiliate_id": "your-sweetwater-affiliate-id",
                    "affiliate_parameters": {"pkey": "your-sweetwater-pkey"},
                    "show_affiliate_buttons": True,
                    "priority": 7,
                    "available_regions": ["US"],
                    "primary_region": "US",
                    "regional_priority": {"US": 10},
                    "use_store_fallback": True,
                    "store_fallback_url": "https://www.sweetwater.com/c/search--",
                },
                {
                    "name": "Donner",
                    "slug": "donner",
                    "website_url": "https://www.donnerdeal.com",
                    "logo_url": "https://www.donnerdeal.com/logo.png",
                    "description": "Donner official store",
                    "commission_rate": 3.0,
                    "has_affiliate_program": True,
                    "affiliate_id": "your-donner-affiliate-id",
                    "affiliate_parameters": {"ref": "your-donner-ref"},
                    "show_affiliate_buttons": True,
                    "priority": 6,
                    "available_regions": ["US", "EU", "UK", "CA"],
                    "primary_region": "US",
                    "regional_priority": {"US": 10, "EU": 8, "UK": 7, "CA": 6},
                    "use_store_fallback": True,
                    "store_fallback_url": "https://www.donnerdeal.com/search?q=",
                },
                {
                    "name": "Guitar Center",
                    "slug": "guitarcenter",
                    "website_url": "https://www.guitarcenter.com",
                    "logo_url": "https://www.guitarcenter.com/logo.png",
                    "description": "US-based music equipment retailer",
                    "commission_rate": 4.0,
                    "has_affiliate_program": True,
                    "affiliate_id": "your-guitarcenter-affiliate-id",
                    "affiliate_parameters": {"ref": "your-guitarcenter-ref"},
                    "show_affiliate_buttons": True,
                    "priority": 4,
                    "available_regions": ["US"],
                    "primary_region": "US",
                    "regional_priority": {"US": 10},
                    "use_store_fallback": True,
                    "store_fallback_url": "https://www.guitarcenter.com/search?q=",
                },
            ]
            
            # Create stores
            stores = []
            for store_data in stores_data:
                store = AffiliateStore(**store_data)
                session.add(store)
                stores.append(store)
            
            await session.commit()
            
            # Get store IDs for brand exclusivity
            store_map = {store.slug: store.id for store in stores}
            
            # Set up brand exclusivity rules
            exclusivity_rules = [
                # Harley Benton is exclusive to Thomann
                {
                    "brand_name": "Harley Benton",
                    "store_slug": "thomann",
                    "is_exclusive": True,
                    "regions": None,  # All regions
                    "priority_boost": 50,
                },
                # Donner is exclusive to Donner store
                {
                    "brand_name": "Donner",
                    "store_slug": "donner",
                    "is_exclusive": True,
                    "regions": None,  # All regions
                    "priority_boost": 50,
                },
                # Sweetwater preferred for US brands
                {
                    "brand_name": "Fender",
                    "store_slug": "sweetwater",
                    "is_exclusive": False,
                    "regions": None,  # All regions (regional control is at store level)
                    "priority_boost": 20,
                },
                {
                    "brand_name": "Gibson",
                    "store_slug": "sweetwater",
                    "is_exclusive": False,
                    "regions": None,  # All regions (regional control is at store level)
                    "priority_boost": 20,
                },
                # Guitar Center preferred for US brands
                {
                    "brand_name": "Fender",
                    "store_slug": "guitarcenter",
                    "is_exclusive": False,
                    "regions": None,  # All regions (regional control is at store level)
                    "priority_boost": 15,
                },
                {
                    "brand_name": "Gibson",
                    "store_slug": "guitarcenter",
                    "is_exclusive": False,
                    "regions": None,  # All regions (regional control is at store level)
                    "priority_boost": 15,
                },
            ]
            
            # Create exclusivity rules
            for rule in exclusivity_rules:
                exclusivity = BrandExclusivity(
                    brand_name=rule["brand_name"],
                    store_id=store_map[rule["store_slug"]],
                    is_exclusive=rule["is_exclusive"],
                    regions=rule["regions"],
                    priority_boost=rule["priority_boost"],
                )
                session.add(exclusivity)
            
            await session.commit()
            
            print("✅ Enhanced affiliate stores created successfully!")
            print(f"   - {len(stores)} stores configured")
            print(f"   - {len(exclusivity_rules)} brand exclusivity rules set")
            
            print("\n📋 Store Configuration Summary:")
            for store in stores:
                print(f"   • {store.name}: {store.primary_region} (Priority: {store.priority})")
            
            print("\n🎯 Brand Exclusivity Rules:")
            for rule in exclusivity_rules:
                exclusivity_type = "EXCLUSIVE" if rule["is_exclusive"] else "PREFERRED"
                regions = "All regions" if not rule["regions"] else ", ".join(rule["regions"])
                print(f"   • {rule['brand_name']} → {rule['store_slug']} ({exclusivity_type}) - {regions}")
            
            print("\n⚠️  IMPORTANT: Update affiliate IDs in this script before running!")
            
        except Exception as e:
            print(f"❌ Error setting up enhanced affiliate stores: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(setup_enhanced_affiliate_stores())
