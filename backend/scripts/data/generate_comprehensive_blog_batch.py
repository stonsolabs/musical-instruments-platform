#!/usr/bin/env python3
"""
Comprehensive blog batch generator using ALL available templates.
Creates 75+ blog post ideas utilizing every template type.
"""

import asyncio
import sys
import os
import json
import random
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

# Comprehensive blog ideas using ALL 24 templates
COMPREHENSIVE_BLOG_IDEAS = [
    # === GENERAL TEMPLATES ===
    
    # Affiliate Roundup: Best Picks (5 posts)
    {"title": "Best Electric Guitars for Beginners Under $500", "template": "Affiliate Roundup: Best Picks", "category": "Electric Guitars", "product_ids": [262, 267, 264, 305], "tags": ["electric_guitar", "beginner", "budget", "roundup"]},
    {"title": "Top 7 Bass Guitars for Rock Music", "template": "Affiliate Roundup: Best Picks", "category": "Bass Guitars", "product_ids": [309, 381, 666, 693], "tags": ["bass_guitar", "rock", "genre_specific"]},
    {"title": "Best Digital Pianos with Weighted Keys", "template": "Affiliate Roundup: Best Picks", "category": "Digital Pianos", "product_ids": [370, 581, 596, 630, 704], "tags": ["digital_piano", "weighted_keys", "premium"]},
    {"title": "Top MIDI Controllers for Music Production", "template": "Affiliate Roundup: Best Picks", "category": "MIDI Controllers", "product_ids": [476, 488, 515, 520, 522], "tags": ["midi_controller", "production", "studio"]},
    {"title": "Best Travel Acoustic Guitars for Musicians", "template": "Affiliate Roundup: Best Picks", "category": "Acoustic Guitars", "product_ids": [38, 46, 61, 75, 103], "tags": ["travel_guitar", "acoustic", "portable"]},
    
    # Budget Heroes: Best Bang for Buck (4 posts)
    {"title": "Best Budget Electric Guitars Under $300", "template": "Budget Heroes: Best Bang for Buck", "category": "Electric Guitars", "product_ids": [262, 267, 364], "tags": ["electric_guitar", "budget", "under_300", "value"]},
    {"title": "Affordable Synthesizers That Sound Expensive", "template": "Budget Heroes: Best Bang for Buck", "category": "Synthesizers", "product_ids": [463, 477, 507, 519, 762], "tags": ["synthesizer", "budget", "value", "affordable"]},
    {"title": "Budget Digital Pianos Under $600", "template": "Budget Heroes: Best Bang for Buck", "category": "Digital Pianos", "product_ids": [589, 697, 722], "tags": ["digital_piano", "budget", "under_600"]},
    {"title": "Best Value Bass Guitars for Beginners", "template": "Budget Heroes: Best Bang for Buck", "category": "Bass Guitars", "product_ids": [482, 484, 551], "tags": ["bass_guitar", "beginner", "value", "budget"]},
    
    # Deals & Value Picks (3 posts)
    {"title": "Hidden Gems: Underrated Guitar Brands", "template": "Deals & Value Picks", "category": "Electric Guitars", "product_ids": [262, 267, 292], "tags": ["hidden_gems", "value", "underrated", "brands"]},
    {"title": "Best Value Acoustic Guitars Under $400", "template": "Deals & Value Picks", "category": "Acoustic Guitars", "product_ids": [155, 190, 199, 208], "tags": ["acoustic", "value", "under_400", "deals"]},
    {"title": "Pro Sound on a Budget: Synthesizer Deals", "template": "Deals & Value Picks", "category": "Synthesizers", "product_ids": [507, 514, 519, 523], "tags": ["synthesizer", "deals", "budget", "pro_sound"]},
    
    # Price Watch & Value Picks (3 posts)
    {"title": "Guitar Price Trends: When to Buy in 2025", "template": "Price Watch & Value Picks", "category": "Electric Guitars", "product_ids": [376, 620, 297, 364], "tags": ["price_trends", "market_analysis", "timing", "2025"]},
    {"title": "Digital Piano Market Analysis: Best Times to Buy", "template": "Price Watch & Value Picks", "category": "Digital Pianos", "product_ids": [589, 697, 359, 370], "tags": ["market_analysis", "timing", "digital_piano", "deals"]},
    {"title": "Bass Guitar Value Analysis: Premium vs Budget", "template": "Price Watch & Value Picks", "category": "Bass Guitars", "product_ids": [309, 314, 482, 484], "tags": ["value_analysis", "premium_vs_budget", "bass_guitar"]},
    
    # Seasonal Deal Hunter (4 posts)
    {"title": "Black Friday Guitar Deals 2025: What to Watch", "template": "Seasonal Deal Hunter", "category": "Electric Guitars", "product_ids": [376, 297, 262, 267], "tags": ["black_friday", "deals", "2025", "seasonal"]},
    {"title": "Holiday Gift Guide: Best Musical Instruments", "template": "Seasonal Deal Hunter", "category": "Electric Guitars", "product_ids": [155, 262, 527, 589, 697], "tags": ["holiday", "gifts", "christmas", "family"]},
    {"title": "Back to School: Student Instrument Deals", "template": "Seasonal Deal Hunter", "category": "Electric Guitars", "product_ids": [155, 190, 262, 482, 589], "tags": ["back_to_school", "student", "education", "deals"]},
    {"title": "Summer Festival Gear: Portable Music Setup", "template": "Seasonal Deal Hunter", "category": "Electric Guitars", "product_ids": [38, 61, 103, 153, 170], "tags": ["summer", "festival", "portable", "travel"]},
    
    # === BUYING GUIDE TEMPLATES ===
    
    # Ultimate 2025 Buying Guide (6 posts)
    {"title": "Ultimate Electric Guitar Buying Guide 2025", "template": "Ultimate 2025 Buying Guide", "category": "Electric Guitars", "product_ids": [262, 267, 297, 376, 364], "tags": ["electric_guitar", "buying_guide", "2025", "comprehensive"]},
    {"title": "Complete Bass Guitar Buying Guide 2025", "template": "Ultimate 2025 Buying Guide", "category": "Bass Guitars", "product_ids": [309, 314, 482, 484, 551], "tags": ["bass_guitar", "buying_guide", "2025", "complete"]},
    {"title": "Digital Piano Buyer's Guide: Everything You Need", "template": "Ultimate 2025 Buying Guide", "category": "Digital Pianos", "product_ids": [589, 697, 359, 370, 581], "tags": ["digital_piano", "buyers_guide", "comprehensive"]},
    {"title": "Synthesizer Buying Guide: Analog vs Digital", "template": "Ultimate 2025 Buying Guide", "category": "Synthesizers", "product_ids": [506, 507, 521, 964, 477], "tags": ["synthesizer", "analog_vs_digital", "buying_guide"]},
    {"title": "Acoustic Guitar Buying Guide: Wood Types & Sound", "template": "Ultimate 2025 Buying Guide", "category": "Acoustic Guitars", "product_ids": [186, 197, 220, 222, 230], "tags": ["acoustic_guitar", "wood_types", "sound", "guide"]},
    {"title": "MIDI Controller Buying Guide for Producers", "template": "Ultimate 2025 Buying Guide", "category": "MIDI Controllers", "product_ids": [476, 488, 515, 520, 522], "tags": ["midi_controller", "production", "buying_guide"]},
    
    # Buying Guide Template (3 posts)
    {"title": "How to Choose Your First Electric Guitar", "template": "Buying Guide Template", "category": "Electric Guitars", "product_ids": [262, 267, 364, 305], "tags": ["first_guitar", "beginner", "how_to_choose"]},
    {"title": "Choosing the Right Digital Piano: Size vs Features", "template": "Buying Guide Template", "category": "Digital Pianos", "product_ids": [589, 697, 722, 746], "tags": ["digital_piano", "size_vs_features", "choosing"]},
    {"title": "Bass Guitar Buying Guide: 4-String vs 5-String", "template": "Buying Guide Template", "category": "Bass Guitars", "product_ids": [309, 314, 335, 482], "tags": ["bass_guitar", "4_string_vs_5_string", "guide"]},
    
    # Buying Guide: What to Look For (3 posts)
    {"title": "What to Look for in a Beginner Acoustic Guitar", "template": "Buying Guide: What to Look For", "category": "Acoustic Guitars", "product_ids": [155, 190, 199, 208], "tags": ["acoustic_guitar", "beginner", "what_to_look_for"]},
    {"title": "Synthesizer Features: What Matters Most", "template": "Buying Guide: What to Look For", "category": "Synthesizers", "product_ids": [507, 508, 514, 519], "tags": ["synthesizer", "features", "what_matters"]},
    {"title": "Digital Piano Key Action: What to Consider", "template": "Buying Guide: What to Look For", "category": "Digital Pianos", "product_ids": [589, 697, 722, 370], "tags": ["digital_piano", "key_action", "considerations"]},
    
    # === COMPARISON TEMPLATES ===
    
    # Head-to-Head Battle: Product Showdown (8 posts)
    {"title": "Gibson Les Paul vs. Epiphone Les Paul: Worth the Premium?", "template": "Head-to-Head Battle: Product Showdown", "category": "Electric Guitars", "product_ids": [297, 279], "tags": ["gibson", "epiphone", "les_paul", "premium_vs_budget"]},
    {"title": "Fender Precision vs. Jazz Bass: The Ultimate Battle", "template": "Head-to-Head Battle: Product Showdown", "category": "Bass Guitars", "product_ids": [309, 374, 381, 502], "tags": ["fender", "precision", "jazz_bass", "battle"]},
    {"title": "Yamaha Clavinova vs. Kawai CA Series", "template": "Head-to-Head Battle: Product Showdown", "category": "Digital Pianos", "product_ids": [359, 370, 581, 596], "tags": ["yamaha", "kawai", "clavinova", "premium"]},
    {"title": "Arturia PolyBrute vs. Moog Subsequent 37", "template": "Head-to-Head Battle: Product Showdown", "category": "Synthesizers", "product_ids": [506, 521, 964], "tags": ["arturia", "moog", "analog", "polybrute"]},
    {"title": "Taylor vs. Martin: Acoustic Guitar Showdown", "template": "Head-to-Head Battle: Product Showdown", "category": "Acoustic Guitars", "product_ids": [186, 197, 232], "tags": ["taylor", "martin", "acoustic", "premium"]},
    {"title": "ESP LTD vs. Schecter: Metal Guitar Battle", "template": "Head-to-Head Battle: Product Showdown", "category": "Electric Guitars", "product_ids": [274, 276, 363, 366], "tags": ["esp", "schecter", "metal", "battle"]},
    {"title": "Casio Privia vs. Yamaha Arius: Budget Piano Battle", "template": "Head-to-Head Battle: Product Showdown", "category": "Digital Pianos", "product_ids": [361, 365, 607, 589], "tags": ["casio", "yamaha", "budget", "battle"]},
    {"title": "Arturia KeyLab vs. Native Instruments Kontrol", "template": "Head-to-Head Battle: Product Showdown", "category": "MIDI Controllers", "product_ids": [488, 489, 520, 526], "tags": ["arturia", "native_instruments", "midi", "battle"]},
    
    # Comparison Guide Template (4 posts)
    {"title": "Electric vs. Acoustic Guitar: Which for Beginners?", "template": "Comparison Guide Template", "category": "Electric Guitars", "product_ids": [155, 190, 262, 267], "tags": ["electric_vs_acoustic", "beginner", "comparison"]},
    {"title": "Piano vs. Keyboard: Complete Comparison Guide", "template": "Comparison Guide Template", "category": "Digital Pianos", "product_ids": [589, 697, 722, 476], "tags": ["piano_vs_keyboard", "comparison", "guide"]},
    {"title": "Analog vs. Digital Synthesizers: Which to Choose?", "template": "Comparison Guide Template", "category": "Synthesizers", "product_ids": [477, 521, 964, 507], "tags": ["analog_vs_digital", "synthesizer", "comparison"]},
    {"title": "Solid Wood vs. Laminate Acoustic Guitars", "template": "Comparison Guide Template", "category": "Acoustic Guitars", "product_ids": [186, 220, 222, 230], "tags": ["solid_wood", "laminate", "acoustic", "construction"]},
    
    # Comparison Mega-Roundup (3 posts)
    {"title": "Guitar Brands Compared: Fender vs. Gibson vs. PRS", "template": "Comparison Mega-Roundup", "category": "Electric Guitars", "product_ids": [376, 297, 269, 280], "tags": ["fender", "gibson", "prs", "brand_comparison"]},
    {"title": "Digital Piano Brands: Yamaha vs. Kawai vs. Roland", "template": "Comparison Mega-Roundup", "category": "Digital Pianos", "product_ids": [589, 359, 570, 578], "tags": ["yamaha", "kawai", "roland", "brand_comparison"]},
    {"title": "Bass Guitar Styles: Precision vs. Jazz vs. Music Man", "template": "Comparison Mega-Roundup", "category": "Bass Guitars", "product_ids": [309, 374, 314, 505], "tags": ["precision", "jazz", "music_man", "styles"]},
    
    # Side-by-Side Comparison (3 posts)
    {"title": "Stratocaster vs. Telecaster: Fender's Icons", "template": "Side-by-Side Comparison", "category": "Electric Guitars", "product_ids": [376, 620, 646], "tags": ["stratocaster", "telecaster", "fender", "icons"]},
    {"title": "Korg vs. Roland: Digital Piano Comparison", "template": "Side-by-Side Comparison", "category": "Digital Pianos", "product_ids": [570, 578, 612], "tags": ["korg", "roland", "digital_piano", "comparison"]},
    {"title": "Active vs. Passive Bass Pickups: Sound Comparison", "template": "Side-by-Side Comparison", "category": "Bass Guitars", "product_ids": [314, 335, 309, 381], "tags": ["active", "passive", "pickups", "sound"]},
    
    # === REVIEW TEMPLATES ===
    
    # Professional Deep Dive Review (6 posts)
    {"title": "Fender Player Stratocaster: Complete Review", "template": "Professional Deep Dive Review", "category": "Electric Guitars", "product_ids": [376], "tags": ["fender", "stratocaster", "review", "deep_dive"]},
    {"title": "Yamaha Clavinova CLP-775: In-Depth Review", "template": "Professional Deep Dive Review", "category": "Digital Pianos", "product_ids": [359], "tags": ["yamaha", "clavinova", "review", "premium"]},
    {"title": "Music Man StingRay Bass: Professional Review", "template": "Professional Deep Dive Review", "category": "Bass Guitars", "product_ids": [314], "tags": ["music_man", "stingray", "review", "professional"]},
    {"title": "Moog Subsequent 37: Analog Synth Review", "template": "Professional Deep Dive Review", "category": "Synthesizers", "product_ids": [521], "tags": ["moog", "subsequent", "analog", "review"]},
    {"title": "Martin D-28: Acoustic Guitar Legend Review", "template": "Professional Deep Dive Review", "category": "Acoustic Guitars", "product_ids": [186], "tags": ["martin", "d28", "legend", "review"]},
    {"title": "Native Instruments Komplete Kontrol Review", "template": "Professional Deep Dive Review", "category": "MIDI Controllers", "product_ids": [520], "tags": ["native_instruments", "kontrol", "review", "production"]},
    
    # Product Review Template (4 posts)
    {"title": "PRS SE Custom 24: Value Guitar Review", "template": "Product Review Template", "category": "Electric Guitars", "product_ids": [269], "tags": ["prs", "se", "custom", "value_review"]},
    {"title": "Kawai CA49: Digital Piano Review", "template": "Product Review Template", "category": "Digital Pianos", "product_ids": [581], "tags": ["kawai", "ca49", "digital_piano", "review"]},
    {"title": "Korg Volca Bass: Analog Bass Synth Review", "template": "Product Review Template", "category": "Synthesizers", "product_ids": [514], "tags": ["korg", "volca", "bass", "analog"]},
    {"title": "Harley Benton ST-62: Budget Strat Review", "template": "Product Review Template", "category": "Electric Guitars", "product_ids": [262], "tags": ["harley_benton", "budget", "stratocaster", "review"]},
    
    # Hands-on Review Template (3 posts)  
    {"title": "Epiphone Les Paul Standard: Hands-On Test", "template": "Hands-on Review Template", "category": "Electric Guitars", "product_ids": [279], "tags": ["epiphone", "les_paul", "hands_on", "test"]},
    {"title": "Yamaha P-145: Portable Piano Hands-On", "template": "Hands-on Review Template", "category": "Digital Pianos", "product_ids": [697], "tags": ["yamaha", "p145", "portable", "hands_on"]},
    {"title": "Behringer DeepMind 12: Hands-On Review", "template": "Hands-on Review Template", "category": "Synthesizers", "product_ids": [477], "tags": ["behringer", "deepmind", "hands_on", "analog"]},
    
    # === TUTORIAL TEMPLATES ===
    
    # Tutorial Guide Template (4 posts)
    {"title": "Guitar Setup Guide: Action, Intonation & Truss Rod", "template": "Tutorial Guide Template", "category": "Electric Guitars", "product_ids": [376, 297, 262], "tags": ["guitar_setup", "action", "intonation", "tutorial"]},
    {"title": "Piano Practice Techniques: Maximize Your Progress", "template": "Tutorial Guide Template", "category": "Digital Pianos", "product_ids": [589, 697, 359], "tags": ["piano_practice", "techniques", "progress", "tutorial"]},
    {"title": "Bass Playing Fundamentals: Rhythm and Timing", "template": "Tutorial Guide Template", "category": "Bass Guitars", "product_ids": [309, 482, 484], "tags": ["bass_fundamentals", "rhythm", "timing", "tutorial"]},
    {"title": "Synthesizer Programming: Creating Your First Patch", "template": "Tutorial Guide Template", "category": "Synthesizers", "product_ids": [507, 521, 514], "tags": ["synthesizer_programming", "patch", "tutorial", "beginner"]},
    
    # Tutorial/How-To with Product Context (3 posts)
    {"title": "How to Record Guitar at Home: Gear Setup Guide", "template": "Tutorial/How-To with Product Context", "category": "Electric Guitars", "product_ids": [376, 297, 262], "tags": ["recording", "home_studio", "guitar", "tutorial"]},
    {"title": "Digital Piano Maintenance: Keep Your Keys Perfect", "template": "Tutorial/How-To with Product Context", "category": "Digital Pianos", "product_ids": [589, 697, 359], "tags": ["maintenance", "digital_piano", "care", "tutorial"]},
    {"title": "MIDI Setup Guide: Connecting Your Controller", "template": "Tutorial/How-To with Product Context", "category": "MIDI Controllers", "product_ids": [476, 515, 520], "tags": ["midi_setup", "controller", "connection", "tutorial"]},
    
    # Setup & Troubleshooting Guide (3 posts)
    {"title": "Guitar Amp Setup: Getting the Perfect Tone", "template": "Setup & Troubleshooting Guide", "category": "Electric Guitars", "product_ids": [376, 297, 262], "tags": ["amp_setup", "tone", "troubleshooting", "guitar"]},
    {"title": "Digital Piano Connection Issues: Quick Fixes", "template": "Setup & Troubleshooting Guide", "category": "Digital Pianos", "product_ids": [589, 697, 359], "tags": ["connection_issues", "troubleshooting", "digital_piano"]},
    {"title": "Bass Setup Problems: Common Issues & Solutions", "template": "Setup & Troubleshooting Guide", "category": "Bass Guitars", "product_ids": [309, 314, 482], "tags": ["bass_setup", "problems", "solutions", "troubleshooting"]},
    
    # Maintenance & Care Checklist (3 posts)
    {"title": "Guitar Maintenance Checklist: Annual Care Guide", "template": "Maintenance & Care Checklist", "category": "Electric Guitars", "product_ids": [376, 297, 262], "tags": ["maintenance", "care", "checklist", "annual"]},
    {"title": "Digital Piano Care: Keeping Your Investment Safe", "template": "Maintenance & Care Checklist", "category": "Digital Pianos", "product_ids": [589, 697, 359], "tags": ["digital_piano_care", "investment", "maintenance"]},
    {"title": "Synthesizer Maintenance: Analog & Digital Care", "template": "Maintenance & Care Checklist", "category": "Synthesizers", "product_ids": [521, 507, 477], "tags": ["synthesizer_maintenance", "analog", "digital", "care"]},
    
    # === SPECIALTY TEMPLATES ===
    
    # Artist Spotlight: Gear, Tone, and Affordable Alternatives (3 posts)
    {"title": "Marcus Miller's Bass Rig: Gear & Affordable Alternatives", "template": "Artist Spotlight: Gear, Tone, and Affordable Alternatives", "category": "Bass Guitars", "product_ids": [306, 335, 343, 348], "tags": ["marcus_miller", "bass_rig", "artist", "alternatives"]},
    {"title": "John Mayer's PRS Silver Sky: Tone & Budget Options", "template": "Artist Spotlight: Gear, Tone, and Affordable Alternatives", "category": "Electric Guitars", "product_ids": [269], "tags": ["john_mayer", "prs", "silver_sky", "tone"]},
    {"title": "Herbie Hancock's Keyboard Setup: Jazz Legend's Gear", "template": "Artist Spotlight: Gear, Tone, and Affordable Alternatives", "category": "Digital Pianos", "product_ids": [570, 578, 584], "tags": ["herbie_hancock", "keyboard", "jazz", "legend"]},
    
    # Historical Article Template (2 posts)
    {"title": "The Evolution of the Electric Guitar: 1931-2025", "template": "Historical Article Template", "category": "Electric Guitars", "product_ids": [376, 297, 262], "tags": ["evolution", "electric_guitar", "history", "1931_2025"]},
    {"title": "Synthesizer History: From Moog to Modern Digital", "template": "Historical Article Template", "category": "Synthesizers", "product_ids": [521, 507, 477], "tags": ["synthesizer_history", "moog", "digital", "evolution"]},
    
    # History & Evolution (Educational) (2 posts)
    {"title": "Bass Guitar Evolution: From Upright to Electric", "template": "History & Evolution (Educational)", "category": "Bass Guitars", "product_ids": [309, 314, 482], "tags": ["bass_evolution", "upright", "electric", "history"]},
    {"title": "Piano to Digital: The Evolution of Keyboard Instruments", "template": "History & Evolution (Educational)", "category": "Digital Pianos", "product_ids": [589, 697, 359], "tags": ["piano_evolution", "digital", "keyboard", "history"]},
    
    # Interactive Quiz: Find Your Perfect Gear (2 posts)
    {"title": "Quiz: What's Your Perfect Electric Guitar Style?", "template": "Interactive Quiz: Find Your Perfect Gear", "category": "Electric Guitars", "product_ids": [376, 297, 262, 269], "tags": ["quiz", "electric_guitar", "style", "interactive"]},
    {"title": "Find Your Ideal Digital Piano: Interactive Quiz", "template": "Interactive Quiz: Find Your Perfect Gear", "category": "Digital Pianos", "product_ids": [589, 697, 359, 581], "tags": ["quiz", "digital_piano", "ideal", "interactive"]},
    
    # New Release: First Look & Key Differences (2 posts)
    {"title": "Fender Player II Series: What's New for 2025?", "template": "New Release: First Look & Key Differences", "category": "Electric Guitars", "product_ids": [376, 620], "tags": ["fender", "player_ii", "new_release", "2025"]},
    {"title": "Yamaha P-225: New Digital Piano First Look", "template": "New Release: First Look & Key Differences", "category": "Digital Pianos", "product_ids": [697], "tags": ["yamaha", "p225", "new_release", "first_look"]}
]

