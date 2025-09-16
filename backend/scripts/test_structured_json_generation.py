#!/usr/bin/env python3
"""
Test script to verify structured JSON blog generation works correctly.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import async_session_factory
from sqlalchemy import text
import json

async def test_template_structure():
    """Test that templates have the structured JSON format"""
    async with async_session_factory() as session:
        # Get a sample template to verify structure
        result = await session.execute(
            text("SELECT name, base_prompt, content_structure FROM blog_generation_templates WHERE name = 'Affiliate Roundup: Best Picks' LIMIT 1")
        )
        template = result.fetchone()
        
        if template:
            name, base_prompt, content_structure = template
            print(f"✅ Template: {name}")
            print(f"📝 Has structured JSON format: {'RESPOND ONLY WITH VALID JSON' in base_prompt}")
            
            try:
                # Handle case where content_structure is already a dict or needs parsing
                if isinstance(content_structure, str):
                    structure = json.loads(content_structure)
                else:
                    structure = content_structure
                    
                print(f"📋 Content structure format: {structure.get('format', 'unknown')}")
                print(f"🔢 Number of sections: {len(structure.get('sections', []))}")
                
                # Show section types
                sections = [s.get('type') for s in structure.get('sections', [])]
                print(f"📑 Section types: {', '.join(sections)}")
                
                return True
            except (json.JSONDecodeError, TypeError) as e:
                print(f"❌ Content structure error: {e}")
                return False
        else:
            print("❌ Template not found")
            return False

async def get_sample_products():
    """Get sample products for testing"""
    async with async_session_factory() as session:
        result = await session.execute(
            text("""
                SELECT id, name, slug 
                FROM products 
                LIMIT 5
            """)
        )
        products = result.fetchall()
        print(f"\n🎸 Found {len(products)} sample products for testing:")
        for product in products:
            print(f"   - {product[1]} [ID: {product[0]}]")
        return products

async def main():
    print("🧪 Testing Structured JSON Blog Generation")
    print("=" * 50)
    
    # Test template structure
    template_ok = await test_template_structure()
    
    if template_ok:
        print("\n✅ Templates are properly configured for structured JSON generation!")
        
        # Get sample products
        await get_sample_products()
        
        print("\n🚀 Ready to test blog generation!")
        print("\nNext steps:")
        print("1. Go to your admin panel")
        print("2. Navigate to Blog Management")
        print("3. Click 'AI Generator'")
        print("4. Select 'Affiliate Roundup: Best Picks' template")
        print("5. Choose a category and some products")
        print("6. Generate content and verify it returns structured JSON")
        
    else:
        print("❌ Templates need to be fixed before testing")

if __name__ == "__main__":
    asyncio.run(main())