#!/usr/bin/env python3
"""
Script to update Thomann store configuration to use manual affiliate format
This updates the existing Thomann store to use /intl/ paths and correct affiliate parameters
without requiring RediR™
"""

import asyncio
import sys
import os
sys.path.append('.')

from app.database import async_session_factory
from app.models import AffiliateStore
from sqlalchemy import select

async def update_thomann_manual_affiliate():
    """Update Thomann store to use manual affiliate format with /intl/ paths"""
    
    async with async_session_factory() as session:
        try:
            print("Updating Thomann store to use manual affiliate format...")
            print("=" * 60)
            
            # Get the Thomann store
            query = select(AffiliateStore).where(AffiliateStore.slug == "thomann")
            result = await session.execute(query)
            thomann_store = result.scalar_one_or_none()
            
            if not thomann_store:
                print("❌ Thomann store not found in database!")
                return
            
            print(f"📦 Found Thomann store: {thomann_store.name}")
            print(f"   Current affiliate parameters: {thomann_store.affiliate_parameters}")
            print(f"   Current website URL: {thomann_store.website_url}")
            print(f"   Current fallback URL: {thomann_store.store_fallback_url}")
            
            # Update affiliate parameters to use manual format
            if not thomann_store.affiliate_parameters:
                thomann_store.affiliate_parameters = {}
            
            # Set correct affiliate parameters for manual format
            thomann_store.affiliate_parameters["offid"] = "1"
            thomann_store.affiliate_parameters["affid"] = thomann_store.affiliate_id
            
            # Remove RediR™ parameter if it exists
            if "redir" in thomann_store.affiliate_parameters:
                del thomann_store.affiliate_parameters["redir"]
                print("   ✅ Removed RediR™ parameter")
            
            # Update website URL to use /intl/ for better international compatibility
            thomann_store.website_url = "https://www.thomann.de/intl"
            print("   ✅ Updated website URL to use /intl/")
            
            # Update fallback URL to use /intl/
            if thomann_store.store_fallback_url:
                if '/gb/' in thomann_store.store_fallback_url:
                    thomann_store.store_fallback_url = thomann_store.store_fallback_url.replace('/gb/', '/intl/')
                elif not '/intl/' in thomann_store.store_fallback_url:
                    thomann_store.store_fallback_url = "https://www.thomann.de/intl/search_dir.html?sw="
                print("   ✅ Updated fallback URL to use /intl/")
            
            await session.commit()
            
            print("\n✅ Thomann store updated successfully!")
            print(f"   Updated affiliate parameters: {thomann_store.affiliate_parameters}")
            print(f"   Website URL: {thomann_store.website_url}")
            print(f"   Fallback URL: {thomann_store.store_fallback_url}")
            
            print("\n🔗 Manual Affiliate Format Benefits:")
            print("   • Uses /intl/ paths for automatic regional display")
            print("   • No RediR™ account required")
            print("   • Correct affiliate parameters: offid=1&affid=4419")
            print("   • Automatic localization based on user's location")
            print("   • Compatible with all Thomann regional domains")
            
            print("\n📋 Example Affiliate URLs:")
            print("   • Product: https://www.thomann.de/intl/product_123.htm?offid=1&affid=4419")
            print("   • Search: https://www.thomann.de/intl/search_dir.html?sw=harley+benton&offid=1&affid=4419")
            print("   • Homepage: https://www.thomann.de/intl/index.html?offid=1&affid=4419")
            
            print("\n🌍 Regional Display:")
            print("   • /intl/ automatically shows the correct regional website")
            print("   • Users see prices in their local currency")
            print("   • Regional shipping and delivery options")
            print("   • Localized customer support")
            
        except Exception as e:
            print(f"❌ Error updating Thomann store: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(update_thomann_manual_affiliate())
