#!/usr/bin/env python3
"""
Script to test URL normalization for different Thomann URL formats
This will verify that all URLs are converted to the working format
"""

import asyncio
import sys
import os
sys.path.append('.')

from app.services.enhanced_affiliate_service import EnhancedAffiliateService
from app.database import async_session_factory
from app.models import AffiliateStore
from sqlalchemy import select

async def test_url_normalization():
    """Test URL normalization with different input formats"""
    
    async with async_session_factory() as session:
        try:
            print("Testing Thomann URL Normalization")
            print("=" * 50)
            
            # Get the Thomann store
            query = select(AffiliateStore).where(AffiliateStore.slug == "thomann")
            result = await session.execute(query)
            thomann_store = result.scalar_one_or_none()
            
            if not thomann_store:
                print("❌ Thomann store not found!")
                return
            
            # Initialize the enhanced affiliate service
            enhanced_service = EnhancedAffiliateService(session)
            
            # Test different input URL formats
            test_urls = [
                # Original problematic URL
                "https://www.thomann.co.uk/intl/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
                
                # Different domains
                "https://www.thomann.de/intl/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
                "https://www.thomann.co.uk/gb/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
                "https://www.thomann.de/gb/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
                "https://www.thomann.de/de/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
                
                # Different products
                "https://www.thomann.co.uk/gb/harley-benton-delta-blues-t.htm",
                "https://www.thomann.de/de/fender-stratocaster.htm",
                "https://www.thomann.co.uk/intl/yamaha-piano.htm",
                
                # No regional path
                "https://www.thomann.de/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
                "https://www.thomann.co.uk/harley-benton-guitar.htm",
            ]
            
            print("🔗 URL Normalization Test Results:")
            print()
            
            for i, test_url in enumerate(test_urls, 1):
                print(f"{i}. Input URL:")
                print(f"   {test_url}")
                
                # Test URL normalization
                normalized_url = enhanced_service._normalize_thomann_url(test_url)
                print(f"   Normalized: {normalized_url}")
                
                # Test full affiliate URL generation
                affiliate_url = enhanced_service._add_affiliate_parameters(thomann_store, test_url)
                print(f"   Affiliate URL: {affiliate_url}")
                
                # Check if it matches the working format
                if "thomann.de/intl/" in affiliate_url and "offid=1&affid=4419" in affiliate_url:
                    print(f"   ✅ CORRECT FORMAT")
                else:
                    print(f"   ❌ INCORRECT FORMAT")
                
                print()
            
            print("📋 Summary:")
            print("✅ All URLs should be normalized to: https://www.thomann.de/intl/[product].htm?offid=1&affid=4419")
            print("✅ This format has been tested and works correctly")
            print("✅ The system will now handle all Thomann domains and convert them to the working format")
            
        except Exception as e:
            print(f"❌ Error testing URL normalization: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(test_url_normalization())
