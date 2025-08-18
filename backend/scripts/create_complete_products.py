#!/usr/bin/env python3
"""
Script to create complete product descriptions and insert them into the database.
Creates at least 2 products for each category with comprehensive descriptions.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from decimal import Decimal

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models import Product, Brand, Category
from sqlalchemy import select

# Database setup
DATABASE_URL = "postgresql+asyncpg://admin:qQqqDgXlIuBSZDUlgqzQEcoTPBkrCjVD@dpg-d2er32qdbo4c738oofng-a.frankfurt-postgres.render.com/musicgear_db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Complete product dataset following the comprehensive_products_with_ai_content.json structure
COMPLETE_PRODUCTS_DATA = {
    "comprehensive_product_dataset": [
        {
            "product_input": {
                "sku": "FENDER-PLAYER-STRAT-SSS",
                "name": "Fender Player Stratocaster MIM",
                "slug": "fender-player-stratocaster-mim",
                "brand": "Fender",
                "category": "electric-guitars",
                "description": "The Fender Player Stratocaster MIM delivers the iconic Strat sound and feel with modern refinements for today's players. This Mexican-made instrument offers exceptional value, combining traditional craftsmanship with contemporary upgrades like the pau ferro fingerboard and refined Player Series pickups.",
                "specifications": {
                    "body_material": "Alder",
                    "neck_material": "Maple",
                    "fingerboard": "Pau Ferro",
                    "pickups": "3x Player Series Alnico 5 Single-Coil",
                    "scale_length": "25.5 inches",
                    "frets": 22,
                    "bridge": "2-Point Synchronized Tremolo",
                    "tuners": "Standard Cast/Sealed",
                    "nut_width": "1.685 inches",
                    "finish": "Polyester"
                },
                "msrp_price": 749,
                "images": ["fender_player_strat_1.jpg", "fender_player_strat_2.jpg", "fender_player_strat_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Fender Player Stratocaster MIM delivers the iconic Strat sound and feel with modern refinements for today's players. This Mexican-made instrument offers exceptional value, combining traditional craftsmanship with contemporary upgrades like the pau ferro fingerboard and refined Player Series pickups.",
                    "key_features": ["Player Series Alnico 5 single-coil pickups", "2-point synchronized tremolo bridge", "Modern 'C' shaped neck profile", "22-fret pau ferro fingerboard"],
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Mexico",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Classic Stratocaster chime with balanced warmth, clear articulation, and singing sustain",
                        "output_level": "Medium",
                        "best_genres": ["Blues", "Rock", "Pop", "Country", "Funk"],
                        "pickup_positions": {
                            "position_1": "Bright, cutting bridge tone perfect for lead work and rhythm chunks",
                            "position_2": "Quacky, funky bridge/middle combination ideal for rhythm and clean tones",
                            "position_3": "Balanced middle pickup with smooth character for both clean and overdriven sounds",
                            "position_4": "Warm middle/neck combination excellent for blues and smooth leads",
                            "position_5": "Full, rich neck pickup tone perfect for jazz, blues, and warm lead tones"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Solid Body",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional polyester finish with good attention to detail",
                        "expected_durability": "High"
                    },
                    "playability": {
                        "neck_profile": "Modern 'C' shape offers comfortable grip for most hand sizes",
                        "action_setup": "Medium action potential with good setup from factory",
                        "comfort_rating": "8/10 - Excellent ergonomics with well-balanced weight distribution",
                        "weight_category": "Medium with approximately 3.2-3.6 kg"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Authentic Fender Quality at Mid-Tier Price",
                            "description": "Genuine Fender craftsmanship from the Corona factory with quality control standards that ensure consistent playability and tone."
                        },
                        {
                            "title": "Exceptional Versatility Across Genres",
                            "description": "The five-way pickup selector and balanced pickup outputs make this guitar suitable for everything from clean jazz to high-gain rock."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited High-Output Capability",
                            "description": "Single-coil pickups may not provide enough output for metal or very high-gain applications without additional pedals."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Intermediate players seeking authentic Fender tone",
                            "reason": "Provides genuine Stratocaster experience with quality construction at an accessible price point"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Metal and hard rock specialists",
                            "reason": "Single-coil pickups and traditional output levels may not provide the high-gain characteristics preferred in heavy music styles"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Tube combo amps 15-30W", "Modeling amplifiers", "Clean platform amps with pedals"],
                    "suitable_music_styles": {
                        "excellent": ["Blues", "Classic Rock", "Country", "Funk", "Pop"],
                        "good": ["Jazz", "Alternative Rock", "Indie", "R&B"],
                        "limited": ["Metal", "Hardcore", "Progressive Rock with high-gain requirements"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate",
                        "growth_potential": "This instrument will serve players from intermediate through advanced levels, offering room for technical growth and tonal exploration for many years"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Tremolo bridge tuning stability", "Single-coil pickup noise", "Neck adjustment due to climate changes"],
                    "care_instructions": {
                        "daily": "Wipe down strings and body after playing, store in case or on stand away from temperature extremes",
                        "weekly": "Clean fingerboard lightly, check tuning stability, inspect hardware for looseness",
                        "monthly": "Deep clean body and hardware, condition fingerboard if needed, check intonation",
                        "annual": "Professional setup including fret inspection, electronics check, and complete adjustment"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Pickup replacement", "Bridge upgrade", "Tuner improvement", "Nut replacement"],
                        "recommended_budget": "€150-300 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8", 
                        "value_for_money": "9",
                        "versatility": "9"
                    },
                    "standout_features": ["Authentic Fender tone and feel", "Excellent versatility across genres"],
                    "notable_limitations": ["Single-coil noise susceptibility", "Limited high-gain output"],
                    "competitive_position": "Strong value leader in the €700-800 range, offering genuine Fender quality that competitors struggle to match at this price point"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Fender Player Stratocaster", "Mexican Stratocaster", "intermediate electric guitar", "versatile electric guitar", "Strat tone"],
                    "readability_score": "Medium",
                    "word_count": "750"
                }
            }
        },
        {
            "product_input": {
                "sku": "GIBSON-LP-STUDIO-EB",
                "name": "Gibson Les Paul Studio Ebony",
                "slug": "gibson-les-paul-studio-ebony",
                "brand": "Gibson",
                "category": "electric-guitars",
                "description": "The Gibson Les Paul Studio brings classic Les Paul tone and feel with modern appointments at an accessible price point.",
                "specifications": {
                    "body_material": "Mahogany with Maple Cap",
                    "neck_material": "Mahogany",
                    "fingerboard": "Rosewood",
                    "pickups": "2x 490R/498T Humbucking",
                    "scale_length": "24.75 inches",
                    "frets": 22,
                    "bridge": "Tune-o-matic with Stopbar Tailpiece",
                    "tuners": "Grover Rotomatic",
                    "nut_width": "1.695 inches",
                    "finish": "Nitrocellulose"
                },
                "msrp_price": 1299,
                "images": ["gibson_lp_studio_1.jpg", "gibson_lp_studio_2.jpg", "gibson_lp_studio_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Gibson Les Paul Studio delivers authentic American-made Les Paul tone with classic mahogany/maple construction and powerful humbucking pickups. This model strips away cosmetic extras to focus on pure sonic performance and playability.",
                    "key_features": ["490R/498T humbucking pickups", "Mahogany body with maple cap", "Nitrocellulose lacquer finish", "Grover Rotomatic tuners"],
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "United States",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Rich, warm, and sustaining with the classic Les Paul midrange focus and powerful low-end response",
                        "output_level": "High",
                        "best_genres": ["Rock", "Blues", "Hard Rock", "Metal", "Jazz"],
                        "pickup_positions": {
                            "bridge": "High-output 498T delivers aggressive, cutting tone perfect for lead work and heavy rhythm",
                            "neck": "Warm 490R provides smooth, singing lead tones and rich rhythm sounds",
                            "both": "Combined pickup position offers balanced tone with enhanced midrange presence"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Solid Body",
                        "hardware_quality": "Premium",
                        "finish_quality": "Traditional nitrocellulose lacquer allows wood resonance while providing vintage aesthetic appeal",
                        "expected_durability": "High"
                    },
                    "playability": {
                        "neck_profile": "Traditional rounded profile provides substantial feel preferred by many players for chord work and bending",
                        "action_setup": "Medium action setup with excellent sustain and note clarity",
                        "comfort_rating": "7/10 - Substantial weight and neck profile may require adjustment period for some players",
                        "weight_category": "Heavy with approximately 4.1-4.5 kg"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Authentic Gibson USA Construction",
                            "description": "Made in Nashville with traditional construction methods and premium materials that deliver the classic Les Paul experience."
                        },
                        {
                            "title": "Powerful High-Output Pickups",
                            "description": "490R/498T pickup combination provides excellent output for both clean and overdriven tones, particularly excelling in rock and blues applications."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Substantial Weight and Size",
                            "description": "The Les Paul's traditional weight and neck profile may be uncomfortable for players accustomed to lighter, slimmer instruments."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Rock and blues players seeking classic Les Paul tone",
                            "reason": "Delivers the iconic Les Paul sound and feel that has defined rock music for generations"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Players requiring lightweight instruments",
                            "reason": "The substantial weight and traditional neck profile may not suit players who prefer lighter, more modern instruments"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Tube amplifiers 20-50W", "High-gain amplifiers", "Clean amplifiers with pedals"],
                    "suitable_music_styles": {
                        "excellent": ["Rock", "Blues", "Hard Rock", "Metal", "Jazz"],
                        "good": ["Country", "Alternative Rock", "Progressive Rock"],
                        "limited": ["Funk", "Pop", "Light acoustic-style playing"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate to High",
                        "growth_potential": "This instrument will challenge and reward players as they develop their technique and understanding of Les Paul characteristics"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Neck relief adjustment", "Bridge height adjustment", "Nut slot maintenance"],
                    "care_instructions": {
                        "daily": "Wipe down strings and body after playing, store in case or on stand",
                        "weekly": "Clean fingerboard, check tuning stability, inspect hardware",
                        "monthly": "Deep clean body and hardware, condition fingerboard, check intonation",
                        "annual": "Professional setup including fret inspection and electronics check"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Pickup replacement", "Bridge upgrade", "Tuner improvement"],
                        "recommended_budget": "€200-500 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "9",
                        "sound_quality": "9", 
                        "value_for_money": "8",
                        "versatility": "8"
                    },
                    "standout_features": ["Authentic Gibson USA construction", "Classic Les Paul tone and sustain"],
                    "notable_limitations": ["Substantial weight", "Traditional neck profile may not suit all players"],
                    "competitive_position": "Premium offering in the €1200-1400 range, delivering authentic Gibson quality and tone that justifies the investment for serious players"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Gibson Les Paul Studio", "Les Paul electric guitar", "humbucker pickups", "rock guitar", "Gibson USA"],
                    "readability_score": "Medium",
                    "word_count": "800"
                }
            }
        },
        {
            "product_input": {
                "sku": "TAYLOR-214CE-DLX",
                "name": "Taylor 214ce Deluxe Grand Auditorium",
                "slug": "taylor-214ce-deluxe-grand-auditorium",
                "brand": "Taylor",
                "category": "acoustic-guitars",
                "description": "The Taylor 214ce Deluxe Grand Auditorium combines Taylor's renowned craftsmanship with exceptional value, delivering a premium acoustic-electric experience.",
                "specifications": {
                    "body_material": "Layered Rosewood Back/Sides, Solid Sitka Spruce Top",
                    "neck_material": "Sapele",
                    "fingerboard": "West African Crelicam Ebony",
                    "scale_length": "25.5 inches",
                    "frets": 20,
                    "bridge": "West African Crelicam Ebony",
                    "tuners": "Taylor Nickel Tuners",
                    "electronics": "Expression System 2",
                    "body_shape": "Grand Auditorium",
                    "finish": "Gloss Top, Satin Back/Sides"
                },
                "msrp_price": 999,
                "images": ["taylor_214ce_1.jpg", "taylor_214ce_2.jpg", "taylor_214ce_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Taylor 214ce Deluxe Grand Auditorium represents exceptional value in Taylor's lineup, offering the brand's signature playability and tone at an accessible price point. The layered rosewood construction provides rich, complex tones while maintaining affordability.",
                    "key_features": ["Expression System 2 electronics", "Grand Auditorium body shape", "Layered rosewood back and sides", "Solid Sitka spruce top"],
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Mexico",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Balanced and articulate with clear highs, warm mids, and defined bass response",
                        "output_level": "Medium",
                        "best_genres": ["Folk", "Country", "Pop", "Singer-Songwriter", "Jazz"],
                        "playing_styles": {
                            "fingerpicking": "Excellent clarity and separation between strings",
                            "strumming": "Rich, full-bodied sound with good projection",
                            "flatpicking": "Clear, cutting tone with excellent note definition"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Acoustic-Electric",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional gloss top with satin back and sides",
                        "expected_durability": "High"
                    },
                    "playability": {
                        "neck_profile": "Taylor's comfortable neck profile with smooth playability",
                        "action_setup": "Low action potential with excellent setup from factory",
                        "comfort_rating": "9/10 - Excellent ergonomics and comfortable playing feel",
                        "weight_category": "Light to Medium"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Taylor Quality at Accessible Price",
                            "description": "Delivers Taylor's renowned playability and tone quality at a price point accessible to intermediate players."
                        },
                        {
                            "title": "Versatile Grand Auditorium Design",
                            "description": "The Grand Auditorium body shape offers excellent balance between fingerpicking and strumming styles."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Layered Wood Construction",
                            "description": "Layered rosewood may not provide the same tonal complexity as solid wood construction found in higher-end models."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Intermediate acoustic players seeking Taylor quality",
                            "reason": "Provides Taylor's signature playability and tone at an accessible price point"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Players requiring premium solid wood construction",
                            "reason": "Layered wood construction may not satisfy players seeking the ultimate in acoustic guitar tone"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Acoustic amplifiers", "PA systems", "Direct recording"],
                    "suitable_music_styles": {
                        "excellent": ["Folk", "Country", "Pop", "Singer-Songwriter"],
                        "good": ["Jazz", "Blues", "Classical"],
                        "limited": ["Heavy strumming", "High-volume performance"]
                    },
                    "skill_development": {
                        "learning_curve": "Low to Moderate",
                        "growth_potential": "This instrument will serve players well as they develop their acoustic playing skills and technique"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Humidity control", "String changes", "Electronics maintenance"],
                    "care_instructions": {
                        "daily": "Wipe down after playing, store in case with humidifier",
                        "weekly": "Clean body and strings, check humidity levels",
                        "monthly": "Deep clean, condition fingerboard if needed",
                        "annual": "Professional setup and electronics check"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["String upgrades", "Pickup system", "Tuner improvement"],
                        "recommended_budget": "€100-300 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8", 
                        "value_for_money": "9",
                        "versatility": "9"
                    },
                    "standout_features": ["Taylor playability", "Versatile Grand Auditorium design", "Quality electronics"],
                    "notable_limitations": ["Layered wood construction", "Limited high-volume performance"],
                    "competitive_position": "Strong value offering in the €900-1100 range, providing Taylor quality and playability that exceeds expectations at this price point"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Taylor 214ce", "acoustic-electric guitar", "Grand Auditorium", "Taylor guitar", "intermediate acoustic"],
                    "readability_score": "Medium",
                    "word_count": "700"
                }
            }
        },
        {
            "product_input": {
                "sku": "MARTIN-D-18",
                "name": "Martin D-18 Standard",
                "slug": "martin-d-18-standard",
                "brand": "Martin",
                "category": "acoustic-guitars",
                "description": "The Martin D-18 Standard represents the quintessential dreadnought acoustic guitar, delivering the classic Martin sound that has defined American folk, bluegrass, and country music for generations.",
                "specifications": {
                    "body_material": "Solid Mahogany Back/Sides, Solid Sitka Spruce Top",
                    "neck_material": "Select Hardwood",
                    "fingerboard": "East Indian Rosewood",
                    "scale_length": "25.4 inches",
                    "frets": 20,
                    "bridge": "East Indian Rosewood",
                    "tuners": "Chrome Open-Geared",
                    "bracing": "Forward-Shifted Scalloped X-Bracing",
                    "body_shape": "Dreadnought",
                    "finish": "Gloss"
                },
                "msrp_price": 2499,
                "images": ["martin_d18_1.jpg", "martin_d18_2.jpg", "martin_d18_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Martin D-18 Standard is the benchmark dreadnought acoustic guitar, delivering the iconic Martin sound that has shaped American music for over a century. Solid mahogany construction provides warm, balanced tones with excellent projection.",
                    "key_features": ["Solid mahogany back and sides", "Solid Sitka spruce top", "Forward-shifted scalloped X-bracing", "Traditional dreadnought body shape"],
                    "target_skill_level": "Advanced",
                    "country_of_origin": "United States",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Warm, balanced, and powerful with excellent bass response and clear, articulate highs",
                        "output_level": "High",
                        "best_genres": ["Bluegrass", "Folk", "Country", "Americana", "Singer-Songwriter"],
                        "playing_styles": {
                            "flatpicking": "Exceptional clarity and power for bluegrass and country styles",
                            "strumming": "Rich, full-bodied sound with excellent projection",
                            "fingerpicking": "Clear note separation with warm, resonant tone"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Acoustic",
                        "hardware_quality": "Premium",
                        "finish_quality": "Traditional gloss finish with excellent attention to detail",
                        "expected_durability": "Very High"
                    },
                    "playability": {
                        "neck_profile": "Traditional Martin neck profile with comfortable playing feel",
                        "action_setup": "Medium action with excellent setup from factory",
                        "comfort_rating": "8/10 - Substantial size may require adjustment for some players",
                        "weight_category": "Medium to Heavy"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Iconic Martin Sound and Heritage",
                            "description": "Delivers the legendary Martin tone that has defined acoustic guitar music for generations."
                        },
                        {
                            "title": "Premium Solid Wood Construction",
                            "description": "Solid mahogany back and sides with solid spruce top provide exceptional tone and resonance."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Substantial Investment",
                            "description": "Premium price point may be beyond the budget of many intermediate players."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Serious acoustic players and professionals",
                            "reason": "Delivers the ultimate in acoustic guitar tone and craftsmanship"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Beginners or casual players",
                            "reason": "Premium price and traditional design may not suit players seeking modern features or lower cost"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["High-quality acoustic amplifiers", "PA systems", "Direct recording"],
                    "suitable_music_styles": {
                        "excellent": ["Bluegrass", "Folk", "Country", "Americana"],
                        "good": ["Singer-Songwriter", "Jazz", "Blues"],
                        "limited": ["Heavy rock strumming", "High-gain applications"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate to High",
                        "growth_potential": "This instrument will challenge and reward players as they develop their acoustic technique and understanding"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "High",
                    "common_issues": ["Humidity control", "Neck relief adjustment", "Bridge maintenance"],
                    "care_instructions": {
                        "daily": "Wipe down after playing, store in case with humidifier",
                        "weekly": "Clean body and strings, check humidity levels",
                        "monthly": "Deep clean, condition fingerboard, check setup",
                        "annual": "Professional setup and inspection"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["String upgrades", "Tuner improvement", "Pickup system"],
                        "recommended_budget": "€200-500 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "10",
                        "sound_quality": "10", 
                        "value_for_money": "9",
                        "versatility": "8"
                    },
                    "standout_features": ["Iconic Martin tone", "Premium solid wood construction", "Exceptional craftsmanship"],
                    "notable_limitations": ["Premium price point", "Traditional design may not suit all players"],
                    "competitive_position": "Premium offering in the €2400-2600 range, representing the gold standard for acoustic guitar tone and craftsmanship"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Martin D-18", "dreadnought acoustic guitar", "Martin guitar", "solid mahogany guitar", "bluegrass guitar"],
                    "readability_score": "Medium",
                    "word_count": "750"
                }
            }
        },
        {
            "product_input": {
                "sku": "ROLAND-FP30X-BK",
                "name": "Roland FP-30X Digital Piano",
                "slug": "roland-fp-30x-digital-piano",
                "brand": "Roland",
                "category": "digital-keyboards",
                "description": "The Roland FP-30X digital piano combines authentic piano feel with modern digital convenience in a portable package.",
                "specifications": {
                    "keys": 88,
                    "key_action": "PHA-4 Standard with Escapement and Ivory Feel",
                    "sound_engine": "SuperNATURAL Piano",
                    "polyphony": 256,
                    "voices": 56,
                    "built_in_songs": 30,
                    "connectivity": "USB, Bluetooth, Headphone x2, Sustain Pedal",
                    "speakers": "2 x 11W",
                    "dimensions": "1300 x 284 x 151 mm",
                    "weight": "16.7 kg"
                },
                "msrp_price": 699,
                "images": ["roland_fp30x_1.jpg", "roland_fp30x_2.jpg", "roland_fp30x_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Roland FP-30X delivers an authentic piano playing experience with modern digital features in a compact, portable design. The PHA-4 keyboard action provides realistic touch response that closely mimics an acoustic piano.",
                    "key_features": ["PHA-4 Standard keyboard with escapement", "SuperNATURAL Piano sound engine", "256-note polyphony", "Bluetooth connectivity"],
                    "target_skill_level": "Beginner to Intermediate",
                    "country_of_origin": "Indonesia",
                    "release_year": "2021"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Rich, expressive piano tones with excellent dynamic range and natural decay",
                        "output_level": "High",
                        "best_genres": ["Classical", "Jazz", "Pop", "Contemporary", "Practice"],
                        "keyboard_response": {
                            "touch_sensitivity": "Excellent dynamic response across all velocity levels",
                            "key_weight": "Realistic weighted action with escapement simulation",
                            "key_material": "Ivory feel white keys with ebony feel black keys"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Digital Piano",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional matte black finish with durable construction",
                        "expected_durability": "High"
                    },
                    "playability": {
                        "keyboard_action": "PHA-4 Standard provides authentic piano feel with escapement",
                        "action_setup": "Excellent from factory with consistent key response",
                        "comfort_rating": "9/10 - Natural piano feel with comfortable playing experience",
                        "weight_category": "Medium - portable but substantial"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Authentic Piano Feel at Accessible Price",
                            "description": "PHA-4 keyboard action delivers realistic piano touch response that helps develop proper technique."
                        },
                        {
                            "title": "Versatile Digital Features",
                            "description": "56 voices, Bluetooth connectivity, and recording capabilities provide modern digital convenience."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Advanced Features",
                            "description": "May not satisfy advanced players requiring extensive sound editing or advanced MIDI capabilities."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Piano students and home players",
                            "reason": "Provides authentic piano experience with modern digital features at an accessible price"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Advanced performers requiring extensive sound design",
                            "reason": "Limited advanced features compared to professional stage pianos"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Built-in speakers", "Studio monitors", "PA systems"],
                    "suitable_music_styles": {
                        "excellent": ["Classical", "Jazz", "Pop", "Contemporary"],
                        "good": ["Rock", "Electronic", "Practice"],
                        "limited": ["Heavy electronic music", "Advanced sound design"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for developing proper piano technique and musical skills"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Low",
                    "common_issues": ["Dust accumulation", "Key cleaning", "Software updates"],
                    "care_instructions": {
                        "daily": "Wipe keys with soft cloth after playing",
                        "weekly": "Clean keyboard surface, check connections",
                        "monthly": "Deep clean, update firmware if needed",
                        "annual": "Professional inspection and cleaning"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Pedal upgrade", "Speaker system", "Stand improvement"],
                        "recommended_budget": "€100-300 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8", 
                        "value_for_money": "9",
                        "versatility": "8"
                    },
                    "standout_features": ["Authentic piano feel", "Excellent value", "Portable design"],
                    "notable_limitations": ["Limited advanced features", "Built-in speaker quality"],
                    "competitive_position": "Strong value leader in the €600-800 range, offering authentic piano experience that exceeds expectations at this price point"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Roland FP-30X", "digital piano", "weighted keys", "piano practice", "portable piano"],
                    "readability_score": "Medium",
                    "word_count": "650"
                }
            }
        },
        {
            "product_input": {
                "sku": "YAMAHA-P125A-BK",
                "name": "Yamaha P-125a Digital Piano",
                "slug": "yamaha-p-125a-digital-piano",
                "brand": "Yamaha",
                "category": "digital-keyboards",
                "description": "The Yamaha P-125a digital piano delivers the authentic feel and sound of a grand piano in a compact, portable design.",
                "specifications": {
                    "keys": 88,
                    "key_action": "GHS (Graded Hammer Standard)",
                    "sound_engine": "AWM Stereo Sampling",
                    "polyphony": 192,
                    "voices": 24,
                    "built_in_songs": 21,
                    "connectivity": "USB, Sustain Pedal, Headphones",
                    "speakers": "2 x 7W",
                    "dimensions": "1326 x 295 x 166 mm",
                    "weight": "11.8 kg"
                },
                "msrp_price": 649,
                "images": ["yamaha_p125a_1.jpg", "yamaha_p125a_2.jpg", "yamaha_p125a_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Yamaha P-125a combines Yamaha's renowned piano craftsmanship with modern digital technology, delivering authentic grand piano sound and feel in a portable package.",
                    "key_features": ["GHS weighted keyboard action", "AWM Stereo Sampling", "CFIIIS grand piano samples", "USB connectivity"],
                    "target_skill_level": "Beginner to Intermediate",
                    "country_of_origin": "Indonesia",
                    "release_year": "2021"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Rich, dynamic grand piano tones with excellent clarity and natural resonance",
                        "output_level": "High",
                        "best_genres": ["Classical", "Jazz", "Pop", "Contemporary", "Practice"],
                        "keyboard_response": {
                            "touch_sensitivity": "Excellent dynamic range with natural piano response",
                            "key_weight": "Graded hammer action with heavier bass keys",
                            "key_material": "Matte finish white keys with smooth black keys"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Digital Piano",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional matte black finish with durable construction",
                        "expected_durability": "High"
                    },
                    "playability": {
                        "keyboard_action": "GHS provides authentic piano feel with graded weight",
                        "action_setup": "Excellent from factory with consistent response",
                        "comfort_rating": "9/10 - Natural piano feel with comfortable playing experience",
                        "weight_category": "Light to Medium - highly portable"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Yamaha Quality and Heritage",
                            "description": "Delivers Yamaha's legendary piano sound and craftsmanship at an accessible price point."
                        },
                        {
                            "title": "Portable and Versatile",
                            "description": "Lightweight design with excellent sound quality makes it perfect for home practice and portable use."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Advanced Features",
                            "description": "Basic feature set may not satisfy advanced players requiring extensive sound design capabilities."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Piano students and home players",
                            "reason": "Provides authentic Yamaha piano experience with modern digital convenience"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Advanced performers requiring extensive features",
                            "reason": "Limited advanced features compared to professional stage pianos"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Built-in speakers", "Studio monitors", "PA systems"],
                    "suitable_music_styles": {
                        "excellent": ["Classical", "Jazz", "Pop", "Contemporary"],
                        "good": ["Rock", "Electronic", "Practice"],
                        "limited": ["Heavy electronic music", "Advanced sound design"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for developing proper piano technique and musical skills"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Low",
                    "common_issues": ["Dust accumulation", "Key cleaning", "Software updates"],
                    "care_instructions": {
                        "daily": "Wipe keys with soft cloth after playing",
                        "weekly": "Clean keyboard surface, check connections",
                        "monthly": "Deep clean, update firmware if needed",
                        "annual": "Professional inspection and cleaning"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Pedal upgrade", "Speaker system", "Stand improvement"],
                        "recommended_budget": "€100-250 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8", 
                        "value_for_money": "9",
                        "versatility": "7"
                    },
                    "standout_features": ["Yamaha piano quality", "Portable design", "Excellent value"],
                    "notable_limitations": ["Limited voices", "Basic feature set"],
                    "competitive_position": "Strong value offering in the €600-700 range, delivering Yamaha quality and portability at an accessible price"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Yamaha P-125a", "digital piano", "weighted keys", "piano practice", "portable piano"],
                    "readability_score": "Medium",
                    "word_count": "600"
                }
            }
        },
        {
            "product_input": {
                "sku": "FENDER-MUSTANG-LT25",
                "name": "Fender Mustang LT25",
                "slug": "fender-mustang-lt25",
                "brand": "Fender",
                "category": "amplifiers",
                "description": "The Fender Mustang LT25 is a versatile 25-watt modeling amplifier that brings professional-quality tones to home practice and small venues.",
                "specifications": {
                    "power": "25 watts",
                    "speaker": "8-inch Fender Special Design",
                    "amp_models": 30,
                    "effects": 40,
                    "presets": 50,
                    "connectivity": "USB, Headphone, Aux In",
                    "controls": "Single knob with LCD display",
                    "dimensions": "347 x 358 x 183 mm",
                    "weight": "5.9 kg"
                },
                "msrp_price": 199,
                "images": ["fender_mustang_lt25_1.jpg", "fender_mustang_lt25_2.jpg", "fender_mustang_lt25_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Fender Mustang LT25 delivers professional-quality amp modeling and effects in a compact, affordable package. Perfect for home practice and small gigs with versatile tone options.",
                    "key_features": ["30 amp models", "40 built-in effects", "USB connectivity", "Headphone output"],
                    "target_skill_level": "Beginner to Intermediate",
                    "country_of_origin": "China",
                    "release_year": "2020"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Versatile range from clean Fender tones to high-gain modern sounds",
                        "output_level": "Medium",
                        "best_genres": ["Rock", "Blues", "Pop", "Country", "Practice"],
                        "amp_models": {
                            "clean_models": "Classic Fender clean tones with excellent clarity",
                            "overdrive_models": "Warm overdrive and crunch tones",
                            "high_gain_models": "Modern high-gain sounds for rock and metal"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Solid State Modeling",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional black finish with Fender styling",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "control_interface": "Simple single-knob interface with LCD display",
                        "ease_of_use": "Very intuitive for beginners",
                        "comfort_rating": "9/10 - Easy to use with excellent feature accessibility",
                        "weight_category": "Light - highly portable"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Exceptional Value for Features",
                            "description": "Offers professional-quality amp modeling and effects at an accessible price point."
                        },
                        {
                            "title": "Perfect for Learning and Practice",
                            "description": "Simple interface makes it easy for beginners to explore different tones and effects."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Volume for Larger Venues",
                            "description": "25-watt output may not be sufficient for larger performance spaces."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Beginners and home players",
                            "reason": "Provides excellent value and features for learning and practice"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Professional performers in large venues",
                            "reason": "Limited power output and basic feature set compared to professional amplifiers"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_guitars": ["Electric guitars", "Acoustic-electric guitars"],
                    "suitable_music_styles": {
                        "excellent": ["Rock", "Blues", "Pop", "Country"],
                        "good": ["Jazz", "Alternative", "Practice"],
                        "limited": ["Heavy metal", "Large venue performance"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for learning different amp tones and effects"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Low",
                    "common_issues": ["Software updates", "Connection cleaning", "Speaker care"],
                    "care_instructions": {
                        "daily": "Wipe down after use, check connections",
                        "weekly": "Clean controls and connections",
                        "monthly": "Update firmware if available",
                        "annual": "Professional inspection if needed"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Pedal additions", "Speaker upgrade", "Footswitch"],
                        "recommended_budget": "€50-150 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7", 
                        "value_for_money": "9",
                        "versatility": "8"
                    },
                    "standout_features": ["Excellent value", "Versatile amp models", "Easy to use"],
                    "notable_limitations": ["Limited power", "Basic speaker quality"],
                    "competitive_position": "Outstanding value leader in the €150-250 range, offering features that typically cost much more"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Fender Mustang LT25", "modeling amplifier", "practice amp", "guitar amplifier", "effects amp"],
                    "readability_score": "Medium",
                    "word_count": "550"
                }
            }
        },
        {
            "product_input": {
                "sku": "MARSHALL-DSL20CR",
                "name": "Marshall DSL20CR Combo",
                "slug": "marshall-dsl20cr-combo",
                "brand": "Marshall",
                "category": "amplifiers",
                "description": "The Marshall DSL20CR is a 20-watt all-tube combo amplifier that delivers classic Marshall tone with modern features and versatility.",
                "specifications": {
                    "power": "20 watts",
                    "tubes": "2 x ECC83, 2 x EL34",
                    "speaker": "12-inch Celestion Seventy 80",
                    "channels": 2,
                    "effects_loop": "Yes",
                    "connectivity": "Speaker out, Effects loop, DI out",
                    "controls": "Gain, Volume, Bass, Middle, Treble per channel",
                    "dimensions": "510 x 440 x 240 mm",
                    "weight": "19.5 kg"
                },
                "msrp_price": 699,
                "images": ["marshall_dsl20cr_1.jpg", "marshall_dsl20cr_2.jpg", "marshall_dsl20cr_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Marshall DSL20CR delivers authentic Marshall tube tone in a compact combo format. Perfect for players seeking classic Marshall sound with modern features and manageable volume levels.",
                    "key_features": ["All-tube design", "Two-channel operation", "Effects loop", "Celestion speaker"],
                    "target_skill_level": "Intermediate to Advanced",
                    "country_of_origin": "United Kingdom",
                    "release_year": "2018"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Classic Marshall crunch and overdrive with rich harmonics and excellent dynamics",
                        "output_level": "High",
                        "best_genres": ["Rock", "Blues", "Hard Rock", "Metal"],
                        "channel_characteristics": {
                            "clean_channel": "Warm, clear clean tones with excellent headroom",
                            "overdrive_channel": "Classic Marshall crunch to high-gain overdrive"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Tube Amplifier",
                        "hardware_quality": "Premium",
                        "finish_quality": "Professional Marshall styling with durable construction",
                        "expected_durability": "High"
                    },
                    "playability": {
                        "control_interface": "Traditional Marshall control layout with intuitive operation",
                        "ease_of_use": "Straightforward for experienced players",
                        "comfort_rating": "8/10 - Excellent tone control with traditional Marshall feel",
                        "weight_category": "Heavy - substantial tube amp weight"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Authentic Marshall Tube Tone",
                            "description": "Delivers the legendary Marshall sound that has defined rock music for decades."
                        },
                        {
                            "title": "Versatile Two-Channel Design",
                            "description": "Clean and overdrive channels provide excellent tonal flexibility for various playing styles."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Substantial Weight and Size",
                            "description": "All-tube construction makes this a heavy amplifier that may not suit portable needs."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Rock and blues players seeking authentic Marshall tone",
                            "reason": "Delivers classic Marshall sound with modern features and manageable volume"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Players requiring lightweight, portable amplifiers",
                            "reason": "Substantial weight and tube maintenance requirements may not suit all players"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_guitars": ["Electric guitars", "Humbucker-equipped guitars"],
                    "suitable_music_styles": {
                        "excellent": ["Rock", "Blues", "Hard Rock", "Metal"],
                        "good": ["Country", "Alternative Rock"],
                        "limited": ["Jazz", "Clean acoustic-style playing"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate",
                        "growth_potential": "Excellent for developing understanding of tube amp characteristics and tone shaping"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Tube replacement", "Bias adjustment", "Speaker care"],
                    "care_instructions": {
                        "daily": "Allow proper warm-up and cool-down periods",
                        "weekly": "Check tube condition, clean connections",
                        "monthly": "Inspect tubes and connections",
                        "annual": "Professional tube replacement and bias adjustment"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Tube upgrades", "Speaker replacement", "Effects pedals"],
                        "recommended_budget": "€200-500 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "9",
                        "sound_quality": "9", 
                        "value_for_money": "8",
                        "versatility": "8"
                    },
                    "standout_features": ["Authentic Marshall tone", "All-tube design", "Excellent build quality"],
                    "notable_limitations": ["Substantial weight", "Tube maintenance requirements"],
                    "competitive_position": "Premium offering in the €650-750 range, delivering authentic Marshall tube tone that justifies the investment"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Marshall DSL20CR", "tube amplifier", "Marshall amp", "rock amplifier", "combo amp"],
                    "readability_score": "Medium",
                    "word_count": "600"
                }
            }
        },
        {
            "product_input": {
                "sku": "FENDER-PLAYER-P-BASS",
                "name": "Fender Player Precision Bass",
                "slug": "fender-player-precision-bass",
                "brand": "Fender",
                "category": "bass-guitars",
                "description": "The Fender Player Precision Bass delivers the classic P-Bass sound and feel with modern playability improvements.",
                "specifications": {
                    "body_material": "Alder",
                    "neck_material": "Maple",
                    "fingerboard": "Pau Ferro",
                    "pickups": "Player Series Split Single-Coil Precision Bass",
                    "scale_length": "34 inches",
                    "frets": 20,
                    "bridge": "4-Saddle Standard",
                    "tuners": "Standard Open-Gear",
                    "nut_width": "1.625 inches",
                    "strings": 4
                },
                "msrp_price": 799,
                "images": ["fender_player_pbass_1.jpg", "fender_player_pbass_2.jpg", "fender_player_pbass_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Fender Player Precision Bass delivers the iconic P-Bass sound that has been the foundation of countless recordings across all genres. Modern playability improvements make it accessible to today's bassists.",
                    "key_features": ["Player Series split-coil pickup", "Modern 'C' shaped neck", "4-saddle bridge", "Pau ferro fingerboard"],
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Mexico",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Deep, punchy, and warm with excellent low-end definition and midrange presence",
                        "output_level": "Medium",
                        "best_genres": ["Rock", "Funk", "Jazz", "Country", "Pop"],
                        "pickup_characteristics": {
                            "split_coil": "Classic P-Bass tone with excellent noise rejection",
                            "tone_control": "Simple but effective tone shaping",
                            "volume_control": "Smooth volume response"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Solid Body",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional polyester finish with good attention to detail",
                        "expected_durability": "High"
                    },
                    "playability": {
                        "neck_profile": "Modern 'C' shape offers comfortable grip for most hand sizes",
                        "action_setup": "Medium action potential with good setup from factory",
                        "comfort_rating": "8/10 - Excellent ergonomics with well-balanced weight distribution",
                        "weight_category": "Medium with approximately 3.8-4.2 kg"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Iconic P-Bass Sound",
                            "description": "Delivers the legendary Precision Bass tone that has defined bass playing for generations."
                        },
                        {
                            "title": "Excellent Value and Quality",
                            "description": "Genuine Fender craftsmanship at an accessible price point with modern improvements."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Tonal Variety",
                            "description": "Single pickup design may not provide the tonal flexibility some players require."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Bassists seeking classic P-Bass tone",
                            "reason": "Provides the iconic Precision Bass sound and feel that has shaped music history"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Players requiring extensive tonal variety",
                            "reason": "Single pickup design limits tonal options compared to multi-pickup basses"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Bass amplifiers 100-300W", "PA systems", "Studio recording"],
                    "suitable_music_styles": {
                        "excellent": ["Rock", "Funk", "Jazz", "Country", "Pop"],
                        "good": ["Blues", "R&B", "Alternative"],
                        "limited": ["Heavy metal", "Progressive rock requiring extensive tonal variety"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate",
                        "growth_potential": "Excellent for developing fundamental bass technique and understanding of classic bass tone"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["String changes", "Neck adjustment", "Bridge setup"],
                    "care_instructions": {
                        "daily": "Wipe down strings and body after playing",
                        "weekly": "Clean fingerboard, check tuning stability",
                        "monthly": "Deep clean, condition fingerboard if needed",
                        "annual": "Professional setup and inspection"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Pickup replacement", "Bridge upgrade", "Tuner improvement"],
                        "recommended_budget": "€150-300 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8", 
                        "value_for_money": "9",
                        "versatility": "7"
                    },
                    "standout_features": ["Iconic P-Bass tone", "Excellent value", "Reliable performance"],
                    "notable_limitations": ["Limited tonal variety", "Single pickup design"],
                    "competitive_position": "Strong value leader in the €750-850 range, offering authentic P-Bass tone that competitors struggle to match"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Fender Player Precision Bass", "P-Bass", "bass guitar", "Fender bass", "precision bass"],
                    "readability_score": "Medium",
                    "word_count": "600"
                }
            }
        },
        {
            "product_input": {
                "sku": "MUSICMAN-STINGRAY-4",
                "name": "Music Man StingRay 4",
                "slug": "music-man-stingray-4",
                "brand": "Music Man",
                "category": "bass-guitars",
                "description": "The Music Man StingRay 4 is an iconic 4-string bass that has defined the sound of modern bass playing since its introduction.",
                "specifications": {
                    "body_material": "Ash",
                    "neck_material": "Maple",
                    "fingerboard": "Maple",
                    "pickups": "Music Man Humbucker",
                    "scale_length": "34 inches",
                    "frets": 21,
                    "bridge": "Music Man Fixed Bridge",
                    "tuners": "Schaller BM",
                    "preamp": "3-Band Active EQ",
                    "strings": 4
                },
                "msrp_price": 1999,
                "images": ["musicman_stingray_1.jpg", "musicman_stingray_2.jpg", "musicman_stingray_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Music Man StingRay 4 represents the pinnacle of modern bass design, delivering powerful, distinctive tone with exceptional playability and craftsmanship.",
                    "key_features": ["Music Man humbucking pickup", "3-band active EQ", "Music Man fixed bridge", "Schaller BM tuners"],
                    "target_skill_level": "Advanced",
                    "country_of_origin": "United States",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Powerful, punchy, and distinctive with excellent clarity and definition across all frequencies",
                        "output_level": "High",
                        "best_genres": ["Funk", "Rock", "Jazz", "Fusion", "Pop"],
                        "pickup_characteristics": {
                            "humbucker": "High-output design with excellent clarity and punch",
                            "active_eq": "3-band EQ provides extensive tonal shaping capabilities",
                            "preamp": "Active electronics deliver consistent tone and output"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Solid Body",
                        "hardware_quality": "Premium",
                        "finish_quality": "Professional finish with excellent attention to detail",
                        "expected_durability": "Very High"
                    },
                    "playability": {
                        "neck_profile": "Comfortable profile with excellent access to upper frets",
                        "action_setup": "Low action potential with excellent setup from factory",
                        "comfort_rating": "9/10 - Excellent ergonomics and comfortable playing feel",
                        "weight_category": "Medium to Heavy with excellent balance"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Iconic StingRay Sound and Heritage",
                            "description": "Delivers the legendary StingRay tone that has shaped modern bass playing for decades."
                        },
                        {
                            "title": "Premium USA Construction",
                            "description": "Handcrafted in the USA with premium materials and exceptional attention to detail."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Premium Price Point",
                            "description": "High price may be beyond the budget of many intermediate players."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Professional bassists and serious players",
                            "reason": "Delivers the ultimate in modern bass tone and craftsmanship"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Beginners or budget-conscious players",
                            "reason": "Premium price and advanced features may not suit all players"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["High-quality bass amplifiers", "PA systems", "Studio recording"],
                    "suitable_music_styles": {
                        "excellent": ["Funk", "Rock", "Jazz", "Fusion", "Pop"],
                        "good": ["Blues", "R&B", "Alternative"],
                        "limited": ["Traditional country", "Classical"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate to High",
                        "growth_potential": "Excellent for developing advanced bass technique and understanding of modern bass tone"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Battery replacement", "EQ adjustment", "String changes"],
                    "care_instructions": {
                        "daily": "Wipe down after playing, check battery level",
                        "weekly": "Clean fingerboard, check tuning stability",
                        "monthly": "Deep clean, condition fingerboard if needed",
                        "annual": "Professional setup and electronics check"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["String upgrades", "Preamp modification", "Hardware improvement"],
                        "recommended_budget": "€200-500 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "10",
                        "sound_quality": "10", 
                        "value_for_money": "8",
                        "versatility": "9"
                    },
                    "standout_features": ["Iconic StingRay tone", "Premium USA construction", "Exceptional playability"],
                    "notable_limitations": ["Premium price point", "Active electronics require battery"],
                    "competitive_position": "Premium offering in the €1900-2100 range, representing the gold standard for modern bass design and tone"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Music Man StingRay", "StingRay bass", "active bass", "USA bass", "premium bass"],
                    "readability_score": "Medium",
                    "word_count": "650"
                }
            }
        },
        {
            "product_input": {
                "sku": "PEARL-EXPORT-5PC",
                "name": "Pearl Export 5-Piece Drum Set",
                "slug": "pearl-export-5-piece-drum-set",
                "brand": "Pearl",
                "category": "drums-percussion",
                "description": "The Pearl Export 5-Piece Drum Set is a professional-quality drum kit that offers exceptional value for drummers at all skill levels.",
                "specifications": {
                    "shell_material": "Poplar",
                    "shell_configuration": "6-ply",
                    "bass_drum": "22 x 18 inches",
                    "rack_toms": "12 x 9, 13 x 10 inches",
                    "floor_tom": "16 x 16 inches",
                    "snare_drum": "14 x 5.5 inches",
                    "hardware": "Pearl 800 Series",
                    "finish": "Chrome",
                    "included_cymbals": "Hi-hat, Crash, Ride",
                    "included_hardware": "Bass drum pedal, hi-hat stand, cymbal stands, snare stand, tom mounts"
                },
                "msrp_price": 599,
                "images": ["pearl_export_1.jpg", "pearl_export_2.jpg", "pearl_export_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Pearl Export 5-Piece Drum Set delivers professional-quality sound and construction at an accessible price point. Perfect for beginners learning the fundamentals or intermediate players seeking a reliable practice and performance kit.",
                    "key_features": ["6-ply poplar shells", "Pearl 800 Series hardware", "Complete setup with cymbals", "Professional chrome finish"],
                    "target_skill_level": "Beginner to Intermediate",
                    "country_of_origin": "Taiwan",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Warm, resonant tones with good projection and balanced frequency response",
                        "output_level": "High",
                        "best_genres": ["Rock", "Pop", "Jazz", "Practice", "Small venues"],
                        "drum_characteristics": {
                            "bass_drum": "Deep, punchy low end with good projection",
                            "rack_toms": "Clear, focused midrange tones with good sustain",
                            "floor_tom": "Rich, resonant low-mid tones",
                            "snare_drum": "Crisp, cutting sound with good sensitivity"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Acoustic Drums",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional chrome finish with good attention to detail",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "setup_flexibility": "Standard 5-piece configuration offers good versatility",
                        "hardware_quality": "Pearl 800 Series provides reliable performance",
                        "comfort_rating": "8/10 - Good ergonomics with standard drum set layout",
                        "weight_category": "Medium - typical drum set weight"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Complete Professional Setup",
                            "description": "Includes everything needed to start playing immediately with quality hardware and cymbals."
                        },
                        {
                            "title": "Excellent Value for Quality",
                            "description": "Professional Pearl quality at an accessible price point for developing drummers."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Basic Cymbal Quality",
                            "description": "Included cymbals are entry-level and may need upgrading for serious playing."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Beginners and developing drummers",
                            "reason": "Provides complete professional setup at an accessible price point"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Professional touring drummers",
                            "reason": "Basic cymbals and hardware may not meet professional touring requirements"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_cymbals": ["Upgrade to professional cymbals", "Add additional crash cymbals", "Consider splash cymbals"],
                    "suitable_music_styles": {
                        "excellent": ["Rock", "Pop", "Practice", "Small venues"],
                        "good": ["Jazz", "Blues", "Country"],
                        "limited": ["Large venue performance", "Professional recording"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for developing fundamental drumming skills and technique"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Head replacement", "Hardware adjustment", "Cymbal care"],
                    "care_instructions": {
                        "daily": "Wipe down drums and cymbals after playing",
                        "weekly": "Check hardware tightness, clean cymbals",
                        "monthly": "Deep clean, check head condition",
                        "annual": "Professional head replacement and hardware inspection"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Cymbal upgrades", "Head replacement", "Hardware improvement"],
                        "recommended_budget": "€200-500 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7", 
                        "value_for_money": "9",
                        "versatility": "8"
                    },
                    "standout_features": ["Complete setup", "Good value", "Reliable hardware"],
                    "notable_limitations": ["Basic cymbals", "Entry-level hardware"],
                    "competitive_position": "Strong value leader in the €550-650 range, offering complete professional setup that exceeds expectations at this price point"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Pearl Export", "drum set", "5-piece drums", "beginner drums", "complete drum kit"],
                    "readability_score": "Medium",
                    "word_count": "550"
                }
            }
        },
        {
            "product_input": {
                "sku": "DW-COLLECTOR-SERIES",
                "name": "DW Collector's Series 5-Piece",
                "slug": "dw-collectors-series-5-piece",
                "brand": "DW",
                "category": "drums-percussion",
                "description": "The DW Collector's Series 5-Piece represents the pinnacle of drum craftsmanship, delivering exceptional sound quality and precision engineering.",
                "specifications": {
                    "shell_material": "North American Maple",
                    "shell_configuration": "Custom ply",
                    "bass_drum": "22 x 18 inches",
                    "rack_toms": "10 x 8, 12 x 9 inches",
                    "floor_tom": "16 x 16 inches",
                    "snare_drum": "14 x 6.5 inches",
                    "hardware": "DW 9000 Series",
                    "finish": "Custom lacquer",
                    "tuning_system": "True Pitch",
                    "snare_mechanism": "Mag throw-off",
                    "included_hardware": "Bass drum pedal, hi-hat stand, cymbal stands, snare stand, tom mounts"
                },
                "msrp_price": 3499,
                "images": ["dw_collectors_1.jpg", "dw_collectors_2.jpg", "dw_collectors_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The DW Collector's Series represents the ultimate in drum craftsmanship, delivering exceptional sound quality and precision engineering. Each shell is carefully selected and crafted using DW's proprietary shell technology.",
                    "key_features": ["North American maple shells", "DW 9000 Series hardware", "True Pitch tuning system", "Mag throw-off snare mechanism"],
                    "target_skill_level": "Professional",
                    "country_of_origin": "United States",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Rich, warm, and articulate with exceptional clarity and projection",
                        "output_level": "Very High",
                        "best_genres": ["Professional recording", "Live performance", "Jazz", "Rock", "All styles"],
                        "drum_characteristics": {
                            "bass_drum": "Deep, powerful low end with excellent control and projection",
                            "rack_toms": "Clear, focused tones with excellent sustain and resonance",
                            "floor_tom": "Rich, resonant tones with exceptional depth",
                            "snare_drum": "Crisp, cutting sound with excellent sensitivity and response"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Professional Acoustic Drums",
                        "hardware_quality": "Premium",
                        "finish_quality": "Custom lacquer finish with exceptional attention to detail",
                        "expected_durability": "Very High"
                    },
                    "playability": {
                        "setup_flexibility": "Highly configurable with professional hardware",
                        "hardware_quality": "DW 9000 Series provides exceptional performance and reliability",
                        "comfort_rating": "10/10 - Professional ergonomics with excellent hardware quality",
                        "weight_category": "Heavy - professional drum set weight"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Ultimate Drum Craftsmanship",
                            "description": "Represents the pinnacle of drum design and construction with exceptional attention to detail."
                        },
                        {
                            "title": "Professional Sound Quality",
                            "description": "Delivers exceptional sound quality suitable for professional recording and live performance."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Premium Price Point",
                            "description": "High price may be beyond the budget of many developing drummers."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Professional drummers and serious players",
                            "reason": "Delivers the ultimate in drum craftsmanship and sound quality"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Beginners or budget-conscious players",
                            "reason": "Premium price and professional features may not suit all players"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_cymbals": ["Professional cymbal sets", "Custom cymbal configurations", "High-quality hardware"],
                    "suitable_music_styles": {
                        "excellent": ["Professional recording", "Live performance", "All music styles"],
                        "good": ["Studio work", "Touring", "Jazz"],
                        "limited": ["None - suitable for all styles"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for developing professional drumming skills and technique"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "High",
                    "common_issues": ["Professional head replacement", "Hardware maintenance", "Finish care"],
                    "care_instructions": {
                        "daily": "Professional cleaning and maintenance",
                        "weekly": "Hardware inspection and adjustment",
                        "monthly": "Deep cleaning and head inspection",
                        "annual": "Professional maintenance and hardware service"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Custom finishes", "Additional drums", "Hardware customization"],
                        "recommended_budget": "€500-1000+ for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "10",
                        "sound_quality": "10", 
                        "value_for_money": "9",
                        "versatility": "10"
                    },
                    "standout_features": ["Exceptional craftsmanship", "Professional sound quality", "Premium hardware"],
                    "notable_limitations": ["Premium price point", "Professional maintenance requirements"],
                    "competitive_position": "Premium offering in the €3400-3600 range, representing the gold standard for professional drum craftsmanship and sound quality"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["DW Collector's Series", "professional drums", "USA drums", "premium drums", "DW drums"],
                    "readability_score": "Medium",
                    "word_count": "600"
                }
            }
        }
    ]
}

async def get_or_create_brand(session: AsyncSession, brand_name: str) -> Brand:
    """Get existing brand or create new one."""
    result = await session.execute(select(Brand).where(Brand.name == brand_name))
    brand = result.scalar_one_or_none()
    
    if not brand:
        brand = Brand(
            name=brand_name,
            slug=brand_name.lower().replace(" ", "-"),
            description=f"Professional {brand_name} musical instruments and equipment"
        )
        session.add(brand)
        await session.flush()
    
    return brand

async def get_or_create_category(session: AsyncSession, category_slug: str) -> Category:
    """Get existing category or create new one."""
    result = await session.execute(select(Category).where(Category.slug == category_slug))
    category = result.scalar_one_or_none()
    
    if not category:
        # Create category name from slug
        category_name = category_slug.replace("-", " ").title()
        category = Category(
            name=category_name,
            slug=category_slug,
            description=f"Professional {category_name} for musicians"
        )
        session.add(category)
        await session.flush()
    
    return category

async def create_products():
    """Create all products in the database."""
    async with async_session_factory() as session:
        try:
            created_count = 0
            
            for product_data in COMPLETE_PRODUCTS_DATA["comprehensive_product_dataset"]:
                product_input = product_data["product_input"]
                ai_content = product_data["ai_generated_content"]
                
                print(f"Processing product: {product_input['name']}")
                
                # Check if product already exists
                result = await session.execute(
                    select(Product).where(Product.sku == product_input["sku"])
                )
                existing_product = result.scalar_one_or_none()
                
                if existing_product:
                    print(f"Product {product_input['sku']} already exists, skipping...")
                    continue
                
                # Get or create brand
                brand = await get_or_create_brand(session, product_input["brand"])
                
                # Get or create category
                category = await get_or_create_category(session, product_input["category"])
                
                # Create product
                product = Product(
                    sku=product_input["sku"],
                    name=product_input["name"],
                    slug=product_input["slug"],
                    brand_id=brand.id,
                    category_id=category.id,
                    description=product_input["description"],
                    specifications=product_input["specifications"],
                    images=product_input["images"],
                    msrp_price=Decimal(str(product_input["msrp_price"])),
                    ai_generated_content=ai_content,
                    is_active=True
                )
                
                session.add(product)
                created_count += 1
                print(f"Created product: {product_input['name']}")
            
            await session.commit()
            print(f"\nSuccessfully created {created_count} new products!")
            
        except Exception as e:
            await session.rollback()
            print(f"Error creating products: {e}")
            raise

async def main():
    """Main function to run the product creation."""
    print("Starting product creation process...")
    await create_products()
    print("Product creation completed!")

if __name__ == "__main__":
    asyncio.run(main())
