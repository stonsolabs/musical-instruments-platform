#!/usr/bin/env python3
"""
Script to enable RediR™ for Thomann affiliate links
This updates the existing Thomann store configuration to include the redir=1 parameter
"""

import asyncio
import sys
import os
sys.path.append('.')

from app.database import async_session_factory
from app.models import AffiliateStore
from sqlalchemy import select

async def enable_thomann_redir():
    """Enable RediR™ for Thomann affiliate links"""
    
    async with async_session_factory() as session:
        try:
            print("Enabling RediR™ for Thomann affiliate links...")
            print("=" * 50)
            
            # Get the Thomann store
            query = select(AffiliateStore).where(AffiliateStore.slug == "thomann")
            result = await session.execute(query)
            thomann_store = result.scalar_one_or_none()
            
            if not thomann_store:
                print("❌ Thomann store not found in database!")
                return
            
            print(f"📦 Found Thomann store: {thomann_store.name}")
            print(f"   Current affiliate parameters: {thomann_store.affiliate_parameters}")
            
            # Update affiliate parameters to include RediR™
            if not thomann_store.affiliate_parameters:
                thomann_store.affiliate_parameters = {}
            
            # Add RediR™ parameter
            thomann_store.affiliate_parameters["redir"] = "1"
            
            # Ensure we have the correct affiliate parameters
            if "offid" not in thomann_store.affiliate_parameters:
                thomann_store.affiliate_parameters["offid"] = "1"
            
            if "affid" not in thomann_store.affiliate_parameters:
                thomann_store.affiliate_parameters["affid"] = thomann_store.affiliate_id
            
            # Update website URL to use /intl/ for better international compatibility
            if not thomann_store.website_url.endswith('/intl'):
                thomann_store.website_url = "https://www.thomann.de/intl"
            
            # Update fallback URL to use /intl/
            if thomann_store.store_fallback_url and '/gb/' in thomann_store.store_fallback_url:
                thomann_store.store_fallback_url = thomann_store.store_fallback_url.replace('/gb/', '/intl/')
            
            await session.commit()
            
            print("✅ RediR™ enabled successfully!")
            print(f"   Updated affiliate parameters: {thomann_store.affiliate_parameters}")
            print(f"   Website URL: {thomann_store.website_url}")
            print(f"   Fallback URL: {thomann_store.store_fallback_url}")
            
            print("\n🔗 RediR™ Benefits:")
            print("   • Automatic regional redirects to user's local Thomann store")
            print("   • Better conversion rates with localized experience")
            print("   • Simplified affiliate link management")
            print("   • Support for all Thomann regional domains")
            
            print("\n📋 Regional Domains Supported:")
            print("   • thomann.de (Germany)")
            print("   • thomann.co.uk (United Kingdom)")
            print("   • thomann.fr (France)")
            print("   • thomann.it (Italy)")
            print("   • thomann.es (Spain)")
            print("   • thomann.nl (Netherlands)")
            print("   • thomann.be (Belgium)")
            print("   • thomann.at (Austria)")
            print("   • thomann.ch (Switzerland)")
            print("   • And more...")
            
        except Exception as e:
            print(f"❌ Error enabling RediR™: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(enable_thomann_redir())