async def get_structured_prompt(blog_idea):
    """Get the structured JSON prompt for a blog idea using actual template from database"""
    async with async_session_factory() as session:
        # Get the actual template content
        result = await session.execute(
            text("SELECT base_prompt FROM blog_generation_templates WHERE name = :name AND is_active = true"),
            {"name": blog_idea['template']}
        )
        template_row = result.fetchone()
        
        if not template_row:
            # Fallback generic prompt
            base_prompt = f"Write a comprehensive blog post about {blog_idea['title']}."
        else:
            base_prompt = template_row[0]
    
    return f"""{base_prompt}

Title: {blog_idea['title']}
Template: {blog_idea['template']}
Category: {blog_idea['category']}
Product IDs to feature: {blog_idea['product_ids']}
Tags: {', '.join(blog_idea['tags'])}

Create engaging, informative content that helps readers make informed purchasing decisions. Do not mention AI generation."""

async def create_comprehensive_batch():
    """Create comprehensive batch file using all templates"""
    
    print("🚀 Creating comprehensive blog batch with ALL templates...")
    print(f"📊 Total blog ideas: {len(COMPREHENSIVE_BLOG_IDEAS)}")
    
    # Count template usage
    template_usage = {}
    for idea in COMPREHENSIVE_BLOG_IDEAS:
        template = idea['template']
        template_usage[template] = template_usage.get(template, 0) + 1
    
    print(f"📋 Using {len(template_usage)} different templates:")
    for template, count in sorted(template_usage.items()):
        print(f"   - {template}: {count} posts")
    
    batch_requests = []
    
    for i, idea in enumerate(COMPREHENSIVE_BLOG_IDEAS):
        prompt = await get_structured_prompt(idea)
        
        batch_request = {
            "custom_id": f"blog-post-{i+1:03d}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4-1106-preview",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert music gear writer creating comprehensive blog posts. Always respond with valid JSON only, no explanations or comments."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 4000,
                "temperature": 0.7
            }
        }
        batch_requests.append(batch_request)
    
    # Save batch file
    batch_filename = f"/Users/felipe/pprojects/musical-instruments-platform/comprehensive_blog_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    with open(batch_filename, 'w') as f:
        for request in batch_requests:
            f.write(json.dumps(request) + '\n')
    
    print(f"📄 Created comprehensive batch file: {batch_filename}")
    print(f"📊 Total requests: {len(batch_requests)}")
    
    # Create detailed summary
    summary = {
        "created_at": datetime.now().isoformat(),
        "total_requests": len(batch_requests),
        "template_usage": template_usage,
        "categories": {},
        "blog_ideas": COMPREHENSIVE_BLOG_IDEAS
    }
    
    # Count categories
    for idea in COMPREHENSIVE_BLOG_IDEAS:
        cat = idea['category']
        summary['categories'][cat] = summary['categories'].get(cat, 0) + 1
    
    summary_file = batch_filename.replace('.jsonl', '_summary.json')
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"📋 Created summary: {summary_file}")
    print(f"📂 Categories covered: {list(summary['categories'].keys())}")
    print(f"🎯 Template coverage: {len(template_usage)}/24 templates")
    
    return batch_filename, len(batch_requests)

async def main():
    print("🎵 Comprehensive Blog Batch Generator")
    print("Using ALL Available Templates")
    print("=" * 50)
    
    try:
        batch_file, count = await create_comprehensive_batch()
        
        print(f"\n🎉 Comprehensive batch generation completed!")
        print(f"📁 Batch file: {batch_file}")
        print(f"🔢 Total requests: {count}")
        print(f"📋 Templates used: ALL 24 available templates")
        
        print(f"\n📝 What this batch includes:")
        print(f"   • Complete template coverage (all 24 templates)")
        print(f"   • Diverse content types (reviews, guides, comparisons)")
        print(f"   • Multiple instrument categories")
        print(f"   • Real product IDs from your catalog")
        print(f"   • Professional, human-like content")
        print(f"   • Structured JSON format for easy processing")
        
    except Exception as e:
        print(f"💥 Error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())