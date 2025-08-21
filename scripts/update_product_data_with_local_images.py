#!/usr/bin/env python3
"""
Script to update product data files to use local image paths.
This updates the main product data files to reference the downloaded/placeholder images.
"""

import json
import os
from pathlib import Path

def get_local_image_paths(sku, image_count=4):
    """Generate local image paths for a product."""
    local_images = []
    for i in range(image_count):
        filename = f"{sku.lower().replace('-', '_')}_{i + 1}.jpg"
        local_images.append(f"/product-images/{filename}")
    return local_images

def update_product_data_file(input_file, output_file):
    """Update a product data file to use local image paths."""
    
    print(f"Processing {input_file}")
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if it's the comprehensive dataset format
    if 'comprehensive_product_dataset' in data:
        products = data['comprehensive_product_dataset']
        for product_data in products:
            product = product_data.get('product_input', {})
            sku = product.get('sku', 'unknown')
            # Update images to use local paths
            product['images'] = get_local_image_paths(sku)
    elif 'all_categories_products' in data:
        # Handle the all_categories_products format
        categories = data['all_categories_products']
        for category_name, category_products in categories.items():
            for product_data in category_products:
                product = product_data.get('product_input', {})
                sku = product.get('sku', 'unknown')
                # Update images to use local paths
                product['images'] = get_local_image_paths(sku)
    else:
        # Assume it's a simple product list
        for product in data:
            if isinstance(product, dict):
                sku = product.get('sku', 'unknown')
                # Update images to use local paths
                product['images'] = get_local_image_paths(sku)
    
    # Write the updated data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Updated {output_file}")

def main():
    """Update all product data files."""
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Files to update
    files_to_update = [
        {
            'input': script_dir / "comprehensive_products_with_images.json",
            'output': project_root / "comprehensive_products_with_local_images.json"
        },
        {
            'input': project_root / "comprehensive_products_with_ai_content.json",
            'output': project_root / "comprehensive_products_with_ai_content_local_images.json"
        },
        {
            'input': project_root / "all_categories_products.json",
            'output': project_root / "all_categories_products_local_images.json"
        }
    ]
    
    print("Updating product data files to use local images...")
    
    for file_info in files_to_update:
        if file_info['input'].exists():
            update_product_data_file(file_info['input'], file_info['output'])
        else:
            print(f"Warning: {file_info['input']} not found, skipping...")
    
    print("\nAll files updated successfully!")
    print("\nUpdated files:")
    for file_info in files_to_update:
        if file_info['output'].exists():
            print(f"  - {file_info['output']}")

if __name__ == "__main__":
    main()
