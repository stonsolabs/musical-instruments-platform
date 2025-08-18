#!/usr/bin/env python3
"""
OpenAI Batch API Content Generation for Musical Instrument Products
Uses OpenAI's batch API for the most cost-effective processing of thousands of products.
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import openai

# Add the parent directory to the path to import app modules
sys.path.append('..')

from app.database import get_db_session
from app.models import Product
from app.config import settings


@dataclass
class BatchAPIConfig:
    """Configuration for OpenAI batch API processing."""
    batch_size: int = 100
    max_concurrent_batches: int = 3
    output_dir: str = "openai_batch_results"
    input_file: str = "batch_input.jsonl"
    results_file: str = "batch_results.jsonl"
    poll_interval: int = 60  # seconds


class OpenAIBatchContentGenerator:
    def __init__(self, config: BatchAPIConfig):
        self.config = config
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.stats = {
            "total_products": 0,
            "batches_created": 0,
            "batches_completed": 0,
            "products_processed": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "start_time": None,
            "end_time": None
        }
        
        # Create output directory
        Path(config.output_dir).mkdir(exist_ok=True)

    def _create_product_prompt(self, product: Product) -> str:
        """Create a standardized prompt for a product."""
        specs_str = ""
        if product.specifications:
            specs_str = "\n".join([f"- {k}: {v}" for k, v in product.specifications.items()])

        prompt = f"""
Generate comprehensive AI content for this musical instrument product.

Product: {product.name}
Brand: {product.brand.name}
Category: {product.category.name}
Subcategory: {product.category.name if not product.category.parent else product.category.parent.name}
Description: {product.description or 'No description available'}

Specifications:
{specs_str}

MSRP Price: €{product.msrp_price or 'N/A'}
Images: {len(product.images)} images available

Generate a JSON object with the following structure for the ai_generated_content field:

{{
  "basic_info": {{
    "overview": "2-3 sentence product overview",
    "key_features": ["feature1", "feature2", "feature3"],
    "target_skill_level": "Beginner|Intermediate|Advanced|Professional",
    "country_of_origin": "Country name",
    "release_year": "Year or 'Current Production'"
  }},
  "technical_analysis": {{
    "sound_characteristics": {{
      "tonal_profile": "Description of overall sound",
      "output_level": "Low|Medium|High",
      "best_genres": ["genre1", "genre2", "genre3"],
      "pickup_positions": {{
        "position_1": "Description"
      }}
    }},
    "build_quality": {{
      "construction_type": "Solid Body|Hollow|Semi-Hollow|etc",
      "hardware_quality": "Budget|Standard|Premium",
      "finish_quality": "Description of finish and aesthetics",
      "expected_durability": "Low|Medium|High"
    }},
    "playability": {{
      "neck_profile": "Description of neck feel",
      "action_setup": "Low|Medium|High action potential",
      "comfort_rating": "1-10 scale with description",
      "weight_category": "Light|Medium|Heavy with approximate kg"
    }}
  }},
  "purchase_decision": {{
    "why_buy": [
      {{
        "title": "Benefit title",
        "description": "Detailed explanation of this benefit"
      }}
    ],
    "why_not_buy": [
      {{
        "title": "Limitation title", 
        "description": "Detailed explanation of this limitation"
      }}
    ],
    "best_for": [
      {{
        "user_type": "User category",
        "reason": "Why this product suits them"
      }}
    ],
    "not_ideal_for": [
      {{
        "user_type": "User category",
        "reason": "Why this product may not suit them"
      }}
    ]
  }},
  "usage_guidance": {{
    "recommended_amplifiers": ["amp_type1", "amp_type2"],
    "suitable_music_styles": {{
      "excellent": ["style1", "style2"],
      "good": ["style3", "style4"],
      "limited": ["style5", "style6"]
    }},
    "skill_development": {{
      "learning_curve": "Easy|Moderate|Steep",
      "growth_potential": "Description of how long this instrument will serve the player"
    }}
  }},
  "maintenance_care": {{
    "maintenance_level": "Low|Medium|High",
    "common_issues": ["issue1", "issue2"],
    "care_instructions": {{
      "daily": "Brief daily care advice",
      "weekly": "Weekly maintenance tasks",
      "monthly": "Monthly maintenance tasks",
      "annual": "Annual professional service recommendations"
    }},
    "upgrade_potential": {{
      "easy_upgrades": ["upgrade1", "upgrade2"],
      "recommended_budget": "€X-Y for meaningful improvements"
    }}
  }},
  "professional_assessment": {{
    "expert_rating": {{
      "build_quality": "1-10",
      "sound_quality": "1-10", 
      "value_for_money": "1-10",
      "versatility": "1-10"
    }},
    "standout_features": ["feature1", "feature2"],
    "notable_limitations": ["limitation1", "limitation2"],
    "competitive_position": "How it stands against similar products in price range"
  }},
  "content_metadata": {{
    "generated_date": "{datetime.utcnow().isoformat()}",
    "content_version": "1.0",
    "seo_keywords": ["keyword1", "keyword2", "keyword3"],
    "readability_score": "Easy|Medium|Advanced",
    "word_count": "Approximate word count"
  }}
}}

