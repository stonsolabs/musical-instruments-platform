#!/usr/bin/env python3
"""
Script to generate multiple variations of Thomann affiliate URLs for testing
This will help identify which URL format works correctly
"""

import asyncio
import sys
import os
sys.path.append('.')

from app.database import async_session_factory
from app.models import AffiliateStore
from app.services.enhanced_affiliate_service import EnhancedAffiliateService
from sqlalchemy import select

async def test_thomann_url_variations():
    """Generate multiple variations of Thomann URLs for testing"""
    
    # Example product URL from your test
    original_url = "https://www.thomann.co.uk/intl/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm"
    
    print("Testing Thomann URL Variations")
    print("=" * 60)
    print(f"Original URL: {original_url}")
    print()
    
    # Test different variations
    test_variations = [
        # 1. Original with /intl/ path
        {
            "name": "Original with /intl/",
            "url": "https://www.thomann.co.uk/intl/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
            "affiliate_id": "4419"
        },
        
        # 2. German domain with /intl/
        {
            "name": "German domain with /intl/",
            "url": "https://www.thomann.de/intl/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
            "affiliate_id": "4419"
        },
        
        # 3. UK domain with /gb/ path
        {
            "name": "UK domain with /gb/",
            "url": "https://www.thomann.co.uk/gb/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
            "affiliate_id": "4419"
        },
        
        # 4. German domain with /de/ path
        {
            "name": "German domain with /de/",
            "url": "https://www.thomann.de/de/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
            "affiliate_id": "4419"
        },
        
        # 5. German domain with /gb/ path (international)
        {
            "name": "German domain with /gb/",
            "url": "https://www.thomann.de/gb/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
            "affiliate_id": "4419"
        },
        
        # 6. No regional path
        {
            "name": "No regional path",
            "url": "https://www.thomann.de/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
            "affiliate_id": "4419"
        },
        
        # 7. Different affiliate parameter format
        {
            "name": "Different affiliate format",
            "url": "https://www.thomann.de/intl/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
            "affiliate_id": "4419",
            "custom_params": {"partner": "4419", "offid": "1"}
        },
        
        # 8. Alternative affiliate ID format
        {
            "name": "Alternative affiliate format",
            "url": "https://www.thomann.de/intl/charvel_pm_bass_sd_pj_iv_mah_sfrd.htm",
            "affiliate_id": "4419",
            "custom_params": {"partner_id": "4419"}
        },
    ]
    
    print("🔗 Generated Affiliate URL Variations:")
    print()
    
    for i, variation in enumerate(test_variations, 1):
        print(f"{i}. {variation['name']}")
        print(f"   Base URL: {variation['url']}")
        
        # Generate affiliate URL
        if "custom_params" in variation:
            # Manual parameter construction
            params = []
            for key, value in variation["custom_params"].items():
                params.append(f"{key}={value}")
            affiliate_url = f"{variation['url']}?{'&'.join(params)}"
        else:
            # Standard affiliate parameters
            affiliate_url = f"{variation['url']}?offid=1&affid={variation['affiliate_id']}"
        
        print(f"   Affiliate URL: {affiliate_url}")
        print()
    
    print("🧪 Additional Test Variations:")
    print()
    
    # Test with different product URLs
    test_products = [
        "https://www.thomann.de/intl/harley-benton-delta-blues-t.htm",
        "https://www.thomann.de/intl/fender-stratocaster.htm",
        "https://www.thomann.de/intl/yamaha-piano.htm",
        "https://www.thomann.de/gb/harley-benton-delta-blues-t.htm",
        "https://www.thomann.de/de/harley-benton-delta-blues-t.htm",
    ]
    
    for i, product_url in enumerate(test_products, 1):
        print(f"Product {i}: {product_url}")
        affiliate_url = f"{product_url}?offid=1&affid=4419"
        print(f"Affiliate: {affiliate_url}")
        print()
    
    print("📋 Testing Instructions:")
    print("1. Copy each affiliate URL above")
    print("2. Test them in your browser")
    print("3. Check which ones work correctly")
    print("4. Note which format redirects properly")
    print("5. Report back which variation works best")
    print()
    
    print("🔍 What to Look For:")
    print("• Does the URL load the product page?")
    print("• Does it redirect to the correct regional domain?")
    print("• Are the affiliate parameters preserved?")
    print("• Does the product exist on the page?")
    print()
    
    print("💡 Common Issues:")
    print("• /intl/ might not work for all products")
    print("• Some products might only exist on specific regional domains")
    print("• Affiliate parameters might need different format")
    print("• Product URLs might need different path structure")

if __name__ == "__main__":
    asyncio.run(test_thomann_url_variations())
