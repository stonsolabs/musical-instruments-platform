#!/usr/bin/env python3
"""
Add products for missing categories that are in the frontend navigation but not in the database.
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

MISSING_CATEGORY_PRODUCTS = [
    # Pianos & Keyboards (2 products)
    {
        "product_input": {
            "sku": "KAWAI-ES110-DIGITAL-PIANO",
            "name": "Kawai ES110 Digital Piano",
            "slug": "kawai-es110-digital-piano",
            "brand": "Kawai",
            "category": "pianos-keyboards",
            "description": "The Kawai ES110 is a portable digital piano that delivers authentic grand piano touch and tone in a lightweight, stage-ready package.",
            "specifications": {
                "keyboard": "88-key RHIII (Responsive Hammer III) action",
                "sounds": "19 sounds including Concert Grand, Upright Piano, Electric Piano",
                "polyphony": "192-note polyphony",
                "connectivity": "USB, MIDI, Headphone jacks",
                "speakers": "Built-in 14W + 14W amplifiers",
                "weight": "12.5 kg",
                "dimensions": "131.2 x 29.5 x 13.2 cm",
                "power": "AC adapter or 6 AA batteries"
            },
            "msrp_price": 899,
            "images": ["kawai_es110_1.jpg", "kawai_es110_2.jpg", "kawai_es110_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "ES110 combines Kawai's renowned RHIII action with SK-EX grand piano samples for authentic playing experience.",
                "key_features": ["RHIII hammer action", "SK-EX grand piano samples", "192-note polyphony", "Portable design"],
                "target_skill_level": "Beginner to Advanced",
                "country_of_origin": "Indonesia",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Warm, rich grand piano tone with excellent dynamic response",
                    "keyboard_action": "RHIII provides authentic grand piano feel with graded hammer action",
                    "best_genres": ["Classical", "Jazz", "Pop", "Contemporary"],
                    "sound_quality": "High-quality SK-EX samples with realistic resonance"
                },
                "build_quality": {
                    "construction_type": "Portable Digital Piano",
                    "hardware_quality": "Professional grade",
                    "finish_quality": "Durable plastic construction with metal frame",
                    "expected_durability": "High"
                },
                "playability": {
                    "keyboard_response": "Excellent dynamic range and touch sensitivity",
                    "action_weight": "Graded hammer action mimics acoustic piano",
                    "comfort_rating": "9/10 - Natural piano feel with good key spacing",
                    "portability": "Lightweight and easy to transport"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Authentic Piano Feel", "description": "RHIII action provides genuine grand piano touch response."},
                    {"title": "Portable Professional Quality", "description": "Stage-ready with excellent sound and lightweight design."}
                ],
                "why_not_buy": [
                    {"title": "Limited Sound Variety", "description": "Only 19 sounds compared to some competitors with 100+."}
                ],
                "best_for": [
                    {"user_type": "Pianists needing portable instrument", "reason": "Authentic piano feel in lightweight package."}
                ],
                "not_ideal_for": [
                    {"user_type": "Those needing extensive sound library", "reason": "Limited sound variety compared to workstations."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Home practice", "Live performance", "Studio recording", "Music education"],
                "suitable_music_styles": {
                    "excellent": ["Classical", "Jazz", "Pop", "Contemporary"],
                    "good": ["Rock", "Blues"],
                    "limited": ["Electronic music requiring extensive sound design"]
                },
                "skill_development": {
                    "learning_curve": "Low for piano players",
                    "growth_potential": "Suitable from beginner to professional level"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Dust accumulation on keys", "Power adapter wear"],
                "care_instructions": {
                    "daily": "Wipe keys with soft cloth",
                    "weekly": "Check connections and clean surface",
                    "monthly": "Inspect power adapter and cables",
                    "annual": "Professional inspection if needed"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Better headphones", "Piano bench", "Stand upgrade"],
                    "recommended_budget": "€100-300"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "9", "sound_quality": "9", "value_for_money": "9", "versatility": "7"},
                "standout_features": ["RHIII action", "SK-EX samples", "Portability"],
                "notable_limitations": ["Limited sound variety"],
                "competitive_position": "Excellent value in portable digital piano market"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Kawai ES110", "digital piano", "portable piano", "RHIII action"],
                "readability_score": "Medium",
                "word_count": "550"
            }
        }
    },
    {
        "product_input": {
            "sku": "NORD-PIANO-5-88",
            "name": "Nord Piano 5 88",
            "slug": "nord-piano-5-88",
            "brand": "Nord",
            "category": "pianos-keyboards",
            "description": "The Nord Piano 5 88 is a premium stage piano featuring Nord's acclaimed piano library, triple sensor keybed, and professional-grade build quality for demanding live performances.",
            "specifications": {
                "keyboard": "88-key triple sensor weighted hammer action",
                "sounds": "Nord Piano Library with 2GB memory",
                "polyphony": "120-note polyphony",
                "connectivity": "USB, MIDI, Audio In/Out, Headphones",
                "speakers": "None (stage piano)",
                "weight": "18.5 kg",
                "dimensions": "128.2 x 12.2 x 35.5 cm",
                "power": "AC adapter"
            },
            "msrp_price": 3499,
            "images": ["nord_piano_5_88_1.jpg", "nord_piano_5_88_2.jpg", "nord_piano_5_88_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "Nord Piano 5 88 delivers world-class piano sounds with exceptional playability for professional stage use.",
                "key_features": ["Nord Piano Library", "Triple sensor keybed", "2GB sample memory", "Professional build"],
                "target_skill_level": "Professional",
                "country_of_origin": "Sweden",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Exceptional piano realism with detailed sampling and natural resonance",
                    "keyboard_action": "Premium triple sensor action with excellent dynamic response",
                    "best_genres": ["Jazz", "Classical", "Pop", "Contemporary", "Studio"],
                    "sound_quality": "Industry-leading piano samples with authentic character"
                },
                "build_quality": {
                    "construction_type": "Professional Stage Piano",
                    "hardware_quality": "Premium",
                    "finish_quality": "Durable metal construction with distinctive red finish",
                    "expected_durability": "Very High"
                },
                "playability": {
                    "keyboard_response": "Exceptional touch sensitivity and dynamic range",
                    "action_weight": "Professional weighted action with triple sensors",
                    "comfort_rating": "10/10 - Premium feel and response",
                    "stage_readiness": "Built for professional touring"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Industry-Leading Piano Sounds", "description": "Nord Piano Library offers unmatched piano realism."},
                    {"title": "Professional Build Quality", "description": "Built to withstand rigorous touring and studio use."}
                ],
                "why_not_buy": [
                    {"title": "High Price Point", "description": "Premium instrument with premium price tag."}
                ],
                "best_for": [
                    {"user_type": "Professional pianists and touring musicians", "reason": "Industry standard for stage piano performance."}
                ],
                "not_ideal_for": [
                    {"user_type": "Beginners or casual players", "reason": "Overkill for basic needs and expensive investment."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Professional live performance", "Studio recording", "High-end home use"],
                "suitable_music_styles": {
                    "excellent": ["Jazz", "Classical", "Pop", "Contemporary"],
                    "good": ["Rock", "Blues", "Fusion"],
                    "limited": ["None - versatile for all styles"]
                },
                "skill_development": {
                    "learning_curve": "Low for experienced pianists",
                    "growth_potential": "Professional instrument that grows with player"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Firmware updates", "Sample library management"],
                "care_instructions": {
                    "daily": "Wipe keys and check connections",
                    "weekly": "Update sample library if needed",
                    "monthly": "Check firmware and backup settings",
                    "annual": "Professional inspection and cleaning"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Additional sample libraries", "Better amplification"],
                    "recommended_budget": "€500-2000"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "10", "sound_quality": "10", "value_for_money": "8", "versatility": "9"},
                "standout_features": ["Nord Piano Library", "Professional build", "Triple sensor action"],
                "notable_limitations": ["High price", "No built-in speakers"],
                "competitive_position": "Top-tier professional stage piano"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Nord Piano 5", "stage piano", "professional piano", "Nord Piano Library"],
                "readability_score": "Medium",
                "word_count": "580"
            }
        }
    },
    # Orchestral (2 products)
    {
        "product_input": {
            "sku": "YAMAHA-YAS-280-ALTO-SAX",
            "name": "Yamaha YAS-280 Alto Saxophone",
            "slug": "yamaha-yas-280-alto-saxophone",
            "brand": "Yamaha",
            "category": "orchestral",
            "description": "The Yamaha YAS-280 is a student-friendly alto saxophone that offers excellent playability, consistent intonation, and durable construction for developing musicians.",
            "specifications": {
                "key": "Eb Alto Saxophone",
                "body_material": "Yellow brass",
                "finish": "Clear lacquer",
                "keys": "High F# key, Front F key",
                "case": "Lightweight hard case included",
                "mouthpiece": "4C mouthpiece included",
                "ligature": "Standard ligature included",
                "cleaning_kit": "Basic cleaning kit included"
            },
            "msrp_price": 1299,
            "images": ["yamaha_yas280_1.jpg", "yamaha_yas280_2.jpg", "yamaha_yas280_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "YAS-280 provides excellent student saxophone with Yamaha's renowned quality and playability.",
                "key_features": ["High F# key", "Front F key", "Clear lacquer finish", "Complete starter package"],
                "target_skill_level": "Beginner to Intermediate",
                "country_of_origin": "Indonesia",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Bright, focused tone with good projection",
                    "intonation": "Consistent and reliable across all registers",
                    "best_genres": ["Jazz", "Classical", "Pop", "Marching Band"],
                    "response": "Quick response with good dynamic control"
                },
                "build_quality": {
                    "construction_type": "Student Grade",
                    "hardware_quality": "Reliable",
                    "finish_quality": "Durable lacquer finish",
                    "expected_durability": "Good"
                },
                "playability": {
                    "key_action": "Light and responsive",
                    "ergonomics": "Comfortable hand position and key placement",
                    "comfort_rating": "8/10 - Easy to play for students",
                    "weight": "Standard weight for alto saxophone"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Yamaha Quality", "description": "Reliable construction and consistent playability."},
                    {"title": "Complete Package", "description": "Includes everything needed to start playing."}
                ],
                "why_not_buy": [
                    {"title": "Student Level", "description": "Not suitable for advanced professional use."}
                ],
                "best_for": [
                    {"user_type": "Students and beginners", "reason": "Excellent starter instrument with good quality."}
                ],
                "not_ideal_for": [
                    {"user_type": "Professional players", "reason": "Student-level instrument with limitations."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Student practice", "School band", "Beginner lessons"],
                "suitable_music_styles": {
                    "excellent": ["Jazz", "Classical", "Pop"],
                    "good": ["Rock", "Blues"],
                    "limited": ["None - versatile for all styles"]
                },
                "skill_development": {
                    "learning_curve": "Moderate",
                    "growth_potential": "Good for 2-3 years of development"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Medium",
                "common_issues": ["Pad replacement", "Key adjustment", "Regular cleaning"],
                "care_instructions": {
                    "daily": "Clean after playing, swab out moisture",
                    "weekly": "Check for loose screws and keys",
                    "monthly": "Clean body and keys thoroughly",
                    "annual": "Professional inspection and adjustment"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Better mouthpiece", "Professional reeds", "Upgraded ligature"],
                    "recommended_budget": "€100-300"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "8", "sound_quality": "7", "value_for_money": "9", "versatility": "8"},
                "standout_features": ["Yamaha reliability", "Complete package", "Good intonation"],
                "notable_limitations": ["Student-level construction"],
                "competitive_position": "Excellent value in student saxophone market"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Yamaha YAS-280", "alto saxophone", "student saxophone", "Yamaha sax"],
                "readability_score": "Medium",
                "word_count": "520"
            }
        }
    },
    {
        "product_input": {
            "sku": "SELMER-PARIS-PRELUDE-VIOLIN",
            "name": "Selmer Paris Prelude Violin",
            "slug": "selmer-paris-prelude-violin",
            "brand": "Selmer Paris",
            "category": "orchestral",
            "description": "The Selmer Paris Prelude Violin offers exceptional craftsmanship and warm, resonant tone for intermediate to advanced violinists seeking professional quality.",
            "specifications": {
                "size": "4/4 Full Size",
                "body_material": "Spruce top, Maple back and sides",
                "fingerboard": "Ebony",
                "bridge": "Hand-carved maple",
                "tailpiece": "Composite with built-in fine tuners",
                "strings": "Dominant strings included",
                "bow": "Brazilwood bow with horsehair",
                "case": "Lightweight hard case included"
            },
            "msrp_price": 2499,
            "images": ["selmer_prelude_violin_1.jpg", "selmer_prelude_violin_2.jpg", "selmer_prelude_violin_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "Prelude violin combines Selmer's expertise with warm, projecting tone for serious players.",
                "key_features": ["Hand-carved bridge", "Dominant strings", "Professional setup", "Quality case"],
                "target_skill_level": "Intermediate to Advanced",
                "country_of_origin": "France",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Warm, rich tone with excellent projection",
                    "response": "Quick response with good dynamic range",
                    "best_genres": ["Classical", "Folk", "Jazz", "Contemporary"],
                    "resonance": "Excellent resonance and sustain"
                },
                "build_quality": {
                    "construction_type": "Professional Grade",
                    "hardware_quality": "High",
                    "finish_quality": "Beautiful varnish finish",
                    "expected_durability": "Very High"
                },
                "playability": {
                    "setup": "Professional setup with proper string height",
                    "ergonomics": "Comfortable neck profile and fingerboard",
                    "comfort_rating": "9/10 - Excellent playability",
                    "weight": "Standard violin weight"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Selmer Quality", "description": "Professional craftsmanship and reliable construction."},
                    {"title": "Warm Tone", "description": "Rich, projecting sound suitable for various styles."}
                ],
                "why_not_buy": [
                    {"title": "Higher Price", "description": "Premium instrument with premium price tag."}
                ],
                "best_for": [
                    {"user_type": "Intermediate to advanced players", "reason": "Professional quality suitable for serious study."}
                ],
                "not_ideal_for": [
                    {"user_type": "Complete beginners", "reason": "Overkill for first instrument."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Solo performance", "Orchestra", "Chamber music", "Recording"],
                "suitable_music_styles": {
                    "excellent": ["Classical", "Folk", "Jazz"],
                    "good": ["Contemporary", "Pop"],
                    "limited": ["None - versatile for all styles"]
                },
                "skill_development": {
                    "learning_curve": "Moderate to High",
                    "growth_potential": "Suitable for advanced study and performance"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Medium",
                "common_issues": ["String replacement", "Bridge adjustment", "Regular cleaning"],
                "care_instructions": {
                    "daily": "Wipe down after playing, loosen bow",
                    "weekly": "Check bridge position and string condition",
                    "monthly": "Clean body and fingerboard",
                    "annual": "Professional setup and inspection"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Professional strings", "Better bow", "Upgraded tailpiece"],
                    "recommended_budget": "€200-800"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "9", "sound_quality": "9", "value_for_money": "8", "versatility": "9"},
                "standout_features": ["Selmer craftsmanship", "Warm tone", "Professional setup"],
                "notable_limitations": ["Higher price point"],
                "competitive_position": "Excellent mid-range professional violin"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Selmer Paris Prelude", "violin", "professional violin", "Selmer violin"],
                "readability_score": "Medium",
                "word_count": "540"
            }
        }
    },
    # Live Sound & Lighting (2 products)
    {
        "product_input": {
            "sku": "YAMAHA-DXR12-PA-SPEAKER",
            "name": "Yamaha DXR12 Powered PA Speaker",
            "slug": "yamaha-dxr12-powered-pa-speaker",
            "brand": "Yamaha",
            "category": "live-sound-lighting",
            "description": "The Yamaha DXR12 is a professional powered PA speaker delivering 1100W of power with exceptional clarity and reliability for live sound applications.",
            "specifications": {
                "power": "1100W (LF: 700W, HF: 400W)",
                "drivers": "12\" LF driver, 1.4\" HF compression driver",
                "frequency_response": "52Hz - 20kHz",
                "max_spl": "132 dB",
                "inputs": "2x XLR/TRS combo, 1x XLR link out",
                "dsp": "Built-in DSP with presets",
                "weight": "18.5 kg",
                "dimensions": "35.5 x 53.5 x 30.5 cm",
                "mounting": "Pole mount, fly points"
            },
            "msrp_price": 699,
            "images": ["yamaha_dxr12_1.jpg", "yamaha_dxr12_2.jpg", "yamaha_dxr12_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "DXR12 provides professional sound reinforcement with Yamaha's reliability and built-in DSP processing.",
                "key_features": ["1100W power", "Built-in DSP", "Multiple mounting options", "Professional build"],
                "target_skill_level": "Professional",
                "country_of_origin": "Indonesia",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Clear, articulate sound with excellent vocal reproduction",
                    "power_output": "High power handling with clean amplification",
                    "best_applications": ["Live bands", "DJ setups", "Corporate events", "Outdoor events"],
                    "coverage": "Wide dispersion pattern for good audience coverage"
                },
                "build_quality": {
                    "construction_type": "Professional PA Speaker",
                    "hardware_quality": "High",
                    "finish_quality": "Durable enclosure with protective grille",
                    "expected_durability": "Very High"
                },
                "playability": {
                    "setup_ease": "Simple plug-and-play operation",
                    "versatility": "Multiple input options and mounting configurations",
                    "comfort_rating": "9/10 - Easy to set up and use",
                    "portability": "Heavy but manageable with handles"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Professional Quality", "description": "Yamaha reliability with excellent sound quality."},
                    {"title": "Built-in DSP", "description": "Multiple presets for different applications."}
                ],
                "why_not_buy": [
                    {"title": "Heavy Weight", "description": "18.5kg may be too heavy for some applications."}
                ],
                "best_for": [
                    {"user_type": "Professional sound engineers and bands", "reason": "Reliable, powerful sound reinforcement."}
                ],
                "not_ideal_for": [
                    {"user_type": "Home users", "reason": "Overkill for home use and expensive."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Live music", "DJ events", "Corporate presentations", "Outdoor events"],
                "suitable_applications": {
                    "excellent": ["Live bands", "DJ setups", "Corporate events"],
                    "good": ["Small venues", "Outdoor events"],
                    "limited": ["Home use", "Very small spaces"]
                },
                "skill_development": {
                    "learning_curve": "Low",
                    "growth_potential": "Professional tool that grows with user needs"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Dust accumulation", "Cable wear"],
                "care_instructions": {
                    "daily": "Wipe down after use",
                    "weekly": "Check connections and clean grille",
                    "monthly": "Inspect for damage and test all inputs",
                    "annual": "Professional inspection if needed"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Better cables", "Speaker stands", "Subwoofer addition"],
                    "recommended_budget": "€200-800"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "9", "sound_quality": "9", "value_for_money": "9", "versatility": "9"},
                "standout_features": ["High power", "Built-in DSP", "Professional build"],
                "notable_limitations": ["Heavy weight"],
                "competitive_position": "Excellent value in professional PA speaker market"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Yamaha DXR12", "PA speaker", "powered speaker", "live sound"],
                "readability_score": "Medium",
                "word_count": "520"
            }
        }
    },
    {
        "product_input": {
            "sku": "CHAUVET-DJ-SCENE-PAR-64",
            "name": "Chauvet DJ Scene PAR 64 LED Light",
            "slug": "chauvet-dj-scene-par-64-led-light",
            "brand": "Chauvet DJ",
            "category": "live-sound-lighting",
            "description": "The Chauvet DJ Scene PAR 64 is a versatile LED par light featuring 64 high-output LEDs with multiple color modes and DMX control for professional lighting effects.",
            "specifications": {
                "leds": "64 x 1W RGB LEDs",
                "power": "64W total power consumption",
                "beam_angle": "25° narrow beam",
                "control": "DMX-512, Auto, Sound Active",
                "modes": "7-color, 7-color fade, 7-color chase, DMX",
                "dimming": "0-100% smooth dimming",
                "weight": "2.3 kg",
                "dimensions": "25.4 x 25.4 x 30.5 cm",
                "mounting": "Yoke mount included"
            },
            "msrp_price": 199,
            "images": ["chauvet_scene_par64_1.jpg", "chauvet_scene_par64_2.jpg", "chauvet_scene_par64_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "Scene PAR 64 delivers bright, colorful lighting with multiple control options for DJ and live performance applications.",
                "key_features": ["64 RGB LEDs", "DMX control", "Multiple modes", "Lightweight design"],
                "target_skill_level": "Beginner to Professional",
                "country_of_origin": "China",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "lighting_characteristics": {
                    "brightness": "High output with good color mixing",
                    "color_quality": "Rich, saturated colors with smooth transitions",
                    "best_applications": ["DJ setups", "Live bands", "Weddings", "Corporate events"],
                    "coverage": "25° beam angle provides focused lighting"
                },
                "build_quality": {
                    "construction_type": "Professional LED Light",
                    "hardware_quality": "Good",
                    "finish_quality": "Durable metal housing with protective lens",
                    "expected_durability": "Good"
                },
                "playability": {
                    "setup_ease": "Simple mounting and operation",
                    "versatility": "Multiple control modes for different needs",
                    "comfort_rating": "8/10 - Easy to set up and control",
                    "portability": "Lightweight and easy to transport"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Versatile Control", "description": "Multiple modes from simple auto to full DMX control."},
                    {"title": "Bright Output", "description": "64 LEDs provide excellent brightness and color mixing."}
                ],
                "why_not_buy": [
                    {"title": "Basic Features", "description": "Limited compared to higher-end moving lights."}
                ],
                "best_for": [
                    {"user_type": "DJs and small venues", "reason": "Good value for professional lighting effects."}
                ],
                "not_ideal_for": [
                    {"user_type": "Large venues", "reason": "May need multiple units for adequate coverage."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["DJ performances", "Live bands", "Weddings", "Small venues"],
                "suitable_applications": {
                    "excellent": ["DJ setups", "Small live venues"],
                    "good": ["Weddings", "Corporate events"],
                    "limited": ["Large concert venues"]
                },
                "skill_development": {
                    "learning_curve": "Low",
                    "growth_potential": "Good starting point for lighting setup"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Dust on lens", "Cable wear"],
                "care_instructions": {
                    "daily": "Wipe lens clean after use",
                    "weekly": "Check connections and clean housing",
                    "monthly": "Test all modes and DMX functions",
                    "annual": "Professional inspection if needed"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["DMX controller", "Lighting stand", "Additional units"],
                    "recommended_budget": "€100-500"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "8", "sound_quality": "8", "value_for_money": "9", "versatility": "8"},
                "standout_features": ["Bright output", "Multiple modes", "DMX control"],
                "notable_limitations": ["Basic features", "Single beam angle"],
                "competitive_position": "Good value in entry-level professional lighting"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Chauvet DJ Scene PAR 64", "LED light", "DMX light", "DJ lighting"],
                "readability_score": "Medium",
                "word_count": "500"
            }
        }
    },
    # Studio & Production (2 products)
    {
        "product_input": {
            "sku": "UNIVERSAL-AUDIO-APOLLO-TWIN-X",
            "name": "Universal Audio Apollo Twin X",
            "slug": "universal-audio-apollo-twin-x",
            "brand": "Universal Audio",
            "category": "studio-production",
            "description": "The Apollo Twin X is a premium audio interface featuring UA's acclaimed analog modeling technology, pristine converters, and real-time UAD processing for professional studio recording.",
            "specifications": {
                "inputs": "2x Unison preamps, 2x line inputs",
                "outputs": "2x line outputs, 1x headphone output",
                "converters": "24-bit/192kHz AD/DA conversion",
                "dsp": "Real-time UAD processing",
                "connectivity": "Thunderbolt 3, USB-C",
                "software": "UAD software bundle included",
                "phantom_power": "48V phantom power",
                "monitoring": "Zero-latency monitoring"
            },
            "msrp_price": 899,
            "images": ["ua_apollo_twin_x_1.jpg", "ua_apollo_twin_x_2.jpg", "ua_apollo_twin_x_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "Apollo Twin X combines pristine audio conversion with real-time UAD processing for professional studio quality.",
                "key_features": ["Unison preamps", "Real-time UAD processing", "Thunderbolt 3", "Professional converters"],
                "target_skill_level": "Professional",
                "country_of_origin": "USA",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "audio_characteristics": {
                    "conversion_quality": "24-bit/192kHz pristine conversion",
                    "preamps": "Unison technology for authentic analog modeling",
                    "best_applications": ["Studio recording", "Voice-over", "Music production", "Podcasting"],
                    "latency": "Near-zero latency monitoring"
                },
                "build_quality": {
                    "construction_type": "Professional Audio Interface",
                    "hardware_quality": "Premium",
                    "finish_quality": "Durable metal construction",
                    "expected_durability": "Very High"
                },
                "playability": {
                    "setup_ease": "Simple Thunderbolt connection",
                    "software_integration": "Seamless UAD software integration",
                    "comfort_rating": "9/10 - Professional ease of use",
                    "reliability": "Industry-standard reliability"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "UAD Processing", "description": "Real-time access to legendary analog modeling."},
                    {"title": "Professional Quality", "description": "Industry-standard conversion and preamps."}
                ],
                "why_not_buy": [
                    {"title": "High Price", "description": "Premium interface with premium price tag."}
                ],
                "best_for": [
                    {"user_type": "Professional studios and serious producers", "reason": "Industry-standard quality and processing."}
                ],
                "not_ideal_for": [
                    {"user_type": "Beginners", "reason": "Overkill for basic recording needs."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Professional recording", "Music production", "Voice-over", "Studio monitoring"],
                "suitable_applications": {
                    "excellent": ["Studio recording", "Music production"],
                    "good": ["Voice-over", "Podcasting"],
                    "limited": ["Basic home recording"]
                },
                "skill_development": {
                    "learning_curve": "Moderate",
                    "growth_potential": "Professional tool that grows with user skills"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Driver updates", "Software updates"],
                "care_instructions": {
                    "daily": "Check connections and software status",
                    "weekly": "Update drivers and software if needed",
                    "monthly": "Clean connections and test all functions",
                    "annual": "Professional inspection if needed"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Additional UAD plugins", "Better monitoring", "Additional interfaces"],
                    "recommended_budget": "€500-2000"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "10", "sound_quality": "10", "value_for_money": "8", "versatility": "9"},
                "standout_features": ["UAD processing", "Unison preamps", "Professional quality"],
                "notable_limitations": ["High price", "Limited inputs"],
                "competitive_position": "Top-tier professional audio interface"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Universal Audio Apollo Twin X", "audio interface", "UAD processing", "studio interface"],
                "readability_score": "Medium",
                "word_count": "540"
            }
        }
    },
    {
        "product_input": {
            "sku": "NEUMANN-TLM-103-MICROPHONE",
            "name": "Neumann TLM 103 Large-Diaphragm Condenser Microphone",
            "slug": "neumann-tlm-103-large-diaphragm-condenser-microphone",
            "brand": "Neumann",
            "category": "studio-production",
            "description": "The Neumann TLM 103 is a premium large-diaphragm condenser microphone delivering the legendary Neumann sound quality with exceptional detail and warmth for professional recording.",
            "specifications": {
                "type": "Large-diaphragm condenser",
                "polar_pattern": "Cardioid",
                "frequency_response": "20Hz - 20kHz",
                "sensitivity": "23 mV/Pa",
                "impedance": "50 ohms",
                "max_spl": "138 dB",
                "self_noise": "7 dB-A",
                "power": "48V phantom power required",
                "weight": "420g"
            },
            "msrp_price": 1199,
            "images": ["neumann_tlm103_1.jpg", "neumann_tlm103_2.jpg", "neumann_tlm103_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "TLM 103 brings Neumann's legendary sound quality to a more accessible price point with exceptional detail and warmth.",
                "key_features": ["Large-diaphragm condenser", "Neumann quality", "Low self-noise", "Professional build"],
                "target_skill_level": "Professional",
                "country_of_origin": "Germany",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "audio_characteristics": {
                    "tonal_profile": "Warm, detailed sound with excellent transient response",
                    "frequency_response": "Flat, natural response with slight presence boost",
                    "best_applications": ["Vocals", "Acoustic instruments", "Voice-over", "Studio recording"],
                    "noise_floor": "Very low self-noise for clean recordings"
                },
                "build_quality": {
                    "construction_type": "Professional Condenser Microphone",
                    "hardware_quality": "Premium",
                    "finish_quality": "Exceptional German craftsmanship",
                    "expected_durability": "Very High"
                },
                "playability": {
                    "setup_ease": "Standard XLR connection with phantom power",
                    "versatility": "Excellent for vocals and acoustic instruments",
                    "comfort_rating": "9/10 - Professional ease of use",
                    "reliability": "Industry-standard Neumann reliability"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Neumann Quality", "description": "Legendary German craftsmanship and sound quality."},
                    {"title": "Versatile Performance", "description": "Excellent for vocals and acoustic instruments."}
                ],
                "why_not_buy": [
                    {"title": "High Price", "description": "Premium microphone with premium price tag."}
                ],
                "best_for": [
                    {"user_type": "Professional studios and serious recording", "reason": "Industry-standard quality and reliability."}
                ],
                "not_ideal_for": [
                    {"user_type": "Beginners", "reason": "Overkill for basic recording needs."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Studio vocals", "Acoustic instruments", "Voice-over", "Professional recording"],
                "suitable_applications": {
                    "excellent": ["Studio vocals", "Acoustic instruments"],
                    "good": ["Voice-over", "Podcasting"],
                    "limited": ["Live performance", "Basic home recording"]
                },
                "skill_development": {
                    "learning_curve": "Low",
                    "growth_potential": "Professional tool that grows with user skills"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Dust accumulation", "Cable wear"],
                "care_instructions": {
                    "daily": "Wipe down after use",
                    "weekly": "Check connections and clean grille",
                    "monthly": "Inspect for damage and test functionality",
                    "annual": "Professional inspection if needed"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Better shock mount", "Professional pop filter", "High-quality cables"],
                    "recommended_budget": "€200-500"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "10", "sound_quality": "10", "value_for_money": "8", "versatility": "9"},
                "standout_features": ["Neumann quality", "Low self-noise", "Professional build"],
                "notable_limitations": ["High price", "Single polar pattern"],
                "competitive_position": "Excellent mid-range professional microphone"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Neumann TLM 103", "condenser microphone", "studio microphone", "Neumann mic"],
                "readability_score": "Medium",
                "word_count": "520"
            }
        }
    },
    # Music Software (2 products)
    {
        "product_input": {
            "sku": "ABLETON-LIVE-11-SUITE",
            "name": "Ableton Live 11 Suite",
            "slug": "ableton-live-11-suite",
            "brand": "Ableton",
            "category": "music-software",
            "description": "Ableton Live 11 Suite is a comprehensive music production and performance software featuring advanced audio and MIDI tools, built-in instruments, and real-time performance capabilities.",
            "specifications": {
                "platform": "Windows 10/11, macOS 10.15+",
                "audio_formats": "WAV, AIFF, MP3, FLAC, OGG",
                "max_tracks": "Unlimited",
                "plugins": "Built-in instruments and effects",
                "included_content": "70+ GB of sounds and samples",
                "features": "Real-time performance, MIDI sequencing, Audio recording",
                "licensing": "Perpetual license",
                "updates": "Free updates within version"
            },
            "msrp_price": 749,
            "images": ["ableton_live_11_suite_1.jpg", "ableton_live_11_suite_2.jpg", "ableton_live_11_suite_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "Live 11 Suite offers comprehensive music production tools with exceptional real-time performance capabilities.",
                "key_features": ["Real-time performance", "Built-in instruments", "70+ GB content", "Advanced MIDI"],
                "target_skill_level": "Intermediate to Professional",
                "country_of_origin": "Germany",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "software_characteristics": {
                    "workflow": "Unique session and arrangement views",
                    "performance": "Real-time audio manipulation and effects",
                    "best_applications": ["Electronic music", "Live performance", "Music production", "Sound design"],
                    "stability": "Industry-standard stability and reliability"
                },
                "build_quality": {
                    "construction_type": "Professional Music Software",
                    "hardware_quality": "Software-based",
                    "finish_quality": "Polished interface with excellent workflow",
                    "expected_durability": "Very High"
                },
                "playability": {
                    "learning_curve": "Moderate to steep",
                    "workflow_efficiency": "Excellent once mastered",
                    "comfort_rating": "8/10 - Intuitive for electronic music production",
                    "performance": "Real-time capabilities for live performance"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Real-time Performance", "description": "Unique live performance capabilities unmatched by other DAWs."},
                    {"title": "Comprehensive Suite", "description": "Complete production environment with extensive content."}
                ],
                "why_not_buy": [
                    {"title": "Learning Curve", "description": "Unique workflow may not suit traditional recording approaches."}
                ],
                "best_for": [
                    {"user_type": "Electronic music producers and live performers", "reason": "Specialized workflow for electronic music and performance."}
                ],
                "not_ideal_for": [
                    {"user_type": "Traditional recording engineers", "reason": "Workflow optimized for electronic music over traditional recording."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Electronic music production", "Live performance", "Sound design", "Music composition"],
                "suitable_applications": {
                    "excellent": ["Electronic music", "Live performance"],
                    "good": ["Sound design", "Music production"],
                    "limited": ["Traditional recording", "Orchestral scoring"]
                },
                "skill_development": {
                    "learning_curve": "Moderate to steep",
                    "growth_potential": "Extensive capabilities that grow with user skills"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Plugin compatibility", "System requirements"],
                "care_instructions": {
                    "daily": "Save projects regularly",
                    "weekly": "Update software and plugins",
                    "monthly": "Backup projects and preferences",
                    "annual": "Check system compatibility"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Additional plugins", "Hardware controllers", "Sample libraries"],
                    "recommended_budget": "€200-1000"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "9", "sound_quality": "9", "value_for_money": "8", "versatility": "9"},
                "standout_features": ["Real-time performance", "Unique workflow", "Comprehensive suite"],
                "notable_limitations": ["Learning curve", "Electronic music focus"],
                "competitive_position": "Industry leader in electronic music production"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Ableton Live 11", "music production", "DAW", "electronic music"],
                "readability_score": "Medium",
                "word_count": "540"
            }
        }
    },
    {
        "product_input": {
            "sku": "LOGIC-PRO-X-MAC",
            "name": "Logic Pro X for Mac",
            "slug": "logic-pro-x-mac",
            "brand": "Apple",
            "category": "music-software",
            "description": "Logic Pro X is Apple's professional music production software featuring advanced recording, mixing, and mastering tools with extensive built-in instruments and effects.",
            "specifications": {
                "platform": "macOS 10.15+ only",
                "audio_formats": "WAV, AIFF, MP3, FLAC, Apple Lossless",
                "max_tracks": "Unlimited",
                "plugins": "Built-in instruments and effects",
                "included_content": "80+ GB of sounds and samples",
                "features": "Advanced mixing, Mastering tools, MIDI sequencing",
                "licensing": "App Store purchase",
                "updates": "Free updates"
            },
            "msrp_price": 199,
            "images": ["logic_pro_x_1.jpg", "logic_pro_x_2.jpg", "logic_pro_x_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "Logic Pro X provides comprehensive music production tools with Apple's signature integration and workflow.",
                "key_features": ["Advanced mixing", "Mastering tools", "80+ GB content", "Apple integration"],
                "target_skill_level": "Intermediate to Professional",
                "country_of_origin": "USA",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "software_characteristics": {
                    "workflow": "Traditional DAW workflow with modern enhancements",
                    "performance": "Optimized for macOS with excellent stability",
                    "best_applications": ["Music production", "Recording", "Mixing", "Mastering"],
                    "integration": "Seamless integration with Apple ecosystem"
                },
                "build_quality": {
                    "construction_type": "Professional Music Software",
                    "hardware_quality": "Software-based",
                    "finish_quality": "Polished Apple interface design",
                    "expected_durability": "Very High"
                },
                "playability": {
                    "learning_curve": "Moderate",
                    "workflow_efficiency": "Excellent for traditional recording",
                    "comfort_rating": "9/10 - Intuitive for traditional music production",
                    "performance": "Optimized performance on macOS"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Apple Integration", "description": "Seamless integration with macOS and Apple ecosystem."},
                    {"title": "Comprehensive Tools", "description": "Complete production environment from recording to mastering."}
                ],
                "why_not_buy": [
                    {"title": "Mac Only", "description": "Limited to macOS platform."}
                ],
                "best_for": [
                    {"user_type": "Mac users and traditional recording", "reason": "Excellent traditional DAW workflow with Apple integration."}
                ],
                "not_ideal_for": [
                    {"user_type": "Windows users", "reason": "Mac-only platform limitation."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Music production", "Recording", "Mixing", "Mastering"],
                "suitable_applications": {
                    "excellent": ["Traditional recording", "Music production"],
                    "good": ["Mixing", "Mastering"],
                    "limited": ["Live performance", "Cross-platform collaboration"]
                },
                "skill_development": {
                    "learning_curve": "Moderate",
                    "growth_potential": "Extensive capabilities that grow with user skills"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["macOS compatibility", "Plugin compatibility"],
                "care_instructions": {
                    "daily": "Save projects regularly",
                    "weekly": "Update software and plugins",
                    "monthly": "Backup projects and preferences",
                    "annual": "Check macOS compatibility"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Additional plugins", "Hardware controllers", "Sample libraries"],
                    "recommended_budget": "€200-1000"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "9", "sound_quality": "9", "value_for_money": "10", "versatility": "9"},
                "standout_features": ["Apple integration", "Comprehensive tools", "Excellent value"],
                "notable_limitations": ["Mac only", "Limited live performance"],
                "competitive_position": "Excellent value in professional DAW market"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Logic Pro X", "music production", "DAW", "Apple music software"],
                "readability_score": "Medium",
                "word_count": "520"
            }
        }
    },
    # Home Audio (2 products)
    {
        "product_input": {
            "sku": "KLIPSCH-RP-600M-BOOKSHELF",
            "name": "Klipsch RP-600M Bookshelf Speakers",
            "slug": "klipsch-rp-600m-bookshelf-speakers",
            "brand": "Klipsch",
            "category": "home-audio",
            "description": "The Klipsch RP-600M bookshelf speakers deliver dynamic, detailed sound with the legendary Klipsch horn-loaded tweeter and copper-spun woofer for exceptional home audio performance.",
            "specifications": {
                "type": "2-way bookshelf speaker",
                "tweeter": "1\" Titanium LTS vented tweeter with Hybrid Tractrix Horn",
                "woofer": "6.5\" Cerametallic cone woofer",
                "frequency_response": "45Hz - 25kHz",
                "sensitivity": "96 dB",
                "power_handling": "100W continuous, 400W peak",
                "impedance": "8 ohms",
                "crossover": "1500Hz",
                "dimensions": "15.75\" x 7.94\" x 11.88\"",
                "weight": "16.5 lbs each"
            },
            "msrp_price": 629,
            "images": ["klipsch_rp600m_1.jpg", "klipsch_rp600m_2.jpg", "klipsch_rp600m_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "RP-600M combines Klipsch's legendary horn technology with modern design for exceptional home audio performance.",
                "key_features": ["Horn-loaded tweeter", "Cerametallic woofer", "High sensitivity", "Dynamic sound"],
                "target_skill_level": "Intermediate to Advanced",
                "country_of_origin": "USA",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "sound_characteristics": {
                    "tonal_profile": "Dynamic, detailed sound with excellent clarity and impact",
                    "frequency_response": "Extended highs and solid bass for bookshelf speakers",
                    "best_applications": ["Home theater", "Music listening", "Stereo systems", "Small to medium rooms"],
                    "sensitivity": "High sensitivity for easy amplification"
                },
                "build_quality": {
                    "construction_type": "Professional Bookshelf Speaker",
                    "hardware_quality": "High",
                    "finish_quality": "Premium MDF construction with attractive finish",
                    "expected_durability": "Very High"
                },
                "playability": {
                    "setup_ease": "Standard speaker setup with good placement flexibility",
                    "amplification": "Easy to drive with high sensitivity",
                    "comfort_rating": "9/10 - Excellent sound quality and build",
                    "versatility": "Good for music and home theater"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Klipsch Heritage", "description": "Legendary horn technology with proven sound quality."},
                    {"title": "High Sensitivity", "description": "Easy to drive with most amplifiers."}
                ],
                "why_not_buy": [
                    {"title": "Bright Character", "description": "Forward sound may not suit all listening preferences."}
                ],
                "best_for": [
                    {"user_type": "Music enthusiasts and home theater", "reason": "Dynamic sound with excellent detail and impact."}
                ],
                "not_ideal_for": [
                    {"user_type": "Those preferring warm, laid-back sound", "reason": "Forward, dynamic character may be too bright."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Home theater", "Music listening", "Stereo systems", "Small to medium rooms"],
                "suitable_applications": {
                    "excellent": ["Rock", "Pop", "Home theater"],
                    "good": ["Jazz", "Classical"],
                    "limited": ["Very large rooms", "Background music"]
                },
                "skill_development": {
                    "learning_curve": "Low",
                    "growth_potential": "Excellent foundation for audio system building"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Dust accumulation", "Cable connections"],
                "care_instructions": {
                    "daily": "Wipe down if needed",
                    "weekly": "Check connections and clean grilles",
                    "monthly": "Clean drivers and check positioning",
                    "annual": "Professional inspection if needed"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Better speaker cables", "Speaker stands", "Subwoofer addition"],
                    "recommended_budget": "€200-800"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "9", "sound_quality": "9", "value_for_money": "9", "versatility": "8"},
                "standout_features": ["Horn technology", "High sensitivity", "Dynamic sound"],
                "notable_limitations": ["Bright character", "Limited bass extension"],
                "competitive_position": "Excellent value in bookshelf speaker market"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Klipsch RP-600M", "bookshelf speakers", "home audio", "Klipsch speakers"],
                "readability_score": "Medium",
                "word_count": "520"
            }
        }
    },
    {
        "product_input": {
            "sku": "DENON-AVR-X2700H-RECEIVER",
            "name": "Denon AVR-X2700H 7.2 Channel AV Receiver",
            "slug": "denon-avr-x2700h-receiver",
            "brand": "Denon",
            "category": "home-audio",
            "description": "The Denon AVR-X2700H is a feature-rich 7.2 channel AV receiver delivering 95W per channel with advanced audio processing, 4K video support, and comprehensive connectivity options.",
            "specifications": {
                "channels": "7.2 channel",
                "power_output": "95W per channel (8 ohms, 20Hz-20kHz, 0.08% THD)",
                "video_support": "4K/60Hz, HDR10, Dolby Vision, HLG",
                "audio_formats": "Dolby Atmos, DTS:X, DTS Neural:X",
                "connectivity": "6x HDMI inputs, 2x outputs, Bluetooth, WiFi",
                "streaming": "HEOS multi-room audio",
                "room_correction": "Audyssey MultEQ XT",
                "dimensions": "17.1\" x 6.6\" x 13.3\"",
                "weight": "22.5 lbs"
            },
            "msrp_price": 799,
            "images": ["denon_avr_x2700h_1.jpg", "denon_avr_x2700h_2.jpg", "denon_avr_x2700h_3.jpg"]
        },
        "ai_generated_content": {
            "basic_info": {
                "overview": "AVR-X2700H provides comprehensive home theater and audio capabilities with modern connectivity and processing.",
                "key_features": ["7.2 channels", "4K video support", "HEOS streaming", "Audyssey room correction"],
                "target_skill_level": "Intermediate to Advanced",
                "country_of_origin": "Japan",
                "release_year": "Current Production"
            },
            "technical_analysis": {
                "audio_characteristics": {
                    "power_output": "95W per channel with clean amplification",
                    "processing": "Advanced audio processing with room correction",
                    "best_applications": ["Home theater", "Multi-room audio", "Music streaming", "Gaming"],
                    "connectivity": "Comprehensive HDMI and wireless connectivity"
                },
                "build_quality": {
                    "construction_type": "Professional AV Receiver",
                    "hardware_quality": "High",
                    "finish_quality": "Durable construction with good ventilation",
                    "expected_durability": "Very High"
                },
                "playability": {
                    "setup_ease": "Comprehensive setup wizard with room correction",
                    "connectivity": "Extensive input/output options",
                    "comfort_rating": "8/10 - Feature-rich but complex setup",
                    "versatility": "Excellent for home theater and music"
                }
            },
            "purchase_decision": {
                "why_buy": [
                    {"title": "Comprehensive Features", "description": "Complete home theater solution with modern connectivity."},
                    {"title": "Room Correction", "description": "Audyssey MultEQ XT optimizes sound for your room."}
                ],
                "why_not_buy": [
                    {"title": "Complex Setup", "description": "Many features may be overwhelming for beginners."}
                ],
                "best_for": [
                    {"user_type": "Home theater enthusiasts", "reason": "Comprehensive features for modern home theater."}
                ],
                "not_ideal_for": [
                    {"user_type": "Simple stereo users", "reason": "Overkill for basic stereo needs."}
                ]
            },
            "usage_guidance": {
                "recommended_use": ["Home theater", "Multi-room audio", "Music streaming", "Gaming"],
                "suitable_applications": {
                    "excellent": ["Home theater", "Multi-room audio"],
                    "good": ["Music streaming", "Gaming"],
                    "limited": ["Simple stereo", "Basic audio needs"]
                },
                "skill_development": {
                    "learning_curve": "Moderate",
                    "growth_potential": "Extensive features that grow with user needs"
                }
            },
            "maintenance_care": {
                "maintenance_level": "Low",
                "common_issues": ["Firmware updates", "HDMI handshake issues"],
                "care_instructions": {
                    "daily": "Check operation and connections",
                    "weekly": "Update firmware if needed",
                    "monthly": "Clean ventilation and check settings",
                    "annual": "Professional inspection if needed"
                },
                "upgrade_potential": {
                    "easy_upgrades": ["Better speakers", "Subwoofer addition", "Streaming services"],
                    "recommended_budget": "€500-2000"
                }
            },
            "professional_assessment": {
                "expert_rating": {"build_quality": "9", "sound_quality": "8", "value_for_money": "9", "versatility": "9"},
                "standout_features": ["Comprehensive features", "Room correction", "Modern connectivity"],
                "notable_limitations": ["Complex setup", "Learning curve"],
                "competitive_position": "Excellent value in mid-range AV receiver market"
            },
            "content_metadata": {
                "generated_date": "2024-01-15T10:30:00Z",
                "content_version": "1.0",
                "seo_keywords": ["Denon AVR-X2700H", "AV receiver", "home theater", "7.2 channel"],
                "readability_score": "Medium",
                "word_count": "540"
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
        for item in MISSING_CATEGORY_PRODUCTS:
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
        print(f"Successfully created {created} new products for missing categories")


if __name__ == "__main__":
    asyncio.run(insert_products())
