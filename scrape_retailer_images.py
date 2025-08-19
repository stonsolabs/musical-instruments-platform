#!/usr/bin/env python3
"""
Script to scrape real product images from music retailers like Thomann and Gear4Music
for musical instruments and replace placeholder images.
"""

import os
import requests
import json
import time
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

# Directory containing the product images
PRODUCT_IMAGES_DIR = "./frontend/public/product-images"

# Real product URLs from music retailers
RETAILER_PRODUCT_URLS = {
    "boss_ds1_distortion": [
        "https://www.thomann.de/gb/boss_ds_1_distortion.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Boss-DS-1-Distortion-Pedal/6QC",
        "https://www.andertons.co.uk/boss-ds-1-distortion-pedal",
        "https://www.sweetwater.com/store/detail/DS1--boss-ds-1-distortion-pedal"
    ],
    "casio_px560_bk": [
        "https://www.thomann.de/gb/casio_px_560_bk.htm",
        "https://www.gear4music.com/Pianos-and-Keyboards/Casio-PX-560-Digital-Piano-Black/1QYZ",
        "https://www.andertons.co.uk/casio-px-560-digital-piano-black",
        "https://www.sweetwater.com/store/detail/PX560BK--casio-px-560-digital-piano-black"
    ],
    "electro_harmonix_big_muff": [
        "https://www.thomann.de/gb/electro_harmonix_big_muff_pi.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Electro-Harmonix-Big-Muff-Pi-Distortion-Sustain-Pedal/5QT",
        "https://www.andertons.co.uk/electro-harmonix-big-muff-pi-distortion-pedal",
        "https://www.sweetwater.com/store/detail/BigMuffPi--electro-harmonix-big-muff-pi-distortion-fuzz-pedal"
    ],
    "fender_player_jazz_bass": [
        "https://www.thomann.de/gb/fender_player_jazz_bass_pf_3ts.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Fender-Player-Jazz-Bass-3-Colour-Sunburst-Pau-Ferro/2ZYX",
        "https://www.andertons.co.uk/fender-player-jazz-bass-pau-ferro-fretboard-3-colour-sunburst",
        "https://www.sweetwater.com/store/detail/JBassPlr3TS--fender-player-jazz-bass-3-color-sunburst-with-pau-ferro-fingerboard"
    ],
    "fender_player_strat_sss": [
        "https://www.thomann.de/gb/fender_player_strat_pf_pwt.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Fender-Player-Stratocaster-Polar-White-Pau-Ferro/2ZYW",
        "https://www.andertons.co.uk/fender-player-stratocaster-pau-ferro-fretboard-polar-white",
        "https://www.sweetwater.com/store/detail/StratPlrPWT--fender-player-stratocaster-polar-white-with-pau-ferro-fingerboard"
    ],
    "fender_rumble_40_v3": [
        "https://www.thomann.de/gb/fender_rumble_40_v3.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Fender-Rumble-40-V3-Bass-Combo-Amplifier/1VKZ",
        "https://www.andertons.co.uk/fender-rumble-40-v3-bass-combo-amplifier",
        "https://www.sweetwater.com/store/detail/Rumble40V3--fender-rumble-40-v3-40-watt-1x10-bass-combo"
    ],
    "focusrite_scarlett_2i2_3rd": [
        "https://www.thomann.de/gb/focusrite_scarlett_2i2_3rd_gen.htm",
        "https://www.gear4music.com/Recording-and-Computers/Focusrite-Scarlett-2i2-3rd-Gen-USB-Audio-Interface/2YKV",
        "https://www.andertons.co.uk/focusrite-scarlett-2i2-3rd-gen-usb-audio-interface",
        "https://www.sweetwater.com/store/detail/Scarlet2i2G3--focusrite-scarlett-2i2-3rd-gen-usb-audio-interface"
    ],
    "gibson_les_paul_studio_eb": [
        "https://www.thomann.de/gb/gibson_les_paul_studio_eb_2019.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Gibson-Les-Paul-Studio-Ebony/3QYX",
        "https://www.andertons.co.uk/gibson-les-paul-studio-ebony",
        "https://www.sweetwater.com/store/detail/LPST00EBCH--gibson-les-paul-studio-ebony"
    ],
    "ibanez_sr300e_pw": [
        "https://www.thomann.de/gb/ibanez_sr300e_pw.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Ibanez-SR300E-Bass-Guitar-Pearl-White/1ZMX",
        "https://www.andertons.co.uk/ibanez-sr300e-4-string-bass-guitar-pearl-white",
        "https://www.sweetwater.com/store/detail/SR300EPW--ibanez-sr300e-4-string-electric-bass-pearl-white"
    ],
    "marshall_dsl40cr": [
        "https://www.thomann.de/gb/marshall_dsl40cr.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Marshall-DSL40CR-40W-Valve-Guitar-Combo-Amplifier/1XKY",
        "https://www.andertons.co.uk/marshall-dsl40cr-40-watt-valve-combo-amplifier",
        "https://www.sweetwater.com/store/detail/DSL40CR--marshall-dsl40cr-40-watt-1x12-tube-combo"
    ],
    "martin_d28_std": [
        "https://www.thomann.de/gb/martin_guitars_d_28_standard.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Martin-D-28-Standard-Acoustic-Guitar/2VKX",
        "https://www.andertons.co.uk/martin-d-28-standard-acoustic-guitar",
        "https://www.sweetwater.com/store/detail/D28--martin-d-28-standard-series-dreadnought-acoustic-guitar"
    ],
    "numark_party_mix": [
        "https://www.thomann.de/gb/numark_party_mix.htm",
        "https://www.gear4music.com/DJ/Numark-Party-Mix-DJ-Controller/2WKY",
        "https://www.andertons.co.uk/numark-party-mix-dj-controller",
        "https://www.sweetwater.com/store/detail/PartyMix--numark-party-mix-dj-controller-with-built-in-light-show"
    ],
    "pearl_export_exx725sp": [
        "https://www.thomann.de/gb/pearl_export_standard_725_smokey_chrome.htm",
        "https://www.gear4music.com/Drums-and-Percussion/Pearl-Export-EXX725SP-C31-5-Piece-Drum-Kit-Smokey-Chrome/3VLZ",
        "https://www.andertons.co.uk/pearl-export-exx725sp-c31-5-piece-drum-kit-smokey-chrome",
        "https://www.sweetwater.com/store/detail/EXX725SPC31--pearl-export-exx-5-piece-drum-set-smokey-chrome"
    ],
    "pioneer_ddj_sb3": [
        "https://www.thomann.de/gb/pioneer_dj_ddj_sb3.htm",
        "https://www.gear4music.com/DJ/Pioneer-DDJ-SB3-DJ-Controller/2XLY",
        "https://www.andertons.co.uk/pioneer-ddj-sb3-serato-dj-controller",
        "https://www.sweetwater.com/store/detail/DDJSB3--pioneer-dj-ddj-sb3-serato-dj-lite-controller"
    ],
    "roland_td17kv": [
        "https://www.thomann.de/gb/roland_td_17kv_v_drums.htm",
        "https://www.gear4music.com/Drums-and-Percussion/Roland-TD-17KV-V-Drums-Electronic-Drum-Kit/2YMZ",
        "https://www.andertons.co.uk/roland-td-17kv-v-drums-electronic-drum-kit",
        "https://www.sweetwater.com/store/detail/TD17KV--roland-td-17kv-v-drums-electronic-drum-set"
    ],
    "shure_sm57_lc": [
        "https://www.thomann.de/gb/shure_sm57_lc.htm",
        "https://www.gear4music.com/Recording-and-Computers/Shure-SM57-LC-Cardioid-Dynamic-Microphone/VKX",
        "https://www.andertons.co.uk/shure-sm57-lc-cardioid-dynamic-microphone",
        "https://www.sweetwater.com/store/detail/SM57--shure-sm57-cardioid-dynamic-microphone"
    ],
    "yamaha_fg830_nat": [
        "https://www.thomann.de/gb/yamaha_fg830_nt.htm",
        "https://www.gear4music.com/Guitar-and-Bass/Yamaha-FG830-Acoustic-Guitar-Natural/1WLX",
        "https://www.andertons.co.uk/yamaha-fg830-acoustic-guitar-natural",
        "https://www.sweetwater.com/store/detail/FG830NT--yamaha-fg830-acoustic-guitar-natural"
    ],
    "yamaha_p125_bk": [
        "https://www.thomann.de/gb/yamaha_p_125_bk.htm",
        "https://www.gear4music.com/Pianos-and-Keyboards/Yamaha-P-125-Digital-Piano-Black/2XMY",
        "https://www.andertons.co.uk/yamaha-p-125-digital-piano-black",
        "https://www.sweetwater.com/store/detail/P125B--yamaha-p-125-88-key-weighted-action-digital-piano-black"
    ]
}

