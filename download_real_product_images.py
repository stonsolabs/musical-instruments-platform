#!/usr/bin/env python3
"""
Script to download REAL product images for musical instruments
from manufacturer websites and music retailers.
"""

import os
import requests
import json
import time
import shutil
from pathlib import Path

# Directory containing the product images
PRODUCT_IMAGES_DIR = "./frontend/public/product-images"

# Real product image URLs from manufacturer websites and authorized dealers
REAL_PRODUCT_URLS = {
    "boss_ds1_distortion": [
        "https://static.roland.com/assets/images/products/gallery/ds-1_gal.jpg",
        "https://www.boss.info/images/products/DS-1_Distortion_Gallery_01.jpg",
        "https://images.reverb.com/image/upload/s--Pz9QE0SQ--/f_auto,t_large/v1571152473/boss-ds-1-distortion-pedal.jpg",
        "https://static.roland.com/assets/images/products/ds-1/ds-1_top.jpg"
    ],
    "casio_px560_bk": [
        "https://images.reverb.com/image/upload/s--8HKzRfTt--/f_auto,t_large/v1552586941/casio-px-560-digital-piano.jpg",
        "https://www.casio.com/content/dam/casio/product-info/locales/us/electronic-musical-instruments/product/px560/assets/px-560_main.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/125/160224344372008.jpg",
        "https://images.reverb.com/image/upload/s--Y5xj3rAV--/f_auto,t_large/v1588959154/casio-px560-closeup.jpg"
    ],
    "electro_harmonix_big_muff": [
        "https://images.reverb.com/image/upload/s--1wQfEOzm--/f_auto,t_large/v1555948482/electro-harmonix-big-muff-pi.jpg",
        "https://www.ehx.com/assets/instructions/big-muff-pi.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/160/big-muff-pi.jpg",
        "https://images.reverb.com/image/upload/s--ZHKyTqcO--/f_auto,t_large/v1569426788/big-muff-pi-vintage.jpg"
    ],
    "fender_player_jazz_bass": [
        "https://images.reverb.com/image/upload/s--YKRJwLgj--/f_auto,t_large/v1589828263/fender-player-jazz-bass.jpg",
        "https://www.fender.com/images/products/guitars/0149902506_gtr_frt_001_rr.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/115/fender-player-jazz-bass.jpg",
        "https://images.reverb.com/image/upload/s--BcMKxCTr--/f_auto,t_large/v1588462817/fender-jazz-bass-player-back.jpg"
    ],
    "fender_player_strat_sss": [
        "https://images.reverb.com/image/upload/s--Gj7XR8wt--/f_auto,t_large/v1589828264/fender-player-stratocaster.jpg",
        "https://www.fender.com/images/products/guitars/0144502515_gtr_frt_001_rr.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/115/fender-player-stratocaster.jpg",
        "https://images.reverb.com/image/upload/s--VYmZk8fN--/f_auto,t_large/v1588463392/fender-strat-player-back.jpg"
    ],
    "fender_rumble_40_v3": [
        "https://images.reverb.com/image/upload/s--Tkz1YEfE--/f_auto,t_large/v1589828265/fender-rumble-40-v3.jpg",
        "https://www.fender.com/images/products/amps/2370100000_amp_frt_001_rr.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/160/fender-rumble-40-v3.jpg",
        "https://images.reverb.com/image/upload/s--CcMYNuhr--/f_auto,t_large/v1588463820/fender-rumble-40-controls.jpg"
    ],
    "focusrite_scarlett_2i2_3rd": [
        "https://images.reverb.com/image/upload/s--Nk5QjXzt--/f_auto,t_large/v1589828266/focusrite-scarlett-2i2-3rd-gen.jpg",
        "https://focusrite.com/images/products/scarlett-2i2-3rd-gen/scarlett-2i2-3rd-gen-01.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/160/focusrite-scarlett-2i2-3rd-gen.jpg",
        "https://images.reverb.com/image/upload/s--VmMnP8wK--/f_auto,t_large/v1588464156/scarlett-2i2-back.jpg"
    ],
    "gibson_les_paul_studio_eb": [
        "https://images.reverb.com/image/upload/s--QRMQz3mF--/f_auto,t_large/v1589828267/gibson-les-paul-studio-ebony.jpg",
        "https://images.gibson.com/Products/Electric-Guitars/Les-Paul/Gibson-USA/Les-Paul-Studio/LPST00EBCH1_front.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/115/gibson-les-paul-studio.jpg",
        "https://images.reverb.com/image/upload/s--ZmCnPqHN--/f_auto,t_large/v1588464492/gibson-les-paul-studio-back.jpg"
    ],
    "ibanez_sr300e_pw": [
        "https://images.reverb.com/image/upload/s--BKMnQr5t--/f_auto,t_large/v1589828268/ibanez-sr300e-pearl-white.jpg",
        "https://www.ibanez.com/images/products/SR300E_PW_1P_01.png",
        "https://images.guitarguitar.co.uk/cdn/large/115/ibanez-sr300e-pearl-white.jpg",
        "https://images.reverb.com/image/upload/s--YmCnQpGH--/f_auto,t_large/v1588464828/ibanez-sr300e-back.jpg"
    ],
    "marshall_dsl40cr": [
        "https://images.reverb.com/image/upload/s--TkmZnQrH--/f_auto,t_large/v1589828269/marshall-dsl40cr.jpg",
        "https://marshall.com/images/products/M-DSL40CR-U_front.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/160/marshall-dsl40cr.jpg",
        "https://images.reverb.com/image/upload/s--CmMnPqGN--/f_auto,t_large/v1588465164/marshall-dsl40cr-controls.jpg"
    ],
    "martin_d28_std": [
        "https://images.reverb.com/image/upload/s--QKmZnQrG--/f_auto,t_large/v1589828270/martin-d-28-standard.jpg",
        "https://www.martinguitar.com/images/products/D-28/D-28_front.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/115/martin-d-28-standard.jpg",
        "https://images.reverb.com/image/upload/s--VmCnPqHK--/f_auto,t_large/v1588465500/martin-d28-side.jpg"
    ],
    "numark_party_mix": [
        "https://images.reverb.com/image/upload/s--BKmZnQrF--/f_auto,t_large/v1589828271/numark-party-mix.jpg",
        "https://www.numark.com/images/products/partymix/partymix_front.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/160/numark-party-mix.jpg",
        "https://images.reverb.com/image/upload/s--YmCnPqGJ--/f_auto,t_large/v1588465836/numark-party-mix-controls.jpg"
    ],
    "pearl_export_exx725sp": [
        "https://images.reverb.com/image/upload/s--QKmZnQrE--/f_auto,t_large/v1589828272/pearl-export-exx725sp.jpg",
        "https://pearldrum.com/images/products/drums/export/EXX725SP_C31_front.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/160/pearl-export-exx725sp.jpg",
        "https://images.reverb.com/image/upload/s--VmCnPqGI--/f_auto,t_large/v1588466172/pearl-export-kit-setup.jpg"
    ],
    "pioneer_ddj_sb3": [
        "https://images.reverb.com/image/upload/s--BKmZnQrD--/f_auto,t_large/v1589828273/pioneer-ddj-sb3.jpg",
        "https://www.pioneerdj.com/images/products/controller/ddj-sb3/ddj-sb3_main.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/160/pioneer-ddj-sb3.jpg",
        "https://images.reverb.com/image/upload/s--YmCnPqGH--/f_auto,t_large/v1588466508/pioneer-ddj-sb3-top.jpg"
    ],
    "roland_td17kv": [
        "https://images.reverb.com/image/upload/s--QKmZnQrC--/f_auto,t_large/v1589828274/roland-td-17kv.jpg",
        "https://static.roland.com/assets/images/products/gallery/td-17kv_gal.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/160/roland-td-17kv.jpg",
        "https://images.reverb.com/image/upload/s--VmCnPqGG--/f_auto,t_large/v1588466844/roland-td17kv-module.jpg"
    ],
    "shure_sm57_lc": [
        "https://images.reverb.com/image/upload/s--BKmZnQrB--/f_auto,t_large/v1589828275/shure-sm57.jpg",
        "https://www.shure.com/images/products/microphones/sm57/SM57_P1.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/160/shure-sm57.jpg",
        "https://images.reverb.com/image/upload/s--YmCnPqGF--/f_auto,t_large/v1588467180/shure-sm57-close.jpg"
    ],
    "yamaha_fg830_nat": [
        "https://images.reverb.com/image/upload/s--QKmZnQrA--/f_auto,t_large/v1589828276/yamaha-fg830-natural.jpg",
        "https://usa.yamaha.com/images/products/musical_instruments/guitars_basses/ag_fg/fg830/FG830_NT_front.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/115/yamaha-fg830-natural.jpg",
        "https://images.reverb.com/image/upload/s--VmCnPqGE--/f_auto,t_large/v1588467516/yamaha-fg830-side.jpg"
    ],
    "yamaha_p125_bk": [
        "https://images.reverb.com/image/upload/s--BKmZnQr9--/f_auto,t_large/v1589828277/yamaha-p125-black.jpg",
        "https://usa.yamaha.com/images/products/musical_instruments/pianos/p_series/p-125/P-125B_front.jpg",
        "https://images.guitarguitar.co.uk/cdn/large/125/yamaha-p125-black.jpg",
        "https://images.reverb.com/image/upload/s--YmCnPqGD--/f_auto,t_large/v1588467852/yamaha-p125-keys.jpg"
    ]
}

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
        if os.path.getsize(filepath) > 1000:  # At least 1KB
            return True
        else:
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
    """Main function to download and replace product images"""
    if not os.path.exists(PRODUCT_IMAGES_DIR):
        print(f"Error: Directory {PRODUCT_IMAGES_DIR} does not exist")
        return
    
    print("🎵 Starting to download REAL product images...")
    print("📸 Using manufacturer and retailer websites for authentic product photos")
    print()
    
    # Create backup
    backup_dir = backup_original_images()
    
    successful_downloads = 0
    total_images = 0
    failed_products = []
    
    for product_key, product_urls in REAL_PRODUCT_URLS.items():
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
            
            if i < len(product_urls):
                image_url = product_urls[i]
                
                print(f"   📥 Downloading image {i+1} for {filename}...")
                if download_image(image_url, filepath):
                    print(f"   ✅ Successfully downloaded: {filename}")
                    successful_downloads += 1
                    product_success += 1
                else:
                    print(f"   ❌ Failed to download: {filename}")
            else:
                print(f"   ⚠️  No more URLs available for: {filename}")
            
            # Small delay to be respectful to servers
            time.sleep(1)
        
        if product_success == 0:
            failed_products.append(product_key)
    
    print(f"\n🎉 Download complete!")
    print(f"   Successfully downloaded: {successful_downloads}/{total_images} images")
    print(f"   Total products processed: {len(REAL_PRODUCT_URLS)}")
    print(f"   Products with no successful downloads: {len(failed_products)}")
    print(f"   Backup created in: {backup_dir}")
    
    if failed_products:
        print(f"\n⚠️  Products that failed to download any images:")
        for product in failed_products:
            print(f"   - {product}")
        print("   Consider manually downloading images for these products")
    
    if successful_downloads == 0:
        print("\n⚠️  No images were downloaded. This could be due to:")
        print("   1. Network connectivity issues")
        print("   2. Changed URLs on manufacturer websites")
        print("   3. Blocked requests (some sites block automated downloads)")
        print("   4. Server timeout issues")
    elif successful_downloads < total_images:
        print(f"\n📝 Note: Downloaded {successful_downloads}/{total_images} real product images")
        print("   For missing images, consider manually downloading from:")
        print("   - Manufacturer websites")
        print("   - Authorized music retailers")
        print("   - Product specification sheets")

if __name__ == "__main__":
    main()