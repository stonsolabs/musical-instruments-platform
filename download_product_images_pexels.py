#!/usr/bin/env python3
"""
Script to download real product images for musical instruments using Pexels API
and replace placeholder images in the product-images directory.
"""

import os
import requests
import json
import time
import shutil
from pathlib import Path

# Pexels API configuration
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"  # Replace with your Pexels API key
PEXELS_API_URL = "https://api.pexels.com/v1/search"

# Directory containing the product images
PRODUCT_IMAGES_DIR = "./frontend/public/product-images"

# Product name mappings based on filenames
PRODUCT_MAPPINGS = {
    "boss_ds1_distortion": "Boss DS-1 distortion guitar pedal",
    "casio_px560_bk": "Casio digital piano keyboard",
    "electro_harmonix_big_muff": "Big Muff distortion guitar pedal",
    "fender_player_jazz_bass": "Fender Jazz Bass electric guitar",
    "fender_player_strat_sss": "Fender Stratocaster electric guitar",
    "fender_rumble_40_v3": "Fender bass guitar amplifier",
    "focusrite_scarlett_2i2_3rd": "Focusrite audio interface recording",
    "gibson_les_paul_studio_eb": "Gibson Les Paul electric guitar",
    "ibanez_sr300e_pw": "Ibanez bass guitar electric",
    "marshall_dsl40cr": "Marshall guitar amplifier tube amp",
    "martin_d28_std": "Martin acoustic guitar dreadnought",
    "numark_party_mix": "DJ controller mixing console",
    "pearl_export_exx725sp": "Pearl drum kit acoustic drums",
    "pioneer_ddj_sb3": "Pioneer DJ controller mixer",
    "roland_td17kv": "Roland electronic drum kit",
    "shure_sm57_lc": "Shure SM57 microphone recording",
    "yamaha_fg830_nat": "Yamaha acoustic guitar",
    "yamaha_p125_bk": "Yamaha digital piano keyboard"
}

def get_pexels_image_url(query, index=0):
    """Get image URL from Pexels API"""
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY":
        print("⚠️  Please set your Pexels API key in the script")
        return None
    
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    
    params = {
        "query": query,
        "per_page": 15,
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(PEXELS_API_URL, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data["photos"] and len(data["photos"]) > index:
            return data["photos"][index]["src"]["large"]
        
        return None
    except Exception as e:
        print(f"Error fetching image for '{query}': {e}")
        return None

def download_image(url, filepath):
    """Download image from URL and save to filepath"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"Error downloading image to {filepath}: {e}")
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
    """Main function to download and replace product images"""
    if not os.path.exists(PRODUCT_IMAGES_DIR):
        print(f"Error: Directory {PRODUCT_IMAGES_DIR} does not exist")
        return
    
    print("🎵 Starting to download real product images using Pexels API...")
    print("⚠️  Make sure to set your Pexels API key in the script first!")
    print("   Get one free at: https://www.pexels.com/api/")
    print()
    
    # Create backup
    backup_dir = backup_original_images()
    
    successful_downloads = 0
    total_images = 0
    
    for product_key, product_name in PRODUCT_MAPPINGS.items():
        print(f"\n🔍 Processing: {product_name}")
        
        # Find all images for this product
        product_files = [f for f in os.listdir(PRODUCT_IMAGES_DIR) 
                        if f.startswith(product_key) and f.endswith('.jpg')]
        
        if not product_files:
            print(f"   ⚠️  No images found for {product_key}")
            continue
        
        # Sort files to ensure consistent ordering
        product_files.sort()
        total_images += len(product_files)
        
        # Download images for each variant
        for i, filename in enumerate(product_files):
            filepath = os.path.join(PRODUCT_IMAGES_DIR, filename)
            
            # Get image URL from Pexels (use different search terms for variety)
            search_terms = [
                product_name,
                f"{product_name} studio",
                f"{product_name} professional",
                f"{product_name} close up"
            ]
            
            search_query = search_terms[i % len(search_terms)]
            image_url = get_pexels_image_url(search_query, i // len(search_terms))
            
            if image_url:
                print(f"   📥 Downloading image {i+1} for {filename}...")
                if download_image(image_url, filepath):
                    print(f"   ✅ Successfully downloaded: {filename}")
                    successful_downloads += 1
                else:
                    print(f"   ❌ Failed to download: {filename}")
            else:
                print(f"   ❌ No image found for: {filename}")
            
            # Rate limiting to be respectful to the API
            time.sleep(1.5)
    
    print(f"\n🎉 Download complete!")
    print(f"   Successfully downloaded: {successful_downloads}/{total_images} images")
    print(f"   Total products processed: {len(PRODUCT_MAPPINGS)}")
    print(f"   Backup created in: {backup_dir}")
    
    if successful_downloads == 0:
        print("\n⚠️  No images were downloaded. Please check:")
        print("   1. Your Pexels API key is set correctly")
        print("   2. Your internet connection")
        print("   3. The API rate limits")
    elif successful_downloads < total_images:
        print(f"\n⚠️  Only {successful_downloads}/{total_images} images downloaded successfully")
        print("   Some images may not have been found or download failed")

if __name__ == "__main__":
    main()