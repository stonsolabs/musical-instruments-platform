#!/usr/bin/env python3
"""
Localization Cleanup Migration Script

This script will:
1. Extract en-GB content from localized_content
2. Flatten it to root level of content JSON
3. Remove all localization references
4. Test on a small sample first

Usage:
    python cleanup_localization.py --test  # Test on 10 products
    python cleanup_localization.py --execute  # Run full migration
    python cleanup_localization.py --rollback  # Rollback changes
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.database import async_session_factory
from sqlalchemy import text
import argparse


class LocalizationCleanup:
    def __init__(self):
        self.test_mode = False
        self.rollback_data = []
    
    async def get_sample_products(self, limit: int = 10) -> List[Dict]:
        """Get a sample of products with localized content for testing"""
        async with async_session_factory() as session:
            result = await session.execute(text("""
                SELECT id, name, content 
                FROM products 
                WHERE content ? 'localized_content'
                LIMIT :limit
            """), {"limit": limit})
            
            return [{"id": row.id, "name": row.name, "content": row.content} for row in result]
    
    async def analyze_content_structure(self, products: List[Dict]) -> Dict[str, Any]:
        """Analyze the current content structure"""
        analysis = {
            "total_products": len(products),
            "has_localized_content": 0,
            "languages_found": set(),
            "content_sections": set(),
            "sample_structures": []
        }
        
        for product in products:
            content = product["content"]
            
            if "localized_content" in content:
                analysis["has_localized_content"] += 1
                localized = content["localized_content"]
                
                # Find languages
                if isinstance(localized, dict):
                    analysis["languages_found"].update(localized.keys())
                    
                    # Find content sections
                    for lang, lang_content in localized.items():
                        if isinstance(lang_content, dict):
                            analysis["content_sections"].update(lang_content.keys())
                
                # Store sample structure (first 3 products)
                if len(analysis["sample_structures"]) < 3:
                    analysis["sample_structures"].append({
                        "id": product["id"],
                        "name": product["name"],
                        "languages": list(localized.keys()) if isinstance(localized, dict) else [],
                        "has_en_gb": "en-GB" in localized if isinstance(localized, dict) else False,
                        "has_en_us": "en-US" in localized if isinstance(localized, dict) else False
                    })
        
        analysis["languages_found"] = list(analysis["languages_found"])
        analysis["content_sections"] = list(analysis["content_sections"])
        
        return analysis
    
    def extract_en_gb_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract en-GB content and flatten to root level"""
        if "localized_content" not in content:
            return content
        
        localized = content["localized_content"]
        
        # Try to get en-GB content, with fallbacks
        en_gb_content = None
        if isinstance(localized, dict):
            en_gb_content = (
                localized.get("en-GB") or 
                localized.get("en-US") or 
                localized.get("en")
            )
        
        if not en_gb_content:
            print(f"Warning: No English content found in localized_content")
            return content
        
        # Create new content structure
        new_content = {}
        
        # Keep existing non-localized fields
        for key, value in content.items():
            if key not in ["localized_content", "language", "locale", "lang"]:
                new_content[key] = value
        
        # Add en-GB content at root level
        if isinstance(en_gb_content, dict):
            new_content.update(en_gb_content)
        else:
            print(f"Warning: en-GB content is not a dict: {type(en_gb_content)}")
        
        return new_content
    
    async def test_migration(self, limit: int = 10) -> Dict[str, Any]:
        """Test the migration on a small sample"""
        print(f"🧪 Testing localization cleanup on {limit} products...")
        
        # Get sample products
        products = await self.get_sample_products(limit)
        if not products:
            print("❌ No products with localized content found")
            return {}
        
        print(f"📊 Found {len(products)} products with localized content")
        
        # Analyze current structure
        analysis = await self.analyze_content_structure(products)
        
        print(f"\n📈 Analysis Results:")
        print(f"  - Products with localized_content: {analysis['has_localized_content']}")
        print(f"  - Languages found: {analysis['languages_found']}")
        print(f"  - Content sections: {analysis['content_sections']}")
        
        print(f"\n🔍 Sample Product Structures:")
        for sample in analysis["sample_structures"]:
            print(f"  - ID {sample['id']}: {sample['name']}")
            print(f"    Languages: {sample['languages']}")
            print(f"    Has en-GB: {sample['has_en_gb']}, Has en-US: {sample['has_en_us']}")
        
        # Test migration on first product
        if products:
            test_product = products[0]
            original_content = test_product["content"]
            migrated_content = self.extract_en_gb_content(original_content.copy())
            
            print(f"\n🔄 Migration Test (Product ID: {test_product['id']}):")
            print(f"  Original keys: {list(original_content.keys())}")
            print(f"  Migrated keys: {list(migrated_content.keys())}")
            
            # Check if localized_content was removed
            has_localized_after = "localized_content" in migrated_content
            print(f"  localized_content removed: {not has_localized_after}")
            
            # Check if content sections were preserved
            original_sections = set()
            if "localized_content" in original_content:
                localized = original_content["localized_content"]
                if isinstance(localized, dict) and "en-GB" in localized:
                    original_sections.update(localized["en-GB"].keys())
            
            migrated_sections = set(migrated_content.keys())
            preserved_sections = original_sections.intersection(migrated_sections)
            print(f"  Content sections preserved: {len(preserved_sections)}/{len(original_sections)}")
            print(f"  Preserved sections: {list(preserved_sections)}")
        
        return analysis
    
    async def execute_migration(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Execute the full migration"""
        print(f"🚀 Executing localization cleanup migration...")
        
        # Get products to migrate
        if limit:
            products = await self.get_sample_products(limit)
            print(f"📊 Migrating {len(products)} products (test mode)")
        else:
            # Get all products with localized content
            async with async_session_factory() as session:
                result = await session.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM products 
                    WHERE content ? 'localized_content'
                """))
                count = result.fetchone().count
                print(f"📊 Found {count} products with localized content")
        
        # Execute migration
        async with async_session_factory() as session:
            # Step 1: Extract en-GB content and flatten
            result1 = await session.execute(text("""
                UPDATE products 
                SET content = (
                    -- Keep existing non-localized fields
                    content - 'localized_content' - 'language' - 'locale' - 'lang'
                ) || (
                    -- Add en-GB content at root level
                    COALESCE(
                        content->'localized_content'->'en-GB',
                        content->'localized_content'->'en-US',
                        content->'localized_content'->'en'
                    )
                )
                WHERE content ? 'localized_content'
            """))
            
            # Step 2: Clean up any remaining language references
            result2 = await session.execute(text("""
                UPDATE products 
                SET content = content - 'language' - 'locale' - 'lang' - 'localized_content'
                WHERE content ? 'language' OR content ? 'locale' OR content ? 'lang' OR content ? 'localized_content'
            """))
            
            await session.commit()
            
            print(f"✅ Migration completed successfully")
            print(f"  - Step 1: Updated {result1.rowcount} products")
            print(f"  - Step 2: Cleaned {result2.rowcount} products")
        
        return {"success": True, "updated": result1.rowcount, "cleaned": result2.rowcount}
    
    async def verify_migration(self) -> Dict[str, Any]:
        """Verify the migration was successful"""
        print(f"🔍 Verifying migration results...")
        
        async with async_session_factory() as session:
            # Check for remaining localized content
            result = await session.execute(text("""
                SELECT COUNT(*) as count 
                FROM products 
                WHERE content ? 'localized_content'
            """))
            remaining_localized = result.fetchone().count
            
            # Check for language references
            result = await session.execute(text("""
                SELECT COUNT(*) as count 
                FROM products 
                WHERE content ? 'language' OR content ? 'locale' OR content ? 'lang'
            """))
            remaining_lang_refs = result.fetchone().count
            
            # Get sample of migrated products
            result = await session.execute(text("""
                SELECT id, name, content 
                FROM products 
                WHERE content ? 'basic_info' OR content ? 'technical_analysis'
                LIMIT 5
            """))
            sample_products = [{"id": row.id, "name": row.name, "content": row.content} for row in result]
        
        print(f"📊 Verification Results:")
        print(f"  - Products with remaining localized_content: {remaining_localized}")
        print(f"  - Products with language references: {remaining_lang_refs}")
        print(f"  - Sample migrated products: {len(sample_products)}")
        
        for product in sample_products:
            content_keys = list(product["content"].keys())
            print(f"    - ID {product['id']}: {product['name']}")
            print(f"      Content keys: {content_keys[:10]}{'...' if len(content_keys) > 10 else ''}")
        
        return {
            "remaining_localized": remaining_localized,
            "remaining_lang_refs": remaining_lang_refs,
            "sample_products": sample_products
        }


async def main():
    parser = argparse.ArgumentParser(description="Localization Cleanup Migration")
    parser.add_argument("--test", action="store_true", help="Test migration on small sample")
    parser.add_argument("--execute", action="store_true", help="Execute full migration")
    parser.add_argument("--verify", action="store_true", help="Verify migration results")
    parser.add_argument("--limit", type=int, default=10, help="Limit for test mode")
    
    args = parser.parse_args()
    
    cleanup = LocalizationCleanup()
    
    if args.test:
        await cleanup.test_migration(args.limit)
    elif args.execute:
        await cleanup.execute_migration()
        await cleanup.verify_migration()
    elif args.verify:
        await cleanup.verify_migration()
    else:
        print("Please specify --test, --execute, or --verify")
        print("Example: python cleanup_localization.py --test")


if __name__ == "__main__":
    asyncio.run(main())
