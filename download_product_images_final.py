#!/usr/bin/env python3
"""
Final script to download real product images using the Pixabay API (free tier available)
or manually curated working URLs for musical instruments.
"""

import os
import requests
import json
import time
import shutil
from pathlib import Path

# Directory containing the product images
PRODUCT_IMAGES_DIR = "./frontend/public/product-images"

# Pixabay API configuration (get free key at https://pixabay.com/api/docs/)
PIXABAY_API_KEY = "YOUR_PIXABAY_API_KEY"  # Replace with your Pixabay API key
PIXABAY_API_URL = "https://pixabay.com/api/"

# Product search terms for Pixabay
PRODUCT_SEARCH_TERMS = {
    "boss_ds1_distortion": ["Boss DS-1 pedal", "distortion guitar pedal", "orange guitar effect", "Boss pedal"],
    "casio_px560_bk": ["Casio digital piano", "electronic piano keyboard", "digital piano black", "Casio keyboard"],
    "electro_harmonix_big_muff": ["Big Muff pedal", "purple guitar pedal", "fuzz distortion", "guitar effect pedal"],
    "fender_player_jazz_bass": ["Fender Jazz Bass", "electric bass guitar", "4 string bass", "Fender bass"],
    "fender_player_strat_sss": ["Fender Stratocaster", "electric guitar white", "Stratocaster guitar", "Fender electric"],
    "fender_rumble_40_v3": ["bass amplifier", "guitar amp combo", "Fender amplifier", "bass amp"],
    "focusrite_scarlett_2i2_3rd": ["audio interface red", "USB audio interface", "recording interface", "Focusrite"],
    "gibson_les_paul_studio_eb": ["Gibson Les Paul", "Les Paul guitar black", "electric guitar Gibson", "Les Paul"],
    "ibanez_sr300e_pw": ["Ibanez bass guitar", "white bass guitar", "electric bass", "Ibanez SR"],
    "marshall_dsl40cr": ["Marshall amplifier", "guitar amp Marshall", "tube amplifier", "Marshall combo"],
    "martin_d28_std": ["Martin acoustic guitar", "dreadnought guitar", "acoustic guitar", "Martin D-28"],
    "numark_party_mix": ["DJ controller", "mixing console", "DJ mixer", "Party Mix"],
    "pearl_export_exx725sp": ["Pearl drum kit", "acoustic drums", "drum set black", "Pearl drums"],
    "pioneer_ddj_sb3": ["Pioneer DJ controller", "DDJ controller", "Serato controller", "DJ mixing"],
    "roland_td17kv": ["Roland electronic drums", "electric drum kit", "V-Drums", "Roland drums"],
    "shure_sm57_lc": ["Shure SM57", "dynamic microphone", "studio microphone", "Shure mic"],
    "yamaha_fg830_nat": ["Yamaha acoustic guitar", "folk guitar natural", "acoustic guitar", "Yamaha FG"],
    "yamaha_p125_bk": ["Yamaha digital piano", "portable piano black", "electric piano", "Yamaha P-125"]
}

# Fallback: Working sample URLs for demonstration (these are real, working Unsplash URLs)
SAMPLE_WORKING_URLS = {
    "guitar": [
        "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=800&q=80&fit=crop",  # Acoustic guitar
        "https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?w=800&q=80&fit=crop",  # Electric guitar
        "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&q=80&fit=crop",  # Guitar equipment
        "https://images.unsplash.com/photo-1571327073757-95c73734d4d4?w=800&q=80&fit=crop"   # Music equipment
    ],
    "piano": [
        "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=800&q=80&fit=crop",  # Piano keys
        "https://images.unsplash.com/photo-1612225330812-01a9c6b355ec?w=800&q=80&fit=crop",  # Digital piano
        "https://images.unsplash.com/photo-1571327073757-95c73734d4d4?w=800&q=80&fit=crop",  # Music equipment
        "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&q=80&fit=crop"   # Equipment
    ],
    "drums": [
        "https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=800&q=80&fit=crop",  # Drum kit
        "https://images.unsplash.com/photo-1571327073757-95c73734d4d4?w=800&q=80&fit=crop",  # Music equipment
        "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&q=80&fit=crop",  # Equipment
        "https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?w=800&q=80&fit=crop"   # Equipment
    ],
    "equipment": [
        "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&q=80&fit=crop",  # Audio equipment
        "https://images.unsplash.com/photo-1571327073757-95c73734d4d4?w=800&q=80&fit=crop",  # Music equipment
        "https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?w=800&q=80&fit=crop",  # Equipment
        "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=800&q=80&fit=crop"   # Piano/equipment
    ]
}

