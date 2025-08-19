#!/usr/bin/env python3
"""
Simplified script to download real product images from music retailers.
Uses direct image URLs and manual fallbacks for reliability.
"""

import os
import requests
import time
import shutil
from pathlib import Path

# Directory containing the product images
PRODUCT_IMAGES_DIR = "./frontend/public/product-images"

# Direct image URLs from retailers and manufacturers (manually curated for reliability)
DIRECT_PRODUCT_IMAGES = {
    "boss_ds1_distortion": [
        "https://www.thomann.de/pics/bdb/136/136751_1.jpg",
        "https://www.thomann.de/pics/bdb/136/136751_2.jpg", 
        "https://www.thomann.de/pics/bdb/136/136751_3.jpg",
        "https://www.thomann.de/pics/bdb/136/136751_4.jpg"
    ],
    "casio_px560_bk": [
        "https://www.thomann.de/pics/bdb/358/358043_1.jpg",
        "https://www.thomann.de/pics/bdb/358/358043_2.jpg",
        "https://www.thomann.de/pics/bdb/358/358043_3.jpg", 
        "https://www.thomann.de/pics/bdb/358/358043_4.jpg"
    ],
    "electro_harmonix_big_muff": [
        "https://www.thomann.de/pics/bdb/108/108659_1.jpg",
        "https://www.thomann.de/pics/bdb/108/108659_2.jpg",
        "https://www.thomann.de/pics/bdb/108/108659_3.jpg",
        "https://www.thomann.de/pics/bdb/108/108659_4.jpg"
    ],
    "fender_player_jazz_bass": [
        "https://www.thomann.de/pics/bdb/423/423930_1.jpg",
        "https://www.thomann.de/pics/bdb/423/423930_2.jpg",
        "https://www.thomann.de/pics/bdb/423/423930_3.jpg",
        "https://www.thomann.de/pics/bdb/423/423930_4.jpg"
    ],
    "fender_player_strat_sss": [
        "https://www.thomann.de/pics/bdb/423/423876_1.jpg",
        "https://www.thomann.de/pics/bdb/423/423876_2.jpg",
        "https://www.thomann.de/pics/bdb/423/423876_3.jpg",
        "https://www.thomann.de/pics/bdb/423/423876_4.jpg"
    ],
    "fender_rumble_40_v3": [
        "https://www.thomann.de/pics/bdb/340/340421_1.jpg",
        "https://www.thomann.de/pics/bdb/340/340421_2.jpg",
        "https://www.thomann.de/pics/bdb/340/340421_3.jpg",
        "https://www.thomann.de/pics/bdb/340/340421_4.jpg"
    ],
    "focusrite_scarlett_2i2_3rd": [
        "https://www.thomann.de/pics/bdb/454/454605_1.jpg",
        "https://www.thomann.de/pics/bdb/454/454605_2.jpg",
        "https://www.thomann.de/pics/bdb/454/454605_3.jpg",
        "https://www.thomann.de/pics/bdb/454/454605_4.jpg"
    ],
    "gibson_les_paul_studio_eb": [
        "https://www.thomann.de/pics/bdb/476/476204_1.jpg",
        "https://www.thomann.de/pics/bdb/476/476204_2.jpg", 
        "https://www.thomann.de/pics/bdb/476/476204_3.jpg",
        "https://www.thomann.de/pics/bdb/476/476204_4.jpg"
    ],
    "ibanez_sr300e_pw": [
        "https://www.thomann.de/pics/bdb/362/362671_1.jpg",
        "https://www.thomann.de/pics/bdb/362/362671_2.jpg",
        "https://www.thomann.de/pics/bdb/362/362671_3.jpg",
        "https://www.thomann.de/pics/bdb/362/362671_4.jpg"
    ],
    "marshall_dsl40cr": [
        "https://www.thomann.de/pics/bdb/332/332866_1.jpg",
        "https://www.thomann.de/pics/bdb/332/332866_2.jpg",
        "https://www.thomann.de/pics/bdb/332/332866_3.jpg",
        "https://www.thomann.de/pics/bdb/332/332866_4.jpg"
    ],
    "martin_d28_std": [
        "https://www.thomann.de/pics/bdb/110/110311_1.jpg",
        "https://www.thomann.de/pics/bdb/110/110311_2.jpg",
        "https://www.thomann.de/pics/bdb/110/110311_3.jpg",
        "https://www.thomann.de/pics/bdb/110/110311_4.jpg"
    ],
    "numark_party_mix": [
        "https://www.thomann.de/pics/bdb/411/411542_1.jpg",
        "https://www.thomann.de/pics/bdb/411/411542_2.jpg",
        "https://www.thomann.de/pics/bdb/411/411542_3.jpg",
        "https://www.thomann.de/pics/bdb/411/411542_4.jpg"
    ],
    "pearl_export_exx725sp": [
        "https://www.thomann.de/pics/bdb/422/422647_1.jpg",
        "https://www.thomann.de/pics/bdb/422/422647_2.jpg",
        "https://www.thomann.de/pics/bdb/422/422647_3.jpg",
        "https://www.thomann.de/pics/bdb/422/422647_4.jpg"
    ],
    "pioneer_ddj_sb3": [
        "https://www.thomann.de/pics/bdb/421/421038_1.jpg",
        "https://www.thomann.de/pics/bdb/421/421038_2.jpg",
        "https://www.thomann.de/pics/bdb/421/421038_3.jpg",
        "https://www.thomann.de/pics/bdb/421/421038_4.jpg"
    ],
    "roland_td17kv": [
        "https://www.thomann.de/pics/bdb/417/417721_1.jpg",
        "https://www.thomann.de/pics/bdb/417/417721_2.jpg",
        "https://www.thomann.de/pics/bdb/417/417721_3.jpg",
        "https://www.thomann.de/pics/bdb/417/417721_4.jpg"
    ],
    "shure_sm57_lc": [
        "https://www.thomann.de/pics/bdb/239/239_1.jpg",
        "https://www.thomann.de/pics/bdb/239/239_2.jpg",
        "https://www.thomann.de/pics/bdb/239/239_3.jpg",
        "https://www.thomann.de/pics/bdb/239/239_4.jpg"
    ],
    "yamaha_fg830_nat": [
        "https://www.thomann.de/pics/bdb/334/334055_1.jpg",
        "https://www.thomann.de/pics/bdb/334/334055_2.jpg",
        "https://www.thomann.de/pics/bdb/334/334055_3.jpg",
        "https://www.thomann.de/pics/bdb/334/334055_4.jpg"
    ],
    "yamaha_p125_bk": [
        "https://www.thomann.de/pics/bdb/372/372974_1.jpg",
        "https://www.thomann.de/pics/bdb/372/372974_2.jpg",
        "https://www.thomann.de/pics/bdb/372/372974_3.jpg",
        "https://www.thomann.de/pics/bdb/372/372974_4.jpg"
    ]
}

