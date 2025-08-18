from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List

import openai

from ..config import settings
from ..models import Product


class AIContentGenerator:
    def __init__(self) -> None:
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_product_content(self, product: Product) -> Dict[str, Any]:
        """Generate comprehensive AI content for a musical instrument product."""
        context = self._build_product_context(product)
        
        # Generate all content sections
        basic_info = await self._generate_basic_info(context)
        technical_analysis = await self._generate_technical_analysis(context)
        purchase_decision = await self._generate_purchase_decision(context)
        usage_guidance = await self._generate_usage_guidance(context)
        maintenance_care = await self._generate_maintenance_care(context)
        professional_assessment = await self._generate_professional_assessment(context)
        
        # Create content metadata
        content_metadata = self._create_content_metadata()
        
        return {
            "basic_info": basic_info,
            "technical_analysis": technical_analysis,
            "purchase_decision": purchase_decision,
            "usage_guidance": usage_guidance,
            "maintenance_care": maintenance_care,
            "professional_assessment": professional_assessment,
            "content_metadata": content_metadata
        }

    def _build_product_context(self, product: Product) -> str:
        """Build comprehensive product context for AI generation."""
        specs_str = ""
        if product.specifications:
            specs_str = "\n".join([f"- {k}: {v}" for k, v in product.specifications.items()])

        context = f"""
Product: {product.name}
Brand: {product.brand.name}
Category: {product.category.name}
Subcategory: {product.category.name if not product.category.parent else product.category.parent.name}
Description: {product.description or 'No description available'}

Specifications:
{specs_str}

MSRP Price: €{product.msrp_price or 'N/A'}
Images: {len(product.images)} images available
"""
        return context

    async def _generate_basic_info(self, context: str) -> Dict[str, Any]:
        """Generate basic product information."""
        prompt = f"""
Generate basic information for this musical instrument product.

{context}

Provide a JSON response with:
- overview: 2-3 sentence product overview
- key_features: array of 3-5 key features
- target_skill_level: "Beginner", "Intermediate", "Advanced", or "Professional"
- country_of_origin: country name or "Various" if unknown
- release_year: year or "Current Production"

Respond in valid JSON format only.
"""
        
        response = await self._make_ai_request(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "overview": "A quality musical instrument suitable for various playing styles.",
                "key_features": ["Quality construction", "Versatile sound", "Good value"],
                "target_skill_level": "Intermediate",
                "country_of_origin": "Various",
                "release_year": "Current Production"
            }

    async def _generate_technical_analysis(self, context: str) -> Dict[str, Any]:
        """Generate technical analysis of the product."""
        prompt = f"""
Provide a comprehensive technical analysis of this musical instrument.

{context}

Generate JSON with:
- sound_characteristics: tonal_profile, output_level (Low/Medium/High), best_genres array, pickup_positions object
- build_quality: construction_type, hardware_quality (Budget/Standard/Premium), finish_quality, expected_durability (Low/Medium/High)
- playability: neck_profile, action_setup (Low/Medium/High), comfort_rating (1-10 with description), weight_category

Respond in valid JSON format only.
"""
        
        response = await self._make_ai_request(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "sound_characteristics": {
                    "tonal_profile": "Versatile with good clarity",
                    "output_level": "Medium",
                    "best_genres": ["Rock", "Pop", "Blues"],
                    "pickup_positions": {"position_1": "Bright and clear"}
                },
                "build_quality": {
                    "construction_type": "Solid Body",
                    "hardware_quality": "Standard",
                    "finish_quality": "Professional finish",
                    "expected_durability": "Medium"
                },
                "playability": {
                    "neck_profile": "Comfortable C-shape",
                    "action_setup": "Medium",
                    "comfort_rating": "7/10 - Good for extended playing",
                    "weight_category": "Medium (3.5kg)"
                }
            }

    async def _generate_purchase_decision(self, context: str) -> Dict[str, Any]:
        """Generate purchase decision guidance."""
        prompt = f"""
Provide purchase decision guidance for this musical instrument.

{context}

Generate JSON with:
- why_buy: array of objects with title and description
- why_not_buy: array of objects with title and description  
- best_for: array of objects with user_type and reason
- not_ideal_for: array of objects with user_type and reason

Respond in valid JSON format only.
"""
        
        response = await self._make_ai_request(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "why_buy": [
                    {"title": "Quality Construction", "description": "Well-built instrument with good materials"},
                    {"title": "Versatile Sound", "description": "Suitable for multiple music styles"}
                ],
                "why_not_buy": [
                    {"title": "Limited Features", "description": "May lack advanced features for professionals"}
                ],
                "best_for": [
                    {"user_type": "Intermediate Players", "reason": "Good balance of quality and affordability"},
                    {"user_type": "Home Recording", "reason": "Reliable performance for studio work"}
                ],
                "not_ideal_for": [
                    {"user_type": "Beginners", "reason": "May be too complex for first-time players"}
                ]
            }

    async def _generate_usage_guidance(self, context: str) -> Dict[str, Any]:
        """Generate usage guidance and recommendations."""
        prompt = f"""
Provide usage guidance for this musical instrument.

{context}

Generate JSON with:
- recommended_amplifiers: array of amp types
- suitable_music_styles: object with excellent, good, and limited arrays
- skill_development: learning_curve (Easy/Moderate/Steep), growth_potential description

Respond in valid JSON format only.
"""
        
        response = await self._make_ai_request(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "recommended_amplifiers": ["Tube amps", "Solid state amps"],
                "suitable_music_styles": {
                    "excellent": ["Rock", "Blues"],
                    "good": ["Pop", "Country"],
                    "limited": ["Classical", "Jazz"]
                },
                "skill_development": {
                    "learning_curve": "Moderate",
                    "growth_potential": "Will serve players for several years as they develop"
                }
            }

    async def _generate_maintenance_care(self, context: str) -> Dict[str, Any]:
        """Generate maintenance and care instructions."""
        prompt = f"""
Provide maintenance and care guidance for this musical instrument.

{context}

Generate JSON with:
- maintenance_level: Low/Medium/High
- common_issues: array of potential issues
- care_instructions: object with daily, weekly, monthly, annual tasks
- upgrade_potential: easy_upgrades array, recommended_budget

Respond in valid JSON format only.
"""
        
        response = await self._make_ai_request(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "maintenance_level": "Medium",
                "common_issues": ["String wear", "Tuning stability"],
                "care_instructions": {
                    "daily": "Wipe down after playing",
                    "weekly": "Check tuning and clean strings",
                    "monthly": "Deep clean and inspect hardware",
                    "annual": "Professional setup and maintenance"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Pickups", "Tuners"],
                    "recommended_budget": "€200-500 for meaningful improvements"
                }
            }

    async def _generate_professional_assessment(self, context: str) -> Dict[str, Any]:
        """Generate professional assessment and ratings."""
        prompt = f"""
Provide a professional assessment of this musical instrument.

{context}

Generate JSON with:
- expert_rating: object with build_quality, sound_quality, value_for_money, versatility (all 1-10)
- standout_features: array of notable features
- notable_limitations: array of limitations
- competitive_position: description of market position

Respond in valid JSON format only.
"""
        
        response = await self._make_ai_request(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "expert_rating": {
                    "build_quality": 7,
                    "sound_quality": 7,
                    "value_for_money": 8,
                    "versatility": 7
                },
                "standout_features": ["Quality construction", "Good value"],
                "notable_limitations": ["Limited color options", "Basic electronics"],
                "competitive_position": "Good value in its price range, suitable for intermediate players"
            }

    def _create_content_metadata(self) -> Dict[str, Any]:
        """Create metadata for the generated content."""
        return {
            "generated_date": datetime.utcnow().isoformat(),
            "content_version": "1.0",
            "seo_keywords": ["musical instrument", "guitar", "keyboard", "best price"],
            "readability_score": "Medium",
            "word_count": "Approximately 800 words"
        }

    async def _make_ai_request(self, prompt: str) -> str:
        """Make a request to the AI model."""
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
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
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        return (response.choices[0].message.content or "").strip()


