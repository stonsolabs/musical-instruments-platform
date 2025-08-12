from __future__ import annotations

import json
from typing import Any, Dict, List

import openai

from ..config import settings
from ..models import Product


class AIContentGenerator:
    def __init__(self) -> None:
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_product_content(self, product: Product) -> Dict[str, Any]:
        context = self._build_product_context(product)
        summary = await self._generate_summary(context)
        pros_cons = await self._generate_pros_cons(context)
        use_cases = await self._generate_use_cases(context)
        seo_content = await self._generate_seo_content(context)

        return {
            "summary": summary,
            "pros": pros_cons.get("pros", []),
            "cons": pros_cons.get("cons", []),
            "best_for": use_cases.get("best_for", []),
            "genres": use_cases.get("genres", []),
            "skill_level": use_cases.get("skill_level", ""),
            "seo_description": seo_content.get("description", ""),
            "seo_keywords": seo_content.get("keywords", []),
        }

    def _build_product_context(self, product: Product) -> str:
        specs_str = ""
        if product.specifications:
            specs_str = "\n".join([f"- {k}: {v}" for k, v in product.specifications.items()])

        context = f"""
Product: {product.name}
Brand: {product.brand.name}
Category: {product.category.name}
Description: {product.description or 'No description available'}

Specifications:
{specs_str}

MSRP Price: €{product.msrp_price or 'N/A'}
"""
        return context

    async def _generate_summary(self, context: str) -> str:
        prompt = f"""
As a musical instrument expert, write a concise 2-3 sentence summary for this product that highlights its key features and appeal.
Focus on what makes this instrument unique and who would benefit from it.

{context}

Summary:"""
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in musical instruments with deep knowledge of guitars, keyboards, drums, and audio equipment.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return (response.choices[0].message.content or "").strip()

    async def _generate_pros_cons(self, context: str) -> Dict[str, List[str]]:
        prompt = f"""
As a musical instrument expert, analyze this product and provide 3-4 pros and 2-3 cons.
Be honest and balanced in your assessment.

{context}

Respond in JSON format:
{{"pros": ["pro1", "pro2", "pro3"], "cons": ["con1", "con2"]}}
"""
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert musical instrument reviewer. Provide honest, balanced assessments.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        try:
            return json.loads((response.choices[0].message.content or "").strip())
        except json.JSONDecodeError:
            return {"pros": ["Quality construction", "Good value for money"], "cons": ["Limited color options"]}

    async def _generate_use_cases(self, context: str) -> Dict[str, Any]:
        prompt = f"""
Analyze this musical instrument and determine:
1. Who it's best for (3-4 specific use cases)
2. What music genres it suits (3-5 genres)
3. Skill level (Beginner/Intermediate/Advanced/Professional)

{context}

Respond in JSON format:
{{
    "best_for": ["use case 1", "use case 2", "use case 3"],
    "genres": ["genre1", "genre2", "genre3"],
    "skill_level": "Intermediate"
}}
"""
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert musical instrument consultant helping musicians choose the right instruments.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.7,
        )
        try:
            return json.loads((response.choices[0].message.content or "").strip())
        except json.JSONDecodeError:
            return {
                "best_for": ["General playing", "Recording", "Live performance"],
                "genres": ["Rock", "Pop", "Blues"],
                "skill_level": "Intermediate",
            }

    async def _generate_seo_content(self, context: str) -> Dict[str, Any]:
        prompt = f"""
Create SEO content for this musical instrument:
1. Meta description (150-160 characters, compelling)
2. 5-7 relevant keywords for search optimization

{context}

Respond in JSON format:
{{
    "description": "meta description here",
    "keywords": ["keyword1", "keyword2", "keyword3"]
}}
"""
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an SEO expert specializing in musical instrument e-commerce.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.7,
        )
        try:
            return json.loads((response.choices[0].message.content or "").strip())
        except json.JSONDecodeError:
            return {
                "description": "High-quality musical instrument with excellent features and competitive pricing.",
                "keywords": ["musical instrument", "guitar", "keyboard", "best price"],
            }