def get_session():
    """Create a session with proper headers"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })
    return session

def scrape_thomann_images(url, session):
    """Scrape product images from Thomann"""
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find product images on Thomann
        image_urls = []
        
        # Try different selectors for Thomann product images
        selectors = [
            'img[data-src*="product"]',
            'img.product-image',
            'img[src*="product"]',
            '.product-gallery img',
            '.image-gallery img'
        ]
        
        for selector in selectors:
            images = soup.select(selector)
            for img in images:
                src = img.get('data-src') or img.get('src')
                if src and ('product' in src.lower() or 'item' in src.lower()):
                    # Convert relative URLs to absolute
                    full_url = urljoin(url, src)
                    if full_url not in image_urls:
                        image_urls.append(full_url)
        
        return image_urls[:4]  # Return max 4 images
        
    except Exception as e:
        print(f"   ❌ Error scraping Thomann: {e}")
        return []

def scrape_gear4music_images(url, session):
    """Scrape product images from Gear4Music"""
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find product images on Gear4Music
        image_urls = []
        
        # Try different selectors for Gear4Music product images
        selectors = [
            'img[data-src*="product"]',
            'img.product-image',
            'img[src*="product"]',
            '.product-gallery img',
            '.image-gallery img',
            '.product-images img'
        ]
        
        for selector in selectors:
            images = soup.select(selector)
            for img in images:
                src = img.get('data-src') or img.get('src')
                if src and ('product' in src.lower() or 'item' in src.lower()):
                    # Convert relative URLs to absolute
                    full_url = urljoin(url, src)
                    if full_url not in image_urls:
                        image_urls.append(full_url)
        
        return image_urls[:4]  # Return max 4 images
        
    except Exception as e:
        print(f"   ❌ Error scraping Gear4Music: {e}")
        return []

def scrape_andertons_images(url, session):
    """Scrape product images from Andertons"""
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find product images on Andertons
        image_urls = []
        
        # Try different selectors for Andertons product images
        selectors = [
            'img[data-src*="product"]',
            'img.product-image',
            'img[src*="product"]',
            '.product-gallery img',
            '.image-gallery img',
            '.product-images img'
        ]
        
        for selector in selectors:
            images = soup.select(selector)
            for img in images:
                src = img.get('data-src') or img.get('src')
                if src and ('product' in src.lower() or 'item' in src.lower() or 'media' in src.lower()):
                    # Convert relative URLs to absolute
                    full_url = urljoin(url, src)
                    if full_url not in image_urls:
                        image_urls.append(full_url)
        
        return image_urls[:4]  # Return max 4 images
        
    except Exception as e:
        print(f"   ❌ Error scraping Andertons: {e}")
        return []

def scrape_sweetwater_images(url, session):
    """Scrape product images from Sweetwater"""
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find product images on Sweetwater
        image_urls = []
        
        # Try different selectors for Sweetwater product images
        selectors = [
            'img[data-src*="product"]',
            'img.product-image',
            'img[src*="product"]',
            '.product-gallery img',
            '.image-gallery img',
            '.product-images img',
            'img[src*="media"]'
        ]
        
        for selector in selectors:
            images = soup.select(selector)
            for img in images:
                src = img.get('data-src') or img.get('src')
                if src and ('product' in src.lower() or 'item' in src.lower() or 'media' in src.lower()):
                    # Convert relative URLs to absolute
                    full_url = urljoin(url, src)
                    if full_url not in image_urls:
                        image_urls.append(full_url)
        
        return image_urls[:4]  # Return max 4 images
        
    except Exception as e:
        print(f"   ❌ Error scraping Sweetwater: {e}")
        return []

def get_product_images_from_retailers(product_urls, session):
    """Get product images from all retailer URLs"""
    all_images = []
    
    for url in product_urls:
        print(f"   🔍 Scraping: {urlparse(url).netloc}")
        
        if 'thomann' in url:
            images = scrape_thomann_images(url, session)
        elif 'gear4music' in url:
            images = scrape_gear4music_images(url, session)
        elif 'andertons' in url:
            images = scrape_andertons_images(url, session)
        elif 'sweetwater' in url:
            images = scrape_sweetwater_images(url, session)
        else:
            print(f"   ⚠️  Unknown retailer: {url}")
            continue
        
        if images:
            print(f"   ✅ Found {len(images)} images from {urlparse(url).netloc}")
            all_images.extend(images)
        else:
            print(f"   ❌ No images found from {urlparse(url).netloc}")
        
        time.sleep(2)  # Be respectful to retailers
        
        if len(all_images) >= 4:  # We only need 4 images per product
            break
    
    return all_images[:4]

def download_image(url, filepath, session, timeout=30):
    """Download image from URL and save to filepath"""
    try:
        response = session.get(url, stream=True, timeout=timeout)
        response.raise_for_status()
        
        # Check if it's actually an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print(f"   ⚠️  URL doesn't point to an image: {content_type}")
            return False
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verify the file was written and has content
        if os.path.getsize(filepath) > 5000:  # At least 5KB for a decent image
            return True
        else:
            if os.path.exists(filepath):
                os.remove(filepath)  # Remove empty/tiny file
            return False
            
    except Exception as e:
        print(f"   ❌ Error downloading image: {e}")
        return False

def backup_original_images():
    """Create backup of original images"""
    backup_dir = f"{PRODUCT_IMAGES_DIR}_backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📁 Created backup directory: {backup_dir}")
        
        # Copy all original images to backup
        for filename in os.listdir(PRODUCT_IMAGES_DIR):
            if filename.endswith('.jpg'):
                src = os.path.join(PRODUCT_IMAGES_DIR, filename)
                dst = os.path.join(backup_dir, filename)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
        
        print("📋 Backup of original images created")
    return backup_dir

def main():
    """Main function to scrape and download product images"""
    if not os.path.exists(PRODUCT_IMAGES_DIR):
        print(f"Error: Directory {PRODUCT_IMAGES_DIR} does not exist")
        return
    
    print("🎵 Starting to scrape REAL product images from music retailers...")
    print("🌐 Sources: Thomann, Gear4Music, Andertons, Sweetwater")
    print("⏱️  This may take a while as we're being respectful to the websites")
    print()
    
    # Create backup
    backup_dir = backup_original_images()
    
    # Create session
    session = get_session()
    
    successful_downloads = 0
    total_images = 0
    failed_products = []
    
    for product_key, retailer_urls in RETAILER_PRODUCT_URLS.items():
        print(f"\n🔍 Processing: {product_key}")
        
        # Find all images for this product
        product_files = [f for f in os.listdir(PRODUCT_IMAGES_DIR) 
                        if f.startswith(product_key) and f.endswith('.jpg')]
        
        if not product_files:
            print(f"   ⚠️  No images found for {product_key}")
            continue
        
        # Sort files to ensure consistent ordering
        product_files.sort()
        total_images += len(product_files)
        
        # Get images from retailers
        scraped_images = get_product_images_from_retailers(retailer_urls, session)
        
        if not scraped_images:
            print(f"   ❌ No images could be scraped for {product_key}")
            failed_products.append(product_key)
            continue
        
        product_success = 0
        
        # Download images for each variant
        for i, filename in enumerate(product_files):
            filepath = os.path.join(PRODUCT_IMAGES_DIR, filename)
            
            if i < len(scraped_images):
                image_url = scraped_images[i]
                
                print(f"   📥 Downloading image {i+1} for {filename}...")
                if download_image(image_url, filepath, session):
                    print(f"   ✅ Successfully downloaded: {filename}")
                    successful_downloads += 1
                    product_success += 1
                else:
                    print(f"   ❌ Failed to download: {filename}")
            else:
                print(f"   ⚠️  No more scraped images available for: {filename}")
        
        if product_success == 0:
            failed_products.append(product_key)
        
        # Longer delay between products to be respectful
        time.sleep(3)
    
    print(f"\n🎉 Scraping complete!")
    print(f"   Successfully downloaded: {successful_downloads}/{total_images} images")
    print(f"   Total products processed: {len(RETAILER_PRODUCT_URLS)}")
    print(f"   Products with no successful downloads: {len(failed_products)}")
    print(f"   Backup created in: {backup_dir}")
    
    if failed_products:
        print(f"\n⚠️  Products that failed to download any images:")
        for product in failed_products:
            print(f"   - {product}")
        print("   This could be due to:")
        print("   - Website structure changes")
        print("   - Rate limiting or blocking")
        print("   - Product URLs being outdated")
    
    if successful_downloads == 0:
        print("\n⚠️  No images were downloaded. This could be due to:")
        print("   1. Retailer websites blocking scraping")
        print("   2. Changed website structures")
        print("   3. Network connectivity issues")
        print("   4. Rate limiting")
        print("\n💡 Alternative approaches:")
        print("   1. Manually download images from retailer websites")
        print("   2. Use manufacturer press kits")
        print("   3. Contact retailers for product image permissions")
    elif successful_downloads < total_images:
        print(f"\n📝 Note: Downloaded {successful_downloads}/{total_images} real product images")
        print("   These are actual product photos from music retailers!")

if __name__ == "__main__":
    main()