Content Guidelines:
- Professional but accessible tone
- Factual and unbiased assessments
- Focus on practical benefits and limitations
- Use industry-standard terminology correctly
- Consider European market preferences
- Avoid excessive marketing language
- Base assessments on actual specifications provided

Respond with valid JSON only.
"""
        return prompt

    async def create_batch_input_file(self, products: List[Product]) -> str:
        """Create the input file for OpenAI batch API."""
        input_file_path = f"{self.config.output_dir}/{self.config.input_file}"
        
        with open(input_file_path, 'w') as f:
            for product in products:
                prompt = self._create_product_prompt(product)
                line = {
                    "custom_id": str(product.id),
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": "gpt-4-turbo-preview",
                        "messages": [
                            {
                                "role": "system",
                                "content": """You are an expert musical instrument content generator. Create comprehensive product profiles for musical instruments that will be stored in a PostgreSQL database with JSON fields. Generate detailed, SEO-optimized content that helps users make informed purchasing decisions.

Content Guidelines:
- Professional but accessible tone
- Factual and unbiased assessments
- Focus on practical benefits and limitations
- Use industry-standard terminology correctly
- Consider European market preferences
- Avoid excessive marketing language
- Base assessments on actual specifications provided

Always respond with valid JSON format only."""
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "max_tokens": 2000,
                        "temperature": 0.7
                    }
                }
                f.write(json.dumps(line) + '\n')
        
        print(f"📝 Created batch input file: {input_file_path}")
        return input_file_path

    async def submit_batch_job(self, input_file_path: str) -> str:
        """Submit a batch job to OpenAI."""
        try:
            with open(input_file_path, 'rb') as f:
                batch = await self.client.batches.create(
                    input_file=f,
                    endpoint="/v1/chat/completions",
                    completion_window="24h"
                )
            
            print(f"🚀 Submitted batch job: {batch.id}")
            return batch.id
            
        except Exception as e:
            print(f"❌ Failed to submit batch job: {str(e)}")
            raise

    async def monitor_batch_job(self, batch_id: str) -> Dict[str, Any]:
        """Monitor the progress of a batch job."""
        while True:
            try:
                batch = await self.client.batches.retrieve(batch_id)
                
                print(f"📊 Batch {batch_id} status: {batch.status}")
                if batch.status in ["completed", "failed", "expired", "cancelled"]:
                    return batch
                
                if batch.status == "validating":
                    print("⏳ Batch is being validated...")
                elif batch.status == "in_progress":
                    print(f"🔄 Batch is in progress... ({batch.progress}%)")
                
                await asyncio.sleep(self.config.poll_interval)
                
            except Exception as e:
                print(f"⚠️  Error monitoring batch: {str(e)}")
                await asyncio.sleep(self.config.poll_interval)

    async def download_batch_results(self, batch_id: str) -> str:
        """Download the results of a completed batch job."""
        try:
            batch = await self.client.batches.retrieve(batch_id)
            
            if batch.output_file_id:
                output_file = await self.client.files.retrieve(batch.output_file_id)
                content = await self.client.files.content(output_file.id)
                
                results_file_path = f"{self.config.output_dir}/batch_{batch_id}_results.jsonl"
                with open(results_file_path, 'wb') as f:
                    f.write(content)
                
                print(f"📥 Downloaded batch results: {results_file_path}")
                return results_file_path
            else:
                raise Exception("No output file available")
                
        except Exception as e:
            print(f"❌ Failed to download batch results: {str(e)}")
            raise

    async def process_batch_results(self, results_file_path: str) -> List[Dict[str, Any]]:
        """Process the batch results and update products."""
        processed_results = []
        
        with open(results_file_path, 'r') as f:
            for line in f:
                try:
                    result = json.loads(line.strip())
                    product_id = result.get('custom_id')
                    response = result.get('response', {})
                    
                    if response.get('status_code') == 200:
                        # Parse the AI response
                        response_body = json.loads(response.get('body', '{}'))
                        ai_content_text = response_body.get('choices', [{}])[0].get('message', {}).get('content', '')
                        
                        try:
                            ai_content = json.loads(ai_content_text)
                            
                            # Update product in database
                            async with get_db_session() as db:
                                stmt = select(Product).where(Product.id == int(product_id))
                                result_db = await db.execute(stmt)
                                product = result_db.scalars().first()
                                
                                if product:
                                    product.ai_generated_content = ai_content
                                    product.updated_at = datetime.utcnow()
                                    await db.commit()
                                    
                                    processed_results.append({
                                        "product_id": int(product_id),
                                        "product_name": product.name,
                                        "status": "success",
                                        "content_generated": True
                                    })
                                    self.stats["success"] += 1
                                else:
                                    processed_results.append({
                                        "product_id": int(product_id),
                                        "status": "failed",
                                        "error": "Product not found in database"
                                    })
                                    self.stats["failed"] += 1
                                    
                        except json.JSONDecodeError:
                            processed_results.append({
                                "product_id": int(product_id),
                                "status": "failed",
                                "error": "Invalid JSON in AI response"
                            })
                            self.stats["failed"] += 1
                    else:
                        processed_results.append({
                            "product_id": int(product_id),
                            "status": "failed",
                            "error": f"API error: {response.get('status_code')}"
                        })
                        self.stats["failed"] += 1
                        
                except Exception as e:
                    print(f"⚠️  Error processing result line: {str(e)}")
                    self.stats["failed"] += 1
        
        return processed_results

    async def process_all_products_batch(self, 
                                       category_filter: Optional[str] = None,
                                       brand_filter: Optional[str] = None,
                                       force_regenerate: bool = False) -> Dict[str, Any]:
        """Process all products using OpenAI batch API."""
        self.stats["start_time"] = datetime.now()
        
        # Get all products
        async with get_db_session() as db:
            stmt = select(Product).where(Product.is_active.is_(True))
            
            if category_filter:
                from app.models import Category
                stmt = stmt.join(Product.category).where(Category.slug == category_filter)
            
            if brand_filter:
                from app.models import Brand
                stmt = stmt.join(Product.brand).where(Brand.slug == brand_filter)
            
            result = await db.execute(stmt)
            all_products = result.scalars().all()
        
        # Filter out products that already have content (unless force_regenerate)
        if not force_regenerate:
            all_products = [p for p in all_products if not p.ai_generated_content]
        
        self.stats["total_products"] = len(all_products)
        print(f"🎯 Found {len(all_products)} products to process")
        
        if not all_products:
            return {"message": "No products found matching criteria"}
        
        # Split into batches
        batches = [all_products[i:i + self.config.batch_size] 
                  for i in range(0, len(all_products), self.config.batch_size)]
        
        print(f"📦 Processing {len(batches)} batches of {self.config.batch_size} products each")
        
        all_results = []
        
        # Process batches
        for batch_id, batch_products in enumerate(batches, 1):
            print(f"\n🔄 Processing batch {batch_id}/{len(batches)}")
            
            try:
                # Create input file for this batch
                input_file_path = await self.create_batch_input_file(batch_products)
                
                # Submit batch job
                batch_job_id = await self.submit_batch_job(input_file_path)
                self.stats["batches_created"] += 1
                
                # Monitor batch job
                batch_result = await self.monitor_batch_job(batch_job_id)
                
                if batch_result.status == "completed":
                    # Download and process results
                    results_file_path = await self.download_batch_results(batch_job_id)
                    batch_results = await self.process_batch_results(results_file_path)
                    all_results.extend(batch_results)
                    self.stats["batches_completed"] += 1
                    self.stats["products_processed"] += len(batch_products)
                else:
                    print(f"❌ Batch {batch_job_id} failed with status: {batch_result.status}")
                    self.stats["failed"] += len(batch_products)
                
            except Exception as e:
                print(f"❌ Error processing batch {batch_id}: {str(e)}")
                self.stats["failed"] += len(batch_products)
        
        self.stats["end_time"] = datetime.now()
        return await self._finalize_results(all_results)

    async def _finalize_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Finalize and save results."""
        # Calculate processing time
        if self.stats["start_time"] and self.stats["end_time"]:
            processing_time = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
            self.stats["processing_time_seconds"] = processing_time
            self.stats["products_per_minute"] = (self.stats["products_processed"] / processing_time) * 60
        
        # Save final results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"{self.config.output_dir}/openai_batch_results_{timestamp}.json"
        
        final_results = {
            "processing_config": {
                "batch_size": self.config.batch_size,
                "max_concurrent_batches": self.config.max_concurrent_batches,
                "poll_interval": self.config.poll_interval
            },
            "statistics": self.stats,
            "results": results
        }
        
        with open(results_file, 'w') as f:
            json.dump(final_results, f, indent=2, default=str)
        
        print(f"💾 Final results saved to: {results_file}")
        
        return final_results

    def print_stats(self):
        """Print processing statistics."""
        print("\n" + "="*60)
        print("📊 OPENAI BATCH API PROCESSING STATISTICS")
        print("="*60)
        print(f"Total products: {self.stats['total_products']}")
        print(f"Batches created: {self.stats['batches_created']}")
        print(f"Batches completed: {self.stats['batches_completed']}")
        print(f"Products processed: {self.stats['products_processed']}")
        print(f"Successful: {self.stats['success']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped: {self.stats['skipped']}")
        
        if "processing_time_seconds" in self.stats:
            print(f"Processing time: {self.stats['processing_time_seconds']:.2f} seconds")
            print(f"Products per minute: {self.stats['products_per_minute']:.2f}")
        
        print("="*60)


