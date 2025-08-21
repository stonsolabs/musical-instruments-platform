#!/usr/bin/env python3
"""
Script to verify that all product images are accessible and create a summary report.
"""

import json
import requests
import asyncio
import aiohttp
from typing import List, Dict, Any
import time

async def check_image_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """Check if an image URL is accessible."""
    try:
        async with session.head(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            return {
                "url": url,
                "status": response.status,
                "accessible": response.status == 200,
                "content_type": response.headers.get("content-type", ""),
                "content_length": response.headers.get("content-length", "")
            }
    except Exception as e:
        return {
            "url": url,
            "status": 0,
            "accessible": False,
            "error": str(e),
            "content_type": "",
            "content_length": ""
        }

async def verify_product_images():
    """Verify all product images and create a report."""
    print("🔍 Starting image verification process...")
    
    # Load product data
    with open("comprehensive_products_with_images.json", 'r') as f:
        data = json.load(f)
    
    products = data["comprehensive_product_dataset"]
    
    # Collect all image URLs
    all_images = []
    for product in products:
        product_input = product["product_input"]
        for image_url in product_input["images"]:
            all_images.append({
                "product_name": product_input["name"],
                "product_sku": product_input["sku"],
                "brand": product_input["brand"],
                "category": product_input["category"],
                "image_url": image_url
            })
    
    print(f"📊 Found {len(all_images)} images across {len(products)} products")
    
    # Verify images
    async with aiohttp.ClientSession() as session:
        verification_tasks = [
            check_image_url(session, img["image_url"]) 
            for img in all_images
        ]
        
        print("🔄 Checking image accessibility...")
        results = await asyncio.gather(*verification_tasks)
    
    # Combine results with product info
    verified_images = []
    for i, result in enumerate(results):
        verified_images.append({
            **all_images[i],
            **result
        })
    
    # Generate report
    accessible_count = sum(1 for img in verified_images if img["accessible"])
    inaccessible_count = len(verified_images) - accessible_count
    
    report = {
        "verification_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_images": len(verified_images),
            "accessible_images": accessible_count,
            "inaccessible_images": inaccessible_count,
            "success_rate": f"{(accessible_count / len(verified_images) * 100):.1f}%"
        },
        "by_category": {},
        "by_brand": {},
        "inaccessible_images": [],
        "all_results": verified_images
    }
    
    # Group by category
    for img in verified_images:
        category = img["category"]
        if category not in report["by_category"]:
            report["by_category"][category] = {"total": 0, "accessible": 0}
        report["by_category"][category]["total"] += 1
        if img["accessible"]:
            report["by_category"][category]["accessible"] += 1
    
    # Group by brand
    for img in verified_images:
        brand = img["brand"]
        if brand not in report["by_brand"]:
            report["by_brand"][brand] = {"total": 0, "accessible": 0}
        report["by_brand"][brand]["total"] += 1
        if img["accessible"]:
            report["by_brand"][brand]["accessible"] += 1
    
    # Collect inaccessible images
    report["inaccessible_images"] = [
        img for img in verified_images if not img["accessible"]
    ]
    
    # Save report
    with open("image_verification_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"\n📊 Image Verification Report")
    print(f"=" * 50)
    print(f"Total Images: {report['summary']['total_images']}")
    print(f"Accessible: {report['summary']['accessible_images']} ({report['summary']['success_rate']})")
    print(f"Inaccessible: {report['summary']['inaccessible_images']}")
    
    print(f"\n📈 By Category:")
    for category, stats in report["by_category"].items():
        success_rate = (stats["accessible"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"  {category}: {stats['accessible']}/{stats['total']} ({success_rate:.1f}%)")
    
    print(f"\n🏷️ By Brand:")
    for brand, stats in report["by_brand"].items():
        success_rate = (stats["accessible"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"  {brand}: {stats['accessible']}/{stats['total']} ({success_rate:.1f}%)")
    
    if report["inaccessible_images"]:
        print(f"\n❌ Inaccessible Images:")
        for img in report["inaccessible_images"][:5]:  # Show first 5
            print(f"  {img['product_name']}: {img['image_url']}")
            if "error" in img:
                print(f"    Error: {img['error']}")
        
        if len(report["inaccessible_images"]) > 5:
            print(f"  ... and {len(report['inaccessible_images']) - 5} more")
    
    print(f"\n📝 Full report saved to: image_verification_report.json")
    
    return report

if __name__ == "__main__":
    asyncio.run(verify_product_images())