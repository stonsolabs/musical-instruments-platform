#!/usr/bin/env python3
"""
Insert two brand-new electric guitars that don't exist yet, following the comprehensive schema.
"""

import asyncio
import os
import sys
from decimal import Decimal

# Ensure app imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.models import Product, Brand, Category

DATABASE_URL = "postgresql+asyncpg://admin:qQqqDgXlIuBSZDUlgqzQEcoTPBkrCjVD@dpg-d2er32qdbo4c738oofng-a.frankfurt-postgres.render.com/musicgear_db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

NEW_PRODUCTS = [
    {
        "product_input": {
            "sku": "PRS-SE-CUSTOM-24",
            "name": "PRS SE Custom 24",
            "slug": "prs-se-custom-24",
            "brand": "PRS",
            "category": "electric-guitars",
            "description": "The PRS SE Custom 24 brings the flagship PRS design to an accessible range, delivering versatile tones, premium playability, and refined aesthetics.",
            "specifications": {
                "body_material": "Mahogany with Maple Top and Flame Maple Veneer",
                "neck_material": "Maple",
                "fingerboard": "Rosewood",
                "pickups": "85/15 ‘S’ Humbuckers",
                "scale_length": "25 inches",
                "frets": 24,
                "bridge": "PRS Patented Tremolo",
                "tuners": "PRS Designed",
                "nut_width": "1.6875 inches",
                "finish": "Gloss Polyurethane"
            },
            "msrp_price": 899,
            "images": ["prs_se_custom24_1.jpg", "prs_se_custom24_2.jpg", "prs_se_custom24_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "SE Custom 24 captures the essence of PRS: versatile 85/15 ‘S’ pickups, silky 24-fret playability, and rock-solid tremolo stability.",
                "key_features": ["85/15 ‘S’ humbuckers", "24 frets, 25\" scale", "PRS tremolo", "Wide Thin neck profile"],
                "target_skill_level": "Intermediate to Advanced",
                "country_of_origin": "Indonesia",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Balanced, modern clarity with tight lows, present mids, and articulate highs",
                    "output_level": "Medium-High",
                    "best_genres": ["Rock", "Pop", "Fusion", "Progressive", "Worship"],
                    "pickup_positions": {
                        "bridge": "Tight, punchy rhythm and cutting leads",
                        "both_split": "Single-coil-like sparkle for cleans and funk",
                        "neck": "Smooth, vocal leads and warm cleans"
                    }
                },
                "build_quality": {
                    "construction_type": "Solid Body",
                    "hardware_quality": "Premium for price tier",
                    "finish_quality": "Consistent, attractive flame veneer with clean binding",
                    "expected_durability": "High"
                },
                "playability": {
                    "neck_profile": "Wide Thin offers fast access with comfortable shoulders",
                    "action_setup": "Low action achievable with stable tremolo",
                    "comfort_rating": "9/10 - Balanced weight and excellent upper fret access",
                    "weight_category": "Medium"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Versatile Modern Tones", "description": "Coil-splits and 85/15 ‘S’ pickups span glassy cleans to saturated leads."},
                    {"title": "PRS Fit and Finish", "description": "Consistent build quality and hardware stability inspire confidence on stage."}
                ],
                "why_not_buy": [
                    {"title": "Non-Traditional Voicing", "description": "Those seeking vintage-only tones may prefer classic SSS/HH alternatives."}
                ],
                "best_for": [
                    {"user_type": "Working guitarists needing one do-it-all instrument", "reason": "Covers wide genre ground with reliable hardware."}
                ],
                "not_ideal_for": [
                    {"user_type": "Vintage purists", "reason": "Modern PRS voice and ergonomics over vintage-correct specs."}
                ]
            },
            "usage_guidance": {
                "recommended_amplifiers": ["Clean platforms with pedals", "Modern high-headroom combos", "Boutique low-watt amps"],
                "suitable_music_styles": {
                    "excellent": ["Pop", "Rock", "Fusion", "Worship"],
                    "good": ["Indie", "Alternative"],
                    "limited": ["Traditional vintage blues-only contexts"]
                },
                "skill_development": {
                    "learning_curve": "Low",
                    "growth_potential": "Remains relevant from intermediate to pro due to flexibility"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Tremolo setup for alternate tunings"],
                "care_instructions": {
                    "daily": "Wipe strings/body; ensure tremolo returns to pitch",
                    "weekly": "Check nut/trem lubrication",
                    "monthly": "Intonation and relief check",
                    "annual": "Pro setup and tremolo knife-edge inspection"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Locking tuners", "Electronics harness"],
                    "recommended_budget": "€80-200"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "9", "sound_quality": "8", "value_for_money": "9", "versatility": "9"},
                "standout_features": ["Wide Thin neck", "Coil-split versatility", "Stable tremolo"],
                "notable_limitations": ["Modern-leaning voice"],
                "competitive_position": "Top contender around €800-1000 against HH superstrats and modern single-cuts"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["PRS SE Custom 24", "PRS guitar", "coil split", "24-fret guitar"],
                "readability_score": "Medium",
                "word_count": "600"
            }
        }
    },
    {
        "product_input": {
            "sku": "ESP-LTD-EC-256",
            "name": "ESP LTD EC-256",
            "slug": "esp-ltd-ec-256",
            "brand": "ESP LTD",
            "category": "electric-guitars",
            "description": "The ESP LTD EC-256 offers single-cut styling with comfortable ergonomics, powerful pickups, and modern reliability at a wallet-friendly price.",
            "specifications": {
                "body_material": "Mahogany",
                "neck_material": "3-Piece Mahogany",
                "fingerboard": "Jatoba",
                "pickups": "LTD Humbuckers with Coil-Split",
                "scale_length": "24.75 inches",
                "frets": 22,
                "bridge": "TOM Bridge with Tailpiece",
                "tuners": "LTD",
                "nut_width": "1.65 inches",
                "finish": "Gloss Polyurethane"
            },
            "msrp_price": 499,
            "images": ["esp_ltd_ec256_1.jpg", "esp_ltd_ec256_2.jpg", "esp_ltd_ec256_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "EC-256 blends classic single-cut tones with modern coil-split versatility and comfortable contours for long sets.",
                "key_features": ["Coil-split humbuckers", "Comfortable belly cut", "Slim-U neck profile", "Reliable TOM bridge"],
                "target_skill_level": "Beginner to Intermediate",
                "country_of_origin": "China",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Thick, sustaining voice with usable single-coil-like options via splits",
                    "output_level": "Medium",
                    "best_genres": ["Rock", "Hard Rock", "Blues", "Alternative"],
                    "pickup_positions": {
                        "bridge": "Crunchy rhythms and singing leads",
                        "both_split": "Chimey cleans and funk-friendly rhythms",
                        "neck": "Warm, rounded cleans and fluid leads"
                    }
                },
                "build_quality": {
                    "construction_type": "Solid Body",
                    "hardware_quality": "Standard",
                    "finish_quality": "Clean binding and glossy finish typical of LTD",
                    "expected_durability": "Good"
                },
                "playability": {
                    "neck_profile": "Slim-U encourages fast movement without hand fatigue",
                    "action_setup": "Low action attainable; stable tuning",
                    "comfort_rating": "8/10 - Contours reduce shoulder fatigue",
                    "weight_category": "Medium"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Great Price-to-Performance", "description": "Modern features and strong QC at an approachable cost."},
                    {"title": "Versatile Coil-Splits", "description": "Covers cleans to crunch with one guitar."}
                ],
                "why_not_buy": [
                    {"title": "Non-USA Electronics", "description": "Stock pickups are solid but lack boutique nuance."}
                ],
                "best_for": [
                    {"user_type": "First serious electric or backup stage guitar", "reason": "Reliable, playable, and flexible."}
                ],
                "not_ideal_for": [
                    {"user_type": "Vintage purists", "reason": "Modern LTD appointments over vintage-correct specs."}
                ]
            },
            "usage_guidance": {
                "recommended_amplifiers": ["Crunchy tube combos", "Modelers", "Clean pedal platforms"],
                "suitable_music_styles": {
                    "excellent": ["Rock", "Hard Rock", "Alternative"],
                    "good": ["Blues", "Pop"],
                    "limited": ["Traditional jazz-only contexts"]
                },
                "skill_development": {
                    "learning_curve": "Low",
                    "growth_potential": "Strong mod platform (pickups/electronics) as skills advance"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Pickup height and coil-split wiring familiarity"],
                "care_instructions": {
                    "daily": "Wipe down; check coil-split switch function",
                    "weekly": "Inspect hardware and relief",
                    "monthly": "Intonation and fretboard care",
                    "annual": "Pro setup"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Pickup swap", "Electronics harness", "Locking tuners"],
                    "recommended_budget": "€120-250"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "8", "sound_quality": "7", "value_for_money": "9", "versatility": "8"},
                "standout_features": ["Slim-U neck", "Coil-split flexibility", "Comfort bevels"],
                "notable_limitations": ["Generic stock pickups"],
                "competitive_position": "Excellent in the €450-550 single-cut market for learners and gigging backups"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["ESP LTD EC-256", "single cut guitar", "coil split guitar", "LTD EC"],
                "readability_score": "Medium",
                "word_count": "580"
            }
        }
    },
    {
        "product_input": {
            "sku": "YAMAHA-PACIFICA-612VIIX",
            "name": "Yamaha Pacifica 612VIIX",
            "slug": "yamaha-pacifica-612viix",
            "brand": "Yamaha",
            "category": "electric-guitars",
            "description": "The Yamaha Pacifica 612VIIX is a premium take on the versatile HSS platform, pairing a Seymour Duncan humbucker with calibrated single-coils for stage-ready tones.",
            "specifications": {
                "body_material": "Alder",
                "neck_material": "Maple",
                "fingerboard": "Rosewood",
                "pickups": "Seymour Duncan TB-14 (Bridge) + SSL-1 (Middle/Neck)",
                "scale_length": "25.5 inches",
                "frets": 22,
                "bridge": "Wilkinson VS50 6 Tremolo",
                "tuners": "Grover Locking",
                "nut_width": "1.65 inches",
                "finish": "Gloss Polyurethane"
            },
            "msrp_price": 799,
            "images": ["yamaha_pacifica_612viix_1.jpg", "yamaha_pacifica_612viix_2.jpg", "yamaha_pacifica_612viix_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "Pacifica 612VIIX blends hot-rodded HSS versatility with pro hardware for reliable gigging and recording.",
                "key_features": ["Seymour Duncan HSS set", "Wilkinson VS50 trem", "Grover locking tuners", "Alder body"],
                "target_skill_level": "Intermediate to Advanced",
                "country_of_origin": "Indonesia",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Snappy single-coil clarity with muscular bridge humbucker punch",
                    "output_level": "Medium-High",
                    "best_genres": ["Pop", "Rock", "Funk", "Fusion", "Worship"],
                    "pickup_positions": {
                        "bridge": "Focused, authoritative leads and riffing",
                        "position_2": "Quack and sparkle for funk and clean rhythm",
                        "neck": "Rounded, articulate cleans and blues leads"
                    }
                },
                "build_quality": {
                    "construction_type": "Solid Body",
                    "hardware_quality": "Premium for price tier",
                    "finish_quality": "Clean fretwork and consistent finishing",
                    "expected_durability": "High"
                },
                "playability": {
                    "neck_profile": "Comfortable modern C with satin-like feel",
                    "action_setup": "Low action stability with Wilkinson vibrato",
                    "comfort_rating": "9/10 - Balanced, ergonomic body contours",
                    "weight_category": "Medium"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Stage-Ready Hardware", "description": "Locking tuners and Wilkinson trem keep tuning stable through sets."},
                    {"title": "Versatile HSS Palette", "description": "Covers glassy cleans to punchy drives with ease."}
                ],
                "why_not_buy": [
                    {"title": "Modern-leaning Voice", "description": "Those seeking strictly vintage tones may prefer traditional SSS."}
                ],
                "best_for": [
                    {"user_type": "Working players needing one guitar for many gigs", "reason": "Reliable tuning and wide tonal range."}
                ],
                "not_ideal_for": [
                    {"user_type": "Vintage-only stylists", "reason": "Hot-rodded HSS exceeds vintage spec."}
                ]
            },
            "usage_guidance": {
                "recommended_amplifiers": ["Clean platforms with pedals", "Modern modelers", "Low-watt tube combos"],
                "suitable_music_styles": {
                    "excellent": ["Pop", "Rock", "Funk", "Worship"],
                    "good": ["Indie", "Alternative"],
                    "limited": ["Strict vintage blues contexts"]
                },
                "skill_development": {
                    "learning_curve": "Low",
                    "growth_potential": "Remains capable as skills advance due to flexible electronics"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Tremolo spring balancing"],
                "care_instructions": {
                    "daily": "Wipe strings and body; check trem return",
                    "weekly": "Verify tuner locking and nut lubrication",
                    "monthly": "Setup: relief, action, intonation",
                    "annual": "Professional setup and fret polish"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Electronics harness", "Steel trem block"],
                    "recommended_budget": "€70-180"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "9", "sound_quality": "8", "value_for_money": "9", "versatility": "9"},
                "standout_features": ["Locking tuners", "Wilkinson bridge", "Seymour Duncan set"],
                "notable_limitations": ["Modern voice over pure vintage"],
                "competitive_position": "Competes strongly around €750-850 against premium HSS alternatives"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Yamaha Pacifica 612VIIX", "HSS guitar", "Wilkinson trem", "locking tuners"],
                "readability_score": "Medium",
                "word_count": "620"
            }
        }
    },
    {
        "product_input": {
            "sku": "GRETSCH-G2622-STREAMLINER",
            "name": "Gretsch G2622 Streamliner Center Block",
            "slug": "gretsch-g2622-streamliner",
            "brand": "Gretsch",
            "category": "electric-guitars",
            "description": "The Gretsch G2622 Streamliner is a center-block semi-hollow that marries classic Gretsch chime with modern feedback control and stage-ready stability.",
            "specifications": {
                "body_material": "Laminated Maple with Center Block",
                "neck_material": "Nato",
                "fingerboard": "Laurel",
                "pickups": "Broad’Tron BT-2S Humbuckers",
                "scale_length": "24.75 inches",
                "frets": 22,
                "bridge": "Adjusto-Matic with V-Stoptail",
                "tuners": "Die-cast",
                "nut_width": "1.6875 inches",
                "finish": "Gloss Polyurethane"
            },
            "msrp_price": 499,
            "images": ["gretsch_g2622_1.jpg", "gretsch_g2622_2.jpg", "gretsch_g2622_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "Center-block design tames feedback while Broad’Trons deliver chunky lows, open mids, and sparkling highs—Gretsch character made gig-friendly.",
                "key_features": ["Center-block semi-hollow", "Broad’Tron BT-2S", "Adjusto-Matic bridge", "Ergonomic thin ‘U’ neck"],
                "target_skill_level": "Beginner to Intermediate",
                "country_of_origin": "Indonesia",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Airy semi-hollow resonance with focused low-end and crisp attack",
                    "output_level": "Medium",
                    "best_genres": ["Indie", "Rock", "Blues", "Jazz", "Rockabilly"],
                    "pickup_positions": {
                        "bridge": "Gretsch twang with bite for rhythm and lead",
                        "both": "Full, airy chords with defined note separation",
                        "neck": "Warm, rounded jazz/blues tones"
                    }
                },
                "build_quality": {
                    "construction_type": "Semi-Hollow Center Block",
                    "hardware_quality": "Standard",
                    "finish_quality": "Clean binding and consistent finishing",
                    "expected_durability": "Good"
                },
                "playability": {
                    "neck_profile": "Thin ‘U’ for easy chording and leads",
                    "action_setup": "Comfortable medium-low action achievable",
                    "comfort_rating": "8/10 - Semi-hollow comfort with good balance",
                    "weight_category": "Medium"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Gretsch Character, Less Feedback", "description": "Center block allows higher stage volumes than full hollows."},
                    {"title": "Versatile Broad’Trons", "description": "From jangly cleans to gritty rock with clarity."}
                ],
                "why_not_buy": [
                    {"title": "Not a Full Hollow", "description": "Those seeking full hollow resonance and bloom may prefer G5420T-class."}
                ],
                "best_for": [
                    {"user_type": "Indie/alt players and blues-rock guitarists", "reason": "Semi-hollow snap with modern control."}
                ],
                "not_ideal_for": [
                    {"user_type": "Metal-only players", "reason": "Semi-hollow dynamics and pickups are not voiced for extreme gain."}
                ]
            },
            "usage_guidance": {
                "recommended_amplifiers": ["Clean pedal platforms", "Chime-friendly tube combos", "Low-watt studio amps"],
                "suitable_music_styles": {
                    "excellent": ["Indie", "Blues", "Rockabilly", "Jazz"],
                    "good": ["Rock", "Pop"],
                    "limited": ["High-gain metal"]
                },
                "skill_development": {
                    "learning_curve": "Low",
                    "growth_potential": "Semi-hollow articulation rewards touch and dynamics"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Humidity for laminated maple", "Bridge height tweaks"],
                "care_instructions": {
                    "daily": "Wipe strings/body; store away from heat",
                    "weekly": "Check bridge posts and screws",
                    "monthly": "Truss and intonation check",
                    "annual": "Pro setup"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Nut upgrade", "Electronics harness", "Bridge saddles"],
                    "recommended_budget": "€80-200"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "8", "sound_quality": "8", "value_for_money": "9", "versatility": "8"},
                "standout_features": ["Center-block control", "Gretsch chime", "Comfortable neck"],
                "notable_limitations": ["Less hollow bloom than full hollows"],
                "competitive_position": "Excellent option around €450-550 among semi-hollow center-blocks"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Gretsch G2622", "Streamliner", "semi-hollow center block", "Broad’Tron"],
                "readability_score": "Medium",
                "word_count": "600"
            }
        }
    }
]