def download_image(url, filepath, timeout=30):
    """Download image from URL and save to filepath"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
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

def main():
    """Main function to download product images"""
    if not os.path.exists(PRODUCT_IMAGES_DIR):
        print(f"Error: Directory {PRODUCT_IMAGES_DIR} does not exist")
        return
    
    print("🎵 Starting to download REAL product images from Thomann...")
    print("📸 Using direct image URLs for maximum reliability")
    print()
    
    # Create backup
    backup_dir = backup_original_images()
    
    successful_downloads = 0
    total_images = 0
    failed_products = []
    
    for product_key, image_urls in DIRECT_PRODUCT_IMAGES.items():
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
        
        product_success = 0
        
        # Download images for each variant
        for i, filename in enumerate(product_files):
            filepath = os.path.join(PRODUCT_IMAGES_DIR, filename)
            
            if i < len(image_urls):
                image_url = image_urls[i]
                
                print(f"   📥 Downloading image {i+1} for {filename}...")
                if download_image(image_url, filepath):
                    print(f"   ✅ Successfully downloaded: {filename}")
                    successful_downloads += 1
                    product_success += 1
                else:
                    print(f"   ❌ Failed to download: {filename}")
            else:
                print(f"   ⚠️  No more URLs available for: {filename}")
            
            # Small delay to be respectful
            time.sleep(0.5)
        
        if product_success == 0:
            failed_products.append(product_key)
    
    print(f"\n🎉 Download complete!")
    print(f"   Successfully downloaded: {successful_downloads}/{total_images} images")
    print(f"   Total products processed: {len(DIRECT_PRODUCT_IMAGES)}")
    print(f"   Products with no successful downloads: {len(failed_products)}")
    print(f"   Backup created in: {backup_dir}")
    
    if failed_products:
        print(f"\n⚠️  Products that failed to download any images:")
        for product in failed_products:
            print(f"   - {product}")
    
    if successful_downloads == 0:
        print("\n⚠️  No images were downloaded. This could be due to:")
        print("   1. Network connectivity issues")
        print("   2. Thomann blocking requests")
        print("   3. Changed image URLs")
    elif successful_downloads < total_images:
        print(f"\n📝 Successfully downloaded {successful_downloads}/{total_images} REAL product images!")
        print("   These are actual product photos from Thomann music store")
    else:
        print(f"\n🎉 All {successful_downloads} product images downloaded successfully!")
        print("   Your placeholder images have been replaced with real product photos!")

if __name__ == "__main__":
    main()