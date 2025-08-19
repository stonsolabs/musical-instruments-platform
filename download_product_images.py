#!/usr/bin/env python3
"""
Script to download real product images for musical instruments
and replace placeholder images in the product-images directory.
"""

import os
import requests
import json
import time
from pathlib import Path
from urllib.parse import quote

# Unsplash API configuration
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"  # Replace with your Unsplash API key
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

# Directory containing the product images
PRODUCT_IMAGES_DIR = "./frontend/public/product-images"

# Product name mappings based on filenames
PRODUCT_MAPPINGS = {
    "boss_ds1_distortion": "Boss DS-1 distortion pedal",
    "casio_px560_bk": "Casio PX-560 digital piano",
    "electro_harmonix_big_muff": "Electro-Harmonix Big Muff Pi distortion pedal",
    "fender_player_jazz_bass": "Fender Player Jazz Bass guitar",
    "fender_player_strat_sss": "Fender Player Stratocaster guitar",
    "fender_rumble_40_v3": "Fender Rumble 40 bass amplifier",
    "focusrite_scarlett_2i2_3rd": "Focusrite Scarlett 2i2 audio interface",
    "gibson_les_paul_studio_eb": "Gibson Les Paul Studio electric guitar",
    "ibanez_sr300e_pw": "Ibanez SR300E bass guitar",
    "marshall_dsl40cr": "Marshall DSL40CR tube amplifier",
    "martin_d28_std": "Martin D-28 acoustic guitar",
    "numark_party_mix": "Numark Party Mix DJ controller",
    "pearl_export_exx725sp": "Pearl Export drum kit",
    "pioneer_ddj_sb3": "Pioneer DDJ-SB3 DJ controller",
    "roland_td17kv": "Roland TD-17KV electronic drum kit",
    "shure_sm57_lc": "Shure SM57 microphone",
    "yamaha_fg830_nat": "Yamaha FG830 acoustic guitar",
    "yamaha_p125_bk": "Yamaha P-125 digital piano"
}

def get_unsplash_image_url(query, index=0):
    """Get image URL from Unsplash API"""
    if UNSPLASH_ACCESS_KEY == "YOUR_UNSPLASH_ACCESS_KEY":
        print("⚠️  Please set your Unsplash API key in the script")
        return None
    
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    
    params = {
        "query": query,
        "per_page": 10,
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(UNSPLASH_API_URL, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data["results"] and len(data["results"]) > index:
            return data["results"][index]["urls"]["regular"]
        
        return None
    except Exception as e:
        print(f"Error fetching image for '{query}': {e}")
        return None

def download_image(url, filepath):
    """Download image from URL and save to filepath"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"Error downloading image to {filepath}: {e}")
        return False

def main():
    """Main function to download and replace product images"""
    if not os.path.exists(PRODUCT_IMAGES_DIR):
        print(f"Error: Directory {PRODUCT_IMAGES_DIR} does not exist")
        return
    
    print("🎵 Starting to download real product images...")
    print("⚠️  Make sure to set your Unsplash API key in the script first!")
    print("   Get one free at: https://unsplash.com/developers")
    print()
    
    # Create backup directory
    backup_dir = f"{PRODUCT_IMAGES_DIR}_backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📁 Created backup directory: {backup_dir}")
    
    successful_downloads = 0
    total_products = len(PRODUCT_MAPPINGS)
    
    for product_key, product_name in PRODUCT_MAPPINGS.items():
        print(f"\n🔍 Processing: {product_name}")
        
        # Find all images for this product
        product_files = [f for f in os.listdir(PRODUCT_IMAGES_DIR) 
                        if f.startswith(product_key) and f.endswith('.jpg')]
        
        if not product_files:
            print(f"   ⚠️  No images found for {product_key}")
            continue
        
        # Download images for each variant
        for i, filename in enumerate(sorted(product_files)):
            filepath = os.path.join(PRODUCT_IMAGES_DIR, filename)
            backup_path = os.path.join(backup_dir, filename)
            
            # Backup original file
            if os.path.exists(filepath) and not os.path.exists(backup_path):
                os.copy2(filepath, backup_path)
            
            # Get image URL from Unsplash
            image_url = get_unsplash_image_url(product_name, i)
            
            if image_url:
                print(f"   📥 Downloading image {i+1} for {filename}...")
                if download_image(image_url, filepath):
                    print(f"   ✅ Successfully downloaded: {filename}")
                    successful_downloads += 1
                else:
                    print(f"   ❌ Failed to download: {filename}")
            else:
                print(f"   ❌ No image found for: {filename}")
            
            # Rate limiting to avoid hitting API limits
            time.sleep(1)
    
    print(f"\n🎉 Download complete!")
    print(f"   Successfully downloaded: {successful_downloads} images")
    print(f"   Total products processed: {total_products}")
    print(f"   Backup created in: {backup_dir}")
    
    if successful_downloads == 0:
        print("\n⚠️  No images were downloaded. Please check:")
        print("   1. Your Unsplash API key is set correctly")
        print("   2. Your internet connection")
        print("   3. The API rate limits")

if __name__ == "__main__":
    main()