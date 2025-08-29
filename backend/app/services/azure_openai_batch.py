import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

import aiohttp
import openai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from ..config import settings
from ..models import Product, Brand, Category, OpenAIBatch
from ..database import get_db


class AzureOpenAIBatchProcessor:
    def __init__(self) -> None:
        self.client = openai.AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.AZURE_OPENAI_ENDPOINT
        )
        self.batch_dir = Path("batch_files")
        self.batch_dir.mkdir(exist_ok=True)

    async def create_batch_file(self, products: List[Product], batch_id: str) -> str:
        """Create a batch file for Azure OpenAI processing."""
        batch_items = []
        
        for product in products:
            # Build product input JSON
            product_input = await self._build_product_input(product)
            
            # Create batch item
            batch_item = {
                "custom_id": f"prod-{product.id}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                    "messages": [
                        {
                            "role": "system",
                            "content": self._get_system_prompt()
                        },
                        {
                            "role": "user",
                            "content": json.dumps(product_input)
                        }
                    ],
                    "response_format": {
                        "type": "json_schema",
                        "json_schema": self._get_json_schema()
                    },
                    "max_tokens": 4000,
                    "temperature": 0.7
                }
            }
            batch_items.append(batch_item)
        
        # Save batch file
        filename = f"batch_{batch_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        filepath = self.batch_dir / filename
        
        with open(filepath, 'w') as f:
            for item in batch_items:
                f.write(json.dumps(item) + '\n')
        
        return str(filepath)

    async def submit_batch(self, filepath: str, batch_id: str) -> str:
        """Submit batch file to Azure OpenAI."""
        try:
            with open(filepath, 'rb') as f:
                response = await self.client.batches.create(
                    input_file=f,
                    endpoint="/v1/chat/completions",
                    completion_window="24h"
                )
            
            # Update batch record
            async with get_db() as db:
                await db.execute(
                    update(OpenAIBatch)
                    .where(OpenAIBatch.batch_id == batch_id)
                    .values(
                        openai_job_id=response.id,
                        status='processing'
                    )
                )
                await db.commit()
            
            return response.id
            
        except Exception as e:
            # Update batch record with error
            async with get_db() as db:
                await db.execute(
                    update(OpenAIBatch)
                    .where(OpenAIBatch.batch_id == batch_id)
                    .values(
                        status='failed',
                        error_message=str(e)
                    )
                )
                await db.commit()
            raise

    async def check_batch_status(self, batch_id: str) -> Dict[str, Any]:
        """Check the status of a batch job."""
        async with get_db() as db:
            result = await db.execute(
                select(OpenAIBatch).where(OpenAIBatch.batch_id == batch_id)
            )
            batch_record = result.scalar_one_or_none()
            
            if not batch_record or not batch_record.openai_job_id:
                return {"status": "not_found"}
            
            try:
                response = await self.client.batches.retrieve(batch_record.openai_job_id)
                
                # Update batch record
                await db.execute(
                    update(OpenAIBatch)
                    .where(OpenAIBatch.batch_id == batch_id)
                    .values(
                        status=response.status,
                        result_file=response.output_file_id if response.output_file_id else None,
                        completed_at=datetime.utcnow() if response.status in ['completed', 'failed'] else None
                    )
                )
                await db.commit()
                
                return {
                    "status": response.status,
                    "request_counts": response.request_counts,
                    "output_file_id": response.output_file_id
                }
                
            except Exception as e:
                return {"status": "error", "error": str(e)}

    async def download_and_process_results(self, batch_id: str) -> Dict[str, Any]:
        """Download batch results and process them."""
        async with get_db() as db:
            result = await db.execute(
                select(OpenAIBatch).where(OpenAIBatch.batch_id == batch_id)
            )
            batch_record = result.scalar_one_or_none()
            
            if not batch_record or not batch_record.result_file:
                raise ValueError("No result file available")
            
            try:
                # Download result file
                response = await self.client.files.content(batch_record.result_file)
                result_data = response.content.decode('utf-8')
                
                # Process results
                processed_count = 0
                error_count = 0
                
                for line in result_data.strip().split('\n'):
                    if not line:
                        continue
                    
                    try:
                        result_item = json.loads(line)
                        await self._process_batch_result(result_item, db)
                        processed_count += 1
                    except Exception as e:
                        error_count += 1
                        print(f"Error processing result: {e}")
                
                # Update batch record
                await db.execute(
                    update(OpenAIBatch)
                    .where(OpenAIBatch.batch_id == batch_id)
                    .values(
                        status='completed',
                        completed_at=datetime.utcnow()
                    )
                )
                await db.commit()
                
                return {
                    "processed_count": processed_count,
                    "error_count": error_count,
                    "total_count": processed_count + error_count
                }
                
            except Exception as e:
                await db.execute(
                    update(OpenAIBatch)
                    .where(OpenAIBatch.batch_id == batch_id)
                    .values(
                        status='failed',
                        error_message=str(e)
                    )
                )
                await db.commit()
                raise

    async def _process_batch_result(self, result_item: Dict[str, Any], db: AsyncSession) -> None:
        """Process a single batch result and update the product."""
        try:
            custom_id = result_item.get('custom_id', '')
            product_id = int(custom_id.replace('prod-', ''))
            
            if result_item.get('status') == 'completed':
                response_body = result_item.get('response', {}).get('body', {})
                choices = response_body.get('choices', [])
                
                if choices:
                    content = choices[0].get('message', {}).get('content', '')
                    if content:
                        ai_content = json.loads(content)
                        
                        # Update product with AI content
                        await db.execute(
                            update(Product)
                            .where(Product.id == product_id)
                            .values(
                                ai_generated_content=ai_content,
                                openai_processing_status='completed',
                                openai_processed_at=datetime.utcnow()
                            )
                        )
            else:
                # Handle error
                await db.execute(
                    update(Product)
                    .where(Product.id == product_id)
                    .values(
                        openai_processing_status='failed',
                        openai_error_message=result_item.get('error', {}).get('message', 'Unknown error')
                    )
                )
                
        except Exception as e:
            print(f"Error processing batch result for {result_item.get('custom_id', 'unknown')}: {e}")

    async def _build_product_input(self, product: Product) -> Dict[str, Any]:
        """Build product input JSON for the AI model."""
        # Get brand and category names
        async with get_db() as db:
            brand_result = await db.execute(select(Brand).where(Brand.id == product.brand_id))
            brand = brand_result.scalar_one()
            
            category_result = await db.execute(select(Category).where(Category.id == product.category_id))
            category = category_result.scalar_one()
        
        # Build store links (placeholder for now)
        store_links = {
            "thomann": {"product_url": None, "ref_id": None},
            "gear4music": {"product_url": None, "ref_id": None},
            "sweetwater": {"product_url": None, "ref_id": None},
            "guitarcenter": {"product_url": None, "ref_id": None},
            "andertons": {"product_url": None, "ref_id": None},
            "reverb": {"product_url": None, "ref_id": None},
            "amazon": {"product_url": None, "ref_id": None},
            "official_store": {"product_url": None, "ref_id": None},
            "guitarguitar": {"product_url": None, "ref_id": None},
            "muziker": {"product_url": None, "ref_id": None},
            "music_store": {"product_url": None, "ref_id": None},
            "strumenti_musicali": {"product_url": None, "ref_id": None}
        }
        
        return {
            "name": product.name,
            "slug": product.slug,
            "brand": brand.name if brand else "Unknown",
            "category": category.name if category else "Unknown",
            "description": product.description or "",
            "msrp_price": float(product.msrp_price) if product.msrp_price else None,
            "url_source": "",  # Will be populated from affiliate links
            "image_uri": product.images[0] if product.images else None,
            "specs": product.specifications,
            "store_links": store_links
        }

    def _get_system_prompt(self) -> str:
        """Get the system prompt for AI content generation."""
        prompt_path = Path(__file__).parent.parent.parent / "openai" / "batch_prompt.txt"
        if prompt_path.exists():
            return prompt_path.read_text()
        else:
            return """You are an expert product data enrichment engine for musical instruments.

Generate comprehensive product content including:
- Basic information and key features
- Technical analysis and specifications
- Purchase decision guidance
- Usage recommendations
- Maintenance instructions
- Professional assessment

Provide content in multiple locales (en-US, en-GB, es-ES, fr-FR, de-DE, it-IT, pt-PT).
Return only valid JSON matching the provided schema."""

    def _get_json_schema(self) -> Dict[str, Any]:
        """Get the JSON schema for validation."""
        schema_path = Path(__file__).parent.parent.parent / "openai" / "json_schema.json"
        if schema_path.exists():
            return json.loads(schema_path.read_text())
        else:
            return {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "properties": {
                    "product_input": {"type": "object"},
                    "images": {"type": "object"},
                    "ai_generated_content": {"type": "object"},
                    "customer_reviews": {"type": "object"},
                    "content_metadata": {"type": "object"},
                    "qa": {"type": "object"}
                }
            }

    async def get_products_for_batch(self, category_limit: int = 3) -> List[Product]:
        """Get products for batch processing, 3 from each category."""
        async with get_db() as db:
            # Get all categories
            categories_result = await db.execute(select(Category).where(Category.is_active == True))
            categories = categories_result.scalars().all()
            
            products = []
            for category in categories:
                # Get 3 products from each category that haven't been processed
                category_products_result = await db.execute(
                    select(Product)
                    .where(
                        Product.category_id == category.id,
                        Product.is_active == True,
                        Product.openai_processing_status.in_(['pending', 'failed'])
                    )
                    .limit(category_limit)
                )
                category_products = category_products_result.scalars().all()
                products.extend(category_products)
            
            return products

    async def create_test_batch(self, products_per_category: int = 5) -> List[Product]:
        """Create a test batch with 5 products from each category for testing."""
        async with get_db() as db:
            # Get all categories
            categories_result = await db.execute(select(Category).where(Category.is_active == True))
            categories = categories_result.scalars().all()
            
            products = []
            for category in categories:
                # Get 5 products from each category
                category_products_result = await db.execute(
                    select(Product)
                    .where(
                        Product.category_id == category.id,
                        Product.is_active == True
                    )
                    .limit(products_per_category)
                )
                category_products = category_products_result.scalars().all()
                products.extend(category_products)
            
            return products
