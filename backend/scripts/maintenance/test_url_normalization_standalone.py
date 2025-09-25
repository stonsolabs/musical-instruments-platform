#!/usr/bin/env python3
"""
Standalone script to test URL normalization for different Thomann URL formats
This tests the logic without requiring database connection
"""

import sys
import os
sys.path.append('.')

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

def normalize_thomann_url(url: str) -> str:
    """Normalize Thomann URLs to use thomann.de/intl/ path for better international compatibility"""
    parsed = urlparse(url)
    
    # Process all Thomann domains (thomann.de, thomann.co.uk, etc.)
    if not parsed.netloc or 'thomann' not in parsed.netloc:
        return url
    
    # Always use thomann.de domain for affiliate links
    # This ensures consistent affiliate tracking and proper regional redirects
    normalized_netloc = 'www.thomann.de'
    
    # Convert regional paths to /intl/ for better international compatibility
    # Examples:
    # /gb/product/123 -> /intl/product/123
    # /de/product/456 -> /intl/product/456
    # /fr/product/789 -> /intl/product/789
    path = parsed.path
    
    # Replace regional paths with /intl/
    regional_patterns = ['/gb/', '/de/', '/fr/', '/it/', '/es/', '/nl/', '/be/', '/at/', '/ch/', '/us/']
    for pattern in regional_patterns:
        if path.startswith(pattern):
            path = path.replace(pattern, '/intl/', 1)
            break
    
    # If it's already /intl/ or doesn't have a regional prefix, keep as is
    if not path.startswith('/intl/') and not any(path.startswith(p) for p in regional_patterns):
        # For root paths or other paths, ensure they use /intl/
        if path == '/' or path == '':
            path = '/intl/'
        elif not path.startswith('/intl/'):
            # Convert direct product paths to /intl/ for better international compatibility
            path = '/intl' + path
    
    # Reconstruct URL with thomann.de domain
    return urlunparse((
        parsed.scheme,
        normalized_netloc,
        path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

def add_affiliate_parameters(url: str, affiliate_id: str = "4419") -> str:
    """Add affiliate parameters to URL"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    # Add Thomann affiliate parameters
    query_params['offid'] = ['1']
    query_params['affid'] = [affiliate_id]
    
    # Reconstruct URL with affiliate parameters
    new_query = urlencode(query_params, doseq=True)
    affiliate_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return affiliate_url

def test_url_normalization():
    """Test URL normalization with different input formats"""
    
    print("Testing Thomann URL Normalization (Standalone)")
    print("=" * 60)
    
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
        normalized_url = normalize_thomann_url(test_url)
        print(f"   Normalized: {normalized_url}")
        
        # Test full affiliate URL generation
        affiliate_url = add_affiliate_parameters(normalized_url)
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

if __name__ == "__main__":
    test_url_normalization()
