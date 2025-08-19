#!/usr/bin/env python3
"""
Script to generate placeholder images for products that failed to download.
This creates simple placeholder images with product names for testing purposes.
"""

import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_placeholder_image(product_name, sku, category, filename, size=(400, 400)):
    """Create a placeholder image with product information."""
    
    # Create a new image with a gradient background
    img = Image.new('RGB', size, color='#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    # Create a gradient effect
    for y in range(size[1]):
        r = int(240 - (y / size[1]) * 40)
        g = int(240 - (y / size[1]) * 40)
        b = int(240 - (y / size[1]) * 40)
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    
    # Add a border
    draw.rectangle([0, 0, size[0]-1, size[1]-1], outline='#cccccc', width=2)
    
    # Try to use a default font, fallback to basic if not available
    try:
        # Try to use a system font
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        try:
            # Try alternative font paths
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            # Use default font
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # Calculate text positioning
    text_color = '#333333'
    center_x = size[0] // 2
    center_y = size[1] // 2
    
    # Add category icon/emoji based on category
    category_icons = {
        'electric-guitars': '🎸',
        'acoustic-guitars': '🎸',
        'bass-guitars': '🎸',
        'pianos': '🎹',
        'keyboards': '🎹',
        'drums': '🥁',
        'amplifiers': '🔊',
        'effects': '🎛️',
        'dj-equipment': '🎧',
        'recording': '🎤',
        'accessories': '🎵'
    }
    
    icon = category_icons.get(category, '🎵')
    
    # Draw icon
    try:
        # Try to use a larger font for emoji
        emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 80)
        emoji_bbox = draw.textbbox((0, 0), icon, font=emoji_font)
        emoji_width = emoji_bbox[2] - emoji_bbox[0]
        emoji_height = emoji_bbox[3] - emoji_bbox[1]
        draw.text((center_x - emoji_width//2, center_y - emoji_height//2 - 40), icon, font=emoji_font, fill=text_color)
    except:
        # Fallback to default font
        draw.text((center_x - 20, center_y - 40), icon, font=font_large, fill=text_color)
    
    # Wrap product name text
    max_width = size[0] - 40
    wrapped_text = textwrap.fill(product_name, width=20)
    
    # Draw product name
    lines = wrapped_text.split('\n')
    line_height = 30
    total_height = len(lines) * line_height
    start_y = center_y + 20
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = center_x - text_width // 2
        y = start_y + i * line_height
        draw.text((x, y), line, font=font_large, fill=text_color)
    
    # Add SKU at bottom
    sku_text = f"SKU: {sku}"
    bbox = draw.textbbox((0, 0), sku_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = center_x - text_width // 2
    y = size[1] - 40
    draw.text((x, y), sku_text, font=font_small, fill='#666666')
    
    # Add "Placeholder" watermark
    watermark_text = "PLACEHOLDER"
    bbox = draw.textbbox((0, 0), watermark_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = center_x - text_width // 2
    y = 20
    draw.text((x, y), watermark_text, font=font_small, fill='#999999')
    
    return img

def generate_placeholder_images():
    """Generate placeholder images for products that need them."""
    
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    public_dir = project_root / "frontend" / "public"
    images_dir = public_dir / "product-images"
    
    # Read the product data
    json_file = script_dir / "comprehensive_products_with_images.json"
    
    if not json_file.exists():
        print(f"Error: {json_file} not found!")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products = data.get('comprehensive_product_dataset', [])
    
    print(f"Generating placeholder images for {len(products)} products")
    
    # Track statistics
    generated_images = 0
    
    # Process each product
    for product_data in products:
        product = product_data.get('product_input', {})
        sku = product.get('sku', 'unknown')
        name = product.get('name', 'Unknown Product')
        category = product.get('category', 'accessories')
        images = product.get('images', [])
        
        print(f"\nProcessing {sku}")
        
        # Check which images need placeholders
        for i, image_url in enumerate(images):
            # Generate expected local filename
            filename = f"{sku.lower().replace('-', '_')}_{i + 1}.jpg"
            local_path = images_dir / filename
            
            # If local image doesn't exist, create placeholder
            if not local_path.exists():
                print(f"  Creating placeholder: {filename}")
                
                # Create placeholder image
                placeholder_img = create_placeholder_image(name, sku, category, filename)
                
                # Save the image
                placeholder_img.save(local_path, 'JPEG', quality=85)
                generated_images += 1
    
    print(f"\n{'='*50}")
    print(f"Placeholder Generation Summary:")
    print(f"Generated placeholder images: {generated_images}")
    print(f"Images stored in: {images_dir}")
    print(f"{'='*50}")

if __name__ == "__main__":
    print("Starting placeholder image generation...")
    generate_placeholder_images()
    print("Done!")
