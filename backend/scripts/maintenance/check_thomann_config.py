#!/usr/bin/env python3
"""
Script to check the current Thomann configuration in the database
This will show what affiliate ID and parameters are currently set
"""

import asyncio
import sys
import os
sys.path.append('.')

from app.database import async_session_factory
from app.models import AffiliateStore
from sqlalchemy import select

async def check_thomann_config():
    """Check current Thomann configuration"""
    
    async with async_session_factory() as session:
        try:
            print("Checking Current Thomann Configuration")
            print("=" * 50)
            
            # Get the Thomann store
            query = select(AffiliateStore).where(AffiliateStore.slug == "thomann")
            result = await session.execute(query)
            thomann_store = result.scalar_one_or_none()
            
            if not thomann_store:
                print("❌ Thomann store not found in database!")
                return
            
            print(f"📦 Thomann Store Details:")
            print(f"   ID: {thomann_store.id}")
            print(f"   Name: {thomann_store.name}")
            print(f"   Slug: {thomann_store.slug}")
            print(f"   Website URL: {thomann_store.website_url}")
            print(f"   Logo URL: {thomann_store.logo_url}")
            print(f"   Description: {thomann_store.description}")
            print(f"   Commission Rate: {thomann_store.commission_rate}%")
            print(f"   Is Active: {thomann_store.is_active}")
            print(f"   Has Affiliate Program: {thomann_store.has_affiliate_program}")
            print(f"   Show Affiliate Buttons: {thomann_store.show_affiliate_buttons}")
            print(f"   Priority: {thomann_store.priority}")
            print()
            
            print(f"🔗 Affiliate Configuration:")
            print(f"   Affiliate ID: {thomann_store.affiliate_id}")
            print(f"   Affiliate Base URL: {thomann_store.affiliate_base_url}")
            print(f"   Domain Affiliate IDs: {thomann_store.domain_affiliate_ids}")
            print(f"   Affiliate Parameters: {thomann_store.affiliate_parameters}")
            print()
            
            print(f"🌍 Regional Configuration:")
            print(f"   Available Regions: {thomann_store.available_regions}")
            print(f"   Primary Region: {thomann_store.primary_region}")
            print(f"   Regional Priority: {thomann_store.regional_priority}")
            print()
            
            print(f"🔄 Fallback Configuration:")
            print(f"   Use Store Fallback: {thomann_store.use_store_fallback}")
            print(f"   Store Fallback URL: {thomann_store.store_fallback_url}")
            print()
            
            # Check if configuration looks correct
            print("✅ Configuration Check:")
            
            issues = []
            
            if not thomann_store.affiliate_id:
                issues.append("❌ No affiliate ID set")
            else:
                print(f"   ✅ Affiliate ID: {thomann_store.affiliate_id}")
            
            if not thomann_store.affiliate_parameters:
                issues.append("❌ No affiliate parameters set")
            else:
                print(f"   ✅ Affiliate parameters: {thomann_store.affiliate_parameters}")
                
                # Check for required parameters
                if "offid" not in thomann_store.affiliate_parameters:
                    issues.append("❌ Missing 'offid' parameter")
                else:
                    print(f"   ✅ offid parameter: {thomann_store.affiliate_parameters['offid']}")
                
                if "affid" not in thomann_store.affiliate_parameters:
                    issues.append("❌ Missing 'affid' parameter")
                else:
                    print(f"   ✅ affid parameter: {thomann_store.affiliate_parameters['affid']}")
                
                # Check if affid matches affiliate_id
                if thomann_store.affiliate_parameters.get("affid") != thomann_store.affiliate_id:
                    issues.append("❌ affid parameter doesn't match affiliate_id")
                else:
                    print(f"   ✅ affid matches affiliate_id")
            
            if not thomann_store.website_url or "/intl" not in thomann_store.website_url:
                issues.append("❌ Website URL should use /intl/ path")
            else:
                print(f"   ✅ Website URL uses /intl/ path")
            
            if thomann_store.store_fallback_url and "/intl" not in thomann_store.store_fallback_url:
                issues.append("❌ Fallback URL should use /intl/ path")
            else:
                print(f"   ✅ Fallback URL uses /intl/ path")
            
            print()
            
            if issues:
                print("⚠️  Issues Found:")
                for issue in issues:
                    print(f"   {issue}")
                print()
                print("💡 To fix these issues, run:")
                print("   python scripts/maintenance/update_thomann_existing_config.py")
            else:
                print("🎉 Configuration looks good!")
                print("   All required parameters are set correctly.")
            
            print()
            print("📋 Example URLs that would be generated:")
            if thomann_store.affiliate_id:
                print(f"   Product: https://www.thomann.de/intl/product_123.htm?offid=1&affid={thomann_store.affiliate_id}")
                print(f"   Search: https://www.thomann.de/intl/search_dir.html?sw=guitar&offid=1&affid={thomann_store.affiliate_id}")
                print(f"   Homepage: https://www.thomann.de/intl/index.html?offid=1&affid={thomann_store.affiliate_id}")
            
        except Exception as e:
            print(f"❌ Error checking Thomann configuration: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(check_thomann_config())