async def get_or_create_brand(session: AsyncSession, name: str) -> Brand:
    res = await session.execute(select(Brand).where(Brand.name == name))
    brand = res.scalar_one_or_none()
    if brand:
        return brand
    brand = Brand(name=name, slug=name.lower().replace(" ", "-"), description=f"{name} instruments")
    session.add(brand)
    await session.flush()
    return brand


async def get_or_create_category(session: AsyncSession, slug: str) -> Category:
    res = await session.execute(select(Category).where(Category.slug == slug))
    cat = res.scalar_one_or_none()
    if cat:
        return cat
    name = slug.replace("-", " ").title()
    cat = Category(name=name, slug=slug, description=f"{name}")
    session.add(cat)
    await session.flush()
    return cat


async def insert_products():
    async with async_session_factory() as session:
        created = 0
        for item in NEW_PRODUCTS:
            pi = item["product_input"]
            agc = item["ai_generated_content"]

            # exists?
            res = await session.execute(select(Product).where(Product.sku == pi["sku"]))
            if res.scalar_one_or_none():
                print(f"Product {pi['sku']} already exists, skipping")
                continue

            brand = await get_or_create_brand(session, pi["brand"])
            category = await get_or_create_category(session, pi["category"])

            product = Product(
                sku=pi["sku"],
                name=pi["name"],
                slug=pi["slug"],
                brand_id=brand.id,
                category_id=category.id,
                description=pi["description"],
                specifications=pi["specifications"],
                images=pi["images"],
                msrp_price=Decimal(str(pi["msrp_price"])),
                ai_generated_content=agc,
                is_active=True,
            )
            session.add(product)
            created += 1
            print(f"Created product: {pi['name']}")
        await session.commit()
        print(f"Successfully created {created} new electric guitars")


if __name__ == "__main__":
    asyncio.run(insert_products())
