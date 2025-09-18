#!/usr/bin/env python3
"""
Update Blog Templates Script - Make templates generate evergreen content
Removes year references from blog generation templates
"""

import asyncio
import sys
import os
import re

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

class TemplateUpdater:
    def __init__(self):
        self.updated_count = 0
        self.errors = []
    
    def clean_prompt(self, prompt: str) -> str:
        """Clean prompt by removing year references and making it evergreen"""
        # Remove year references like "2024", "2025", etc.
        prompt = re.sub(r'\s+(20\d{2})\s*', ' ', prompt)
        prompt = re.sub(r'\s+(20\d{2})$', '', prompt)
        prompt = re.sub(r'^(20\d{2})\s+', '', prompt)
        
        # Remove "current year" references
        prompt = re.sub(r'\bcurrent year\b', 'today', prompt, flags=re.IGNORECASE)
        prompt = re.sub(r'\bthis year\b', 'today', prompt, flags=re.IGNORECASE)
        
        # Remove "latest" year references
        prompt = re.sub(r'\blatest\s+(20\d{2})\b', 'latest', prompt, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        prompt = re.sub(r'\s+', ' ', prompt).strip()
        
        return prompt
    
    async def update_templates(self):
        """Update all blog generation templates to be evergreen"""
        print("🌱 Updating blog templates to generate evergreen content...")
        
        async with async_session_factory() as session:
            # Get all active templates
            result = await session.execute(text("""
                SELECT id, name, base_prompt, system_prompt, product_context_prompt
                FROM blog_generation_templates 
                WHERE is_active = true
                ORDER BY id
            """))
            
            templates = result.fetchall()
            print(f"Found {len(templates)} templates to check")
            
            for template in templates:
                template_id, name, base_prompt, system_prompt, product_context_prompt = template
                
                # Clean all prompt fields
                cleaned_base = self.clean_prompt(base_prompt) if base_prompt else base_prompt
                cleaned_system = self.clean_prompt(system_prompt) if system_prompt else system_prompt
                cleaned_product = self.clean_prompt(product_context_prompt) if product_context_prompt else product_context_prompt
                
                # Check if any changes were made
                if (cleaned_base != base_prompt or 
                    cleaned_system != system_prompt or 
                    cleaned_product != product_context_prompt):
                    
                    try:
                        # Update the template
                        await session.execute(text("""
                            UPDATE blog_generation_templates 
                            SET base_prompt = :base_prompt, 
                                system_prompt = :system_prompt,
                                product_context_prompt = :product_context_prompt,
                                updated_at = NOW()
                            WHERE id = :id
                        """), {
                            'base_prompt': cleaned_base,
                            'system_prompt': cleaned_system,
                            'product_context_prompt': cleaned_product,
                            'id': template_id
                        })
                        
                        self.updated_count += 1
                        print(f"✅ Updated template {template_id}: {name}")
                        
                        # Show what changed
                        if cleaned_base != base_prompt:
                            print(f"   Base prompt: {base_prompt[:100]}... → {cleaned_base[:100]}...")
                        if cleaned_system != system_prompt:
                            print(f"   System prompt: {system_prompt[:100]}... → {cleaned_system[:100]}...")
                        if cleaned_product != product_context_prompt:
                            print(f"   Product context: {product_context_prompt[:100]}... → {cleaned_product[:100]}...")
                        
                    except Exception as e:
                        error_msg = f"Error updating template {template_id}: {str(e)}"
                        self.errors.append(error_msg)
                        print(f"❌ {error_msg}")
            
            await session.commit()
        
        print(f"\n🎉 Template updating completed!")
        print(f"✅ Updated: {self.updated_count} templates")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.errors:
            print("\nErrors encountered:")
            for error in self.errors:
                print(f"  - {error}")

async def main():
    updater = TemplateUpdater()
    await updater.update_templates()

if __name__ == "__main__":
    asyncio.run(main())