def get_pixabay_image_url(query, index=0):
    """Get image URL from Pixabay API"""
    if PIXABAY_API_KEY == "YOUR_PIXABAY_API_KEY":
        print("   ⚠️  Pixabay API key not set, using fallback URLs")
        return None
    
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "orientation": "horizontal",
        "category": "music",
        "min_width": 800,
        "per_page": 10,
        "safesearch": "true"
    }
    
    try:
        response = requests.get(PIXABAY_API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data["hits"] and len(data["hits"]) > index:
            return data["hits"][index]["largeImageURL"]
        
        return None
    except Exception as e:
        print(f"   ❌ Error fetching from Pixabay: {e}")
        return None

def download_image(url, filepath, timeout=30):
    """Download image from URL and save to filepath"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True, timeout=timeout)
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

def get_category_for_product(product_key):
    """Determine the category for a product"""
    if any(word in product_key.lower() for word in ["guitar", "bass", "strat", "les_paul", "martin", "yamaha_fg", "fender", "gibson", "ibanez"]):
        return "guitar"
    elif any(word in product_key.lower() for word in ["piano", "keyboard", "casio", "yamaha_p"]):
        return "piano"
    elif any(word in product_key.lower() for word in ["drum", "pearl", "roland_td"]):
        return "drums"
    else:
        return "equipment"

def main():
    """Main function to download and replace product images"""
    if not os.path.exists(PRODUCT_IMAGES_DIR):
        print(f"Error: Directory {PRODUCT_IMAGES_DIR} does not exist")
        return
    
    print("🎵 Starting to download real product images...")
    print("📸 Using Pixabay API (if configured) or fallback to curated stock images")
    print("   For best results, get a free API key at: https://pixabay.com/api/docs/")
    print()
    
    # Create backup
    backup_dir = backup_original_images()
    
    successful_downloads = 0
    total_images = 0
    
    for product_key, search_terms in PRODUCT_SEARCH_TERMS.items():
        print(f"\n🔍 Processing: {search_terms[0]}")
        
        # Find all images for this product
        product_files = [f for f in os.listdir(PRODUCT_IMAGES_DIR) 
                        if f.startswith(product_key) and f.endswith('.jpg')]
        
        if not product_files:
            print(f"   ⚠️  No images found for {product_key}")
            continue
        
        # Sort files to ensure consistent ordering
        product_files.sort()
        total_images += len(product_files)
        
        category = get_category_for_product(product_key)
        fallback_urls = SAMPLE_WORKING_URLS[category]
        
        # Download images for each variant
        for i, filename in enumerate(product_files):
            filepath = os.path.join(PRODUCT_IMAGES_DIR, filename)
            image_url = None
            
            # Try Pixabay API first
            if i < len(search_terms):
                search_query = search_terms[i % len(search_terms)]
                image_url = get_pixabay_image_url(search_query, i // len(search_terms))
            
            # Fallback to sample URLs if Pixabay fails
            if not image_url and i < len(fallback_urls):
                image_url = fallback_urls[i]
                print(f"   📥 Using fallback image {i+1} for {filename}...")
            
            if image_url:
                if download_image(image_url, filepath):
                    print(f"   ✅ Successfully downloaded: {filename}")
                    successful_downloads += 1
                else:
                    print(f"   ❌ Failed to download: {filename}")
            else:
                print(f"   ⚠️  No image URL available for: {filename}")
            
            # Small delay to be respectful
            time.sleep(1)
    
    print(f"\n🎉 Download complete!")
    print(f"   Successfully downloaded: {successful_downloads}/{total_images} images")
    print(f"   Total products processed: {len(PRODUCT_SEARCH_TERMS)}")
    print(f"   Backup created in: {backup_dir}")
    
    if successful_downloads == 0:
        print("\n⚠️  No images were downloaded. Please check:")
        print("   1. Your internet connection")
        print("   2. Consider getting a Pixabay API key for better results")
    elif successful_downloads < total_images:
        print(f"\n📝 Note: Downloaded {successful_downloads}/{total_images} images")
        print("   For better product-specific images, consider:")
        print("   1. Getting a free Pixabay API key")
        print("   2. Using the Pexels API version")
        print("   3. Manually downloading from manufacturer websites")
        print("   4. Using paid stock photo services")

if __name__ == "__main__":
    main()