async def main():
    """Main function to run the OpenAI batch content generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenAI Batch API content generation for musical instruments")
    parser.add_argument("--all", action="store_true", help="Generate content for all products")
    parser.add_argument("--category", type=str, help="Filter by category slug")
    parser.add_argument("--brand", type=str, help="Filter by brand slug")
    parser.add_argument("--force", action="store_true", help="Force regeneration of existing content")
    
    # Batch processing options
    parser.add_argument("--batch-size", type=int, default=100, help="Number of products per batch")
    parser.add_argument("--poll-interval", type=int, default=60, help="Poll interval for batch status (seconds)")
    parser.add_argument("--output-dir", type=str, default="openai_batch_results", help="Output directory for results")
    
    args = parser.parse_args()
    
    # Create batch configuration
    config = BatchAPIConfig(
        batch_size=args.batch_size,
        poll_interval=args.poll_interval,
        output_dir=args.output_dir
    )
    
    generator = OpenAIBatchContentGenerator(config)
    
    try:
        if args.all:
            # Generate for all products
            result = await generator.process_all_products_batch(
                category_filter=args.category,
                brand_filter=args.brand,
                force_regenerate=args.force
            )
        else:
            print("❌ Please specify --all")
            return
        
        generator.print_stats()
        
    except KeyboardInterrupt:
        print("\n⏹️  Batch processing interrupted by user")
        generator.print_stats()
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        generator.print_stats()


if __name__ == "__main__":
    asyncio.run(main())
