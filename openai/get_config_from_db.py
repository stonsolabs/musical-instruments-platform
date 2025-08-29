#!/usr/bin/env python3
"""
Utility module to retrieve configuration files from database.
"""
import asyncio
from pathlib import Path
from sqlalchemy import text
from database import get_async_session

async def get_batch_prompt_from_db() -> str:
    """Get batch prompt from database."""
    async with await get_async_session() as session:
        result = await session.execute(
            text("SELECT content FROM config_files WHERE filename = 'batch_prompt.txt'")
        )
        row = result.fetchone()
        return row.content if row else None

async def get_json_schema_from_db() -> str:
    """Get JSON schema from database."""
    async with await get_async_session() as session:
        result = await session.execute(
            text("SELECT content FROM config_files WHERE filename = 'json_schema_v2.json'")
        )
        row = result.fetchone()
        return row.content if row else None

def get_batch_prompt() -> str:
    """Get batch prompt from file or database."""
    prompt_path = Path(__file__).parent / "batch_prompt.txt"
    if prompt_path.exists():
        return prompt_path.read_text()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_batch_prompt_from_db())
        loop.close()
        if result:
            return result
    except Exception as e:
        print(f"Error retrieving prompt from database: {str(e)}")
    return """You are an expert product data enrichment engine for musical instruments. Your task is to analyze product information and generate comprehensive, accurate content for e-commerce platforms.

TASKS:

1. BRAND & CATEGORY IDENTIFICATION:
   - Identify the brand from the product name and description
   - Assign the most appropriate category from: Electric Guitars, Electric Basses, Steel String Acoustic Guitars, Travel Guitars, Digital Pianos, Stage Pianos, Home Keyboards, Entertainer Keyboards, MIDI Master Keyboards, Synthesizer Keyboards, Workstations, Electric Organs, Turntables, Studio Equipment, Acoustic Guitar, Acoustic Piano, Synthesizer, Drum Kit, Electronic Drums, Microphone, Amplifier, Effects Pedal, DJ Equipment, PA System, Accessories, String Instrument, Wind Instrument, Percussion Instrument, Unknown
   - If brand is not clearly identifiable, use "Unknown" but try to extract any brand hints

2. TECHNICAL SPECIFICATIONS:
   Generate comprehensive technical specifications based on the category:
   - For guitars: Body material, neck material, fingerboard, pickups, controls, bridge type, scale length, etc.
   - For keyboards: Key count, action type, polyphony, built-in sounds, connectivity, etc.
   - For drums: Shell material, sizes, hardware, heads, etc.
   - For microphones: Type, polar pattern, frequency response, connectivity, etc.
   - For amplifiers: Power output, channels, effects, connectivity, etc.
   - For effects: Effect type, parameters, bypass options, power requirements, etc.

3. STORE LINKS:
   Generate realistic store links for: Thomann, Gear4Music, Sweetwater, GuitarCenter, Andertons, Amazon, Official Store
   - Use the product name and brand to create plausible URLs
   - Format: https://store.com/brand/product-name
   - If brand is unknown, use generic format

4. IMAGES:
   Generate image descriptions for: front_view, back_view, official_image
   - Describe what each image should show
   - Include key features and angles

5. LOCALIZED CONTENT:
   Create content for en-US, en-GB, es-ES, fr-FR, de-DE, it-IT, pt-PT including:
   - basic_info: Concise product overview
   - technical_analysis: Detailed technical breakdown
   - purchase_decision: Buying guidance
   - usage_guidance: How to use the product
   - maintenance_care: Care and maintenance tips
   - professional_assessment: Expert evaluation
   - customer_reviews: Realistic customer feedback

6. PRODUCT IDENTIFIERS:
   Generate or extract: sku, gtin12, gtin13, gtin14, upc, ean, mpn, isbn
   - Use existing SKU if provided
   - Generate realistic identifiers based on product type

7. METADATA:
   - content_metadata: Content generation details
   - qa: Common questions and answers
   - dates: Creation and update timestamps
   - sources: Data sources and references

STRICT REQUIREMENTS:
- All content must be accurate and realistic
- Technical specifications must be plausible for the product type
- Store links must follow real e-commerce URL patterns
- Localized content must be culturally appropriate
- Product identifiers must follow standard formats
- All dates must be current
- Content must be comprehensive but not repetitive

OUTPUT: Return a single JSON object that strictly validates against the provided JSON schema. JSON only."""

def get_json_schema() -> str:
    """Get JSON schema from file or database."""
    schema_path = Path(__file__).parent / "json_schema_v2.json"
    if schema_path.exists():
        return schema_path.read_text()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_json_schema_from_db())
        loop.close()
        if result:
            return result
    except Exception as e:
        print(f"Error retrieving schema from database: {str(e)}")
    return "{}"
