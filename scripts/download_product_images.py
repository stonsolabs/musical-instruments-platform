#!/usr/bin/env python3
"""
Script to download all product images and store them locally in the public folder.
This creates a test version with local images for faster loading and offline development.
"""

import json
import os
import requests
import time
from urllib.parse import urlparse
from pathlib import Path
import hashlib

def download_image(url, local_path):
    """Download an image from URL and save it to local path."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Save the image
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Downloaded: {os.path.basename(local_path)}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def get_image_filename(url, product_sku, index):
    """Generate a filename for the image based on URL and product info."""
    # Extract file extension from URL
    parsed_url = urlparse(url)
    path = parsed_url.path
    ext = os.path.splitext(path)[1]
    
    if not ext:
        ext = '.jpg'  # Default to jpg if no extension found
    
    # Create a clean filename
    filename = f"{product_sku.lower().replace('-', '_')}_{index + 1}{ext}"
    return filename

def process_product_images():
    """Process all product images from the JSON file."""
    
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    public_dir = project_root / "frontend" / "public"
    images_dir = public_dir / "product-images"
    
    # Create images directory
    images_dir.mkdir(exist_ok=True)
    
    # Read the product data
    json_file = script_dir / "comprehensive_products_with_images.json"
    
    if not json_file.exists():
        print(f"Error: {json_file} not found!")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products = data.get('comprehensive_product_dataset', [])
    
    print(f"Found {len(products)} products to process")
    
    # Track statistics
    total_images = 0
    downloaded_images = 0
    failed_downloads = 0
    
    # Process each product
    for product_data in products:
        product = product_data.get('product_input', {})
        sku = product.get('sku', 'unknown')
        images = product.get('images', [])
        
        print(f"\nProcessing {sku} ({len(images)} images)")
        
        # Download each image
        local_images = []
        for i, image_url in enumerate(images):
            total_images += 1
            
            if not image_url or not image_url.startswith('http'):
                print(f"  Skipping invalid URL: {image_url}")
                continue
            
            # Generate local filename
            filename = get_image_filename(image_url, sku, i)
            local_path = images_dir / filename
            
            # Download the image
            if download_image(image_url, local_path):
                downloaded_images += 1
                local_images.append(f"/product-images/{filename}")
            else:
                failed_downloads += 1
                # Keep the original URL if download fails
                local_images.append(image_url)
            
            # Small delay to be respectful to servers
            time.sleep(0.1)
        
        # Update the product data with local image paths
        product['images'] = local_images
    
    # Save updated data
    output_file = script_dir / "products_with_local_images.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Download Summary:")
    print(f"Total images processed: {total_images}")
    print(f"Successfully downloaded: {downloaded_images}")
    print(f"Failed downloads: {failed_downloads}")
    print(f"Images stored in: {images_dir}")
    print(f"Updated data saved to: {output_file}")
    print(f"{'='*50}")
    
    # Create a simple index file for easy access
    index_file = images_dir / "index.txt"
    with open(index_file, 'w') as f:
        f.write("Product Images Index\n")
        f.write("===================\n\n")
        for product_data in data.get('comprehensive_product_dataset', []):
            product = product_data.get('product_input', {})
            sku = product.get('sku', 'unknown')
            images = product.get('images', [])
            f.write(f"{sku}: {len(images)} images\n")
            for i, img in enumerate(images):
                f.write(f"  {i+1}. {img}\n")
            f.write("\n")

if __name__ == "__main__":
    print("Starting product image download...")
    process_product_images()
    print("Done!")
