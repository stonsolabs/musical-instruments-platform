#!/usr/bin/env python3
"""
Script to update existing Thomann store configuration to use manual affiliate format
This script reads the current Thomann configuration from the database and updates it
to use /intl/ paths and correct affiliate parameters while preserving the existing affiliate ID
"""

import asyncio
import sys
import os
sys.path.append('.')

from app.database import async_session_factory
from app.models import AffiliateStore
from sqlalchemy import select

async def update_thomann_existing_config():
    """Update existing Thomann store to use manual affiliate format with /intl/ paths"""
    
    async with async_session_factory() as session:
        try:
            print("Updating existing Thomann store configuration...")
            print("=" * 60)
            
            # Get the Thomann store
            query = select(AffiliateStore).where(AffiliateStore.slug == "thomann")
            result = await session.execute(query)
            thomann_store = result.scalar_one_or_none()
            
            if not thomann_store:
                print("❌ Thomann store not found in database!")
                print("   Please run the setup script first or check your database connection.")
                return
            
            print(f"📦 Found Thomann store: {thomann_store.name}")
            print(f"   Current affiliate ID: {thomann_store.affiliate_id}")
            print(f"   Current affiliate parameters: {thomann_store.affiliate_parameters}")
            print(f"   Current website URL: {thomann_store.website_url}")
            print(f"   Current fallback URL: {thomann_store.store_fallback_url}")
            
            # Preserve the existing affiliate ID
            existing_affiliate_id = thomann_store.affiliate_id
            if not existing_affiliate_id:
                print("❌ No affiliate ID found in current configuration!")
                print("   Please set the affiliate_id field in the database first.")
                return
            
            print(f"✅ Using existing affiliate ID: {existing_affiliate_id}")
            
            # Update affiliate parameters to use manual format
            if not thomann_store.affiliate_parameters:
                thomann_store.affiliate_parameters = {}
            
            # Set correct affiliate parameters for manual format using existing ID
            thomann_store.affiliate_parameters["offid"] = "1"
            thomann_store.affiliate_parameters["affid"] = existing_affiliate_id
            
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
            
            # Update domain-specific affiliate IDs to use the existing affiliate ID
            if thomann_store.domain_affiliate_ids:
                for region in thomann_store.domain_affiliate_ids:
                    thomann_store.domain_affiliate_ids[region] = existing_affiliate_id
                print("   ✅ Updated domain-specific affiliate IDs")
            
            await session.commit()
            
            print("\n✅ Thomann store updated successfully!")
            print(f"   Preserved affiliate ID: {existing_affiliate_id}")
            print(f"   Updated affiliate parameters: {thomann_store.affiliate_parameters}")
            print(f"   Website URL: {thomann_store.website_url}")
            print(f"   Fallback URL: {thomann_store.store_fallback_url}")
            
            print("\n🔗 Manual Affiliate Format Benefits:")
            print("   • Uses /intl/ paths for automatic regional display")
            print("   • No RediR™ account required")
            print(f"   • Correct affiliate parameters: offid=1&affid={existing_affiliate_id}")
            print("   • Automatic localization based on user's location")
            print("   • Compatible with all Thomann regional domains")
            
            print("\n📋 Example Affiliate URLs:")
            print(f"   • Product: https://www.thomann.de/intl/product_123.htm?offid=1&affid={existing_affiliate_id}")
            print(f"   • Search: https://www.thomann.de/intl/search_dir.html?sw=harley+benton&offid=1&affid={existing_affiliate_id}")
            print(f"   • Homepage: https://www.thomann.de/intl/index.html?offid=1&affid={existing_affiliate_id}")
            
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
    asyncio.run(update_thomann_existing_config())
