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
        },
        {
            "product_input": {
                "sku": "BOSS-DS1-DISTORTION",
                "name": "Boss DS-1 Distortion",
                "slug": "boss-ds-1-distortion",
                "brand": "Boss",
                "category": "effects-pedals",
                "description": "The Boss DS-1 Distortion is one of the most iconic and widely-used distortion pedals in music history, trusted by countless guitarists for its reliable, versatile tone.",
                "specifications": {
                    "effect_type": "Distortion",
                    "controls": "Tone, Distortion, Level",
                    "power_supply": "9V DC (Boss PSA adapter) or 9V battery",
                    "current_draw": "4mA",
                    "input_impedance": "1M ohm",
                    "output_impedance": "1k ohm",
                    "bypass": "Buffered",
                    "enclosure": "Boss compact",
                    "dimensions": "73 x 129 x 59 mm",
                    "weight": "360g"
                },
                "msrp_price": 59,
                "images": ["boss_ds1_1.jpg", "boss_ds1_2.jpg", "boss_ds1_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Boss DS-1 Distortion is a legendary pedal that has shaped the sound of rock music for decades. Its distinctive midrange-focused distortion has been featured on countless recordings and continues to be a favorite among both beginners and professional musicians.",
                    "key_features": ["Classic distortion tone", "Simple three-knob design", "Rugged construction", "Affordable price"],
                    "target_skill_level": "All levels",
                    "country_of_origin": "Taiwan",
                    "release_year": "1978"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Midrange-focused distortion with good sustain and harmonics",
                        "output_level": "Medium to High",
                        "best_genres": ["Rock", "Punk", "Metal", "Alternative"],
                        "control_characteristics": {
                            "tone": "Smooth tone control from dark to bright",
                            "distortion": "Wide range from subtle overdrive to full distortion",
                            "level": "Good output level control for various amplifiers"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Solid State",
                        "hardware_quality": "Standard",
                        "finish_quality": "Durable Boss construction with excellent reliability",
                        "expected_durability": "Very High"
                    },
                    "playability": {
                        "ease_of_use": "Very simple three-knob interface",
                        "versatility": "Excellent for various distortion needs",
                        "comfort_rating": "10/10 - Simple and intuitive operation",
                        "weight_category": "Light - compact and portable"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Iconic Distortion Sound",
                            "description": "Delivers the classic distortion tone that has defined rock music for generations."
                        },
                        {
                            "title": "Bulletproof Reliability",
                            "description": "Boss construction ensures it can withstand the rigors of live performance and touring."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Tonal Variety",
                            "description": "Single distortion type may not provide the variety some players require."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Rock and punk guitarists",
                            "reason": "Provides classic distortion tone at an affordable price"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Players requiring extensive tonal variety",
                            "reason": "Single distortion type limits tonal options"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Clean amplifiers", "Tube amplifiers", "Solid state amplifiers"],
                    "suitable_music_styles": {
                        "excellent": ["Rock", "Punk", "Metal", "Alternative"],
                        "good": ["Blues", "Hard Rock"],
                        "limited": ["Jazz", "Clean acoustic-style playing"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for learning distortion techniques and tone shaping"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Low",
                    "common_issues": ["Battery replacement", "Connection cleaning"],
                    "care_instructions": {
                        "daily": "Check battery level, clean connections",
                        "weekly": "Clean pedal surface",
                        "monthly": "Deep clean if needed",
                        "annual": "Professional inspection if needed"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Power supply upgrade", "Modification kits"],
                        "recommended_budget": "€20-50 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "9",
                        "sound_quality": "8", 
                        "value_for_money": "10",
                        "versatility": "7"
                    },
                    "standout_features": ["Iconic distortion tone", "Bulletproof reliability", "Excellent value"],
                    "notable_limitations": ["Limited tonal variety", "Basic feature set"],
                    "competitive_position": "Outstanding value leader in the €50-70 range, offering iconic tone that has stood the test of time"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Boss DS-1", "distortion pedal", "rock distortion", "guitar effects", "Boss pedal"],
                    "readability_score": "Medium",
                    "word_count": "500"
                }
            }
        },
        {
            "product_input": {
                "sku": "ELECTRO-HARMONIX-BIGMUFF",
                "name": "Electro-Harmonix Big Muff Pi",
                "slug": "electro-harmonix-big-muff-pi",
                "brand": "Electro-Harmonix",
                "category": "effects-pedals",
                "description": "The Electro-Harmonix Big Muff Pi is the legendary fuzz pedal that has shaped the sound of rock music for over 50 years.",
                "specifications": {
                    "effect_type": "Fuzz",
                    "controls": "Sustain, Tone, Volume",
                    "power_supply": "9V DC or 9V battery",
                    "current_draw": "2.5mA",
                    "input_impedance": "500k ohm",
                    "output_impedance": "10k ohm",
                    "bypass": "True bypass",
                    "enclosure": "Standard size",
                    "dimensions": "119 x 93 x 32 mm",
                    "weight": "200g"
                },
                "msrp_price": 89,
                "images": ["ehx_bigmuff_1.jpg", "ehx_bigmuff_2.jpg", "ehx_bigmuff_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Electro-Harmonix Big Muff Pi delivers massive, sustaining fuzz tones that have been used by guitarists from David Gilmour to Jack White. This iconic pedal creates harmonically rich distortion with excellent sustain.",
                    "key_features": ["Massive fuzz tone", "Excellent sustain", "Three-knob design", "True bypass"],
                    "target_skill_level": "Intermediate to Advanced",
                    "country_of_origin": "United States",
                    "release_year": "1969"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Thick, creamy fuzz with harmonically rich distortion and excellent sustain",
                        "output_level": "High",
                        "best_genres": ["Rock", "Psychedelic Rock", "Stoner Rock", "Alternative"],
                        "control_characteristics": {
                            "sustain": "Controls the amount of fuzz and sustain",
                            "tone": "Shapes the overall tonal character",
                            "volume": "Controls output level"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Solid State",
                        "hardware_quality": "Standard",
                        "finish_quality": "Classic EHX styling with good durability",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "ease_of_use": "Simple three-knob interface",
                        "versatility": "Excellent for creating walls of sound",
                        "comfort_rating": "9/10 - Simple and effective operation",
                        "weight_category": "Light - compact design"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Iconic Fuzz Tone",
                            "description": "Delivers the legendary Big Muff fuzz sound that has defined generations of rock music."
                        },
                        {
                            "title": "Excellent Sustain",
                            "description": "Creates massive, sustaining fuzz tones perfect for lead work and power chords."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Clean Headroom",
                            "description": "High-gain fuzz may not suit players requiring clean tones."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Rock and psychedelic guitarists",
                            "reason": "Provides iconic fuzz tone with excellent sustain for lead work"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Players requiring clean tones",
                            "reason": "High-gain fuzz design limits clean headroom"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Clean amplifiers", "Tube amplifiers", "High-headroom amplifiers"],
                    "suitable_music_styles": {
                        "excellent": ["Rock", "Psychedelic Rock", "Stoner Rock", "Alternative"],
                        "good": ["Blues", "Hard Rock"],
                        "limited": ["Jazz", "Country", "Clean playing"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate",
                        "growth_potential": "Excellent for developing fuzz techniques and sustain control"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Low",
                    "common_issues": ["Battery replacement", "Connection cleaning"],
                    "care_instructions": {
                        "daily": "Check battery level, clean connections",
                        "weekly": "Clean pedal surface",
                        "monthly": "Deep clean if needed",
                        "annual": "Professional inspection if needed"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Power supply upgrade", "Modification kits"],
                        "recommended_budget": "€30-80 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "9", 
                        "value_for_money": "9",
                        "versatility": "8"
                    },
                    "standout_features": ["Iconic fuzz tone", "Excellent sustain", "Classic design"],
                    "notable_limitations": ["Limited clean headroom", "High-gain nature"],
                    "competitive_position": "Strong value offering in the €80-100 range, delivering iconic fuzz tone that has shaped music history"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Electro-Harmonix Big Muff", "fuzz pedal", "Big Muff Pi", "guitar fuzz", "EHX pedal"],
                    "readability_score": "Medium",
                    "word_count": "550"
                }
            }
        },
        {
            "product_input": {
                "sku": "PIONEER-DDJ-400",
                "name": "Pioneer DDJ-400 Controller",
                "slug": "pioneer-ddj-400-controller",
                "brand": "Pioneer",
                "category": "dj-equipment",
                "description": "The Pioneer DDJ-400 is a professional-grade DJ controller designed specifically for Rekordbox software, offering an intuitive interface that mirrors the layout of Pioneer's flagship CDJ and DJM equipment.",
                "specifications": {
                    "channels": 2,
                    "jog_wheels": "Full-size with touch display",
                    "software_compatibility": "Rekordbox DJ",
                    "sound_card": "Built-in 24-bit/48kHz",
                    "hot_cues": "8 per deck",
                    "effects": "Beat FX",
                    "connectivity": "USB Type-B",
                    "power_supply": "USB bus powered",
                    "dimensions": "320 x 107 x 25 mm",
                    "weight": "1.2 kg"
                },
                "msrp_price": 299,
                "images": ["pioneer_ddj400_1.jpg", "pioneer_ddj400_2.jpg", "pioneer_ddj400_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Pioneer DDJ-400 provides professional DJ functionality in a compact, portable design. Perfect for beginners learning the fundamentals of DJing as well as experienced DJs seeking a reliable controller for mobile gigs.",
                    "key_features": ["Full-size jog wheels with touch display", "Rekordbox DJ integration", "Built-in sound card", "8 hot cues per deck"],
                    "target_skill_level": "Beginner to Intermediate",
                    "country_of_origin": "China",
                    "release_year": "2018"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "audio_quality": "24-bit/48kHz sound card provides clear, professional audio",
                        "output_level": "High",
                        "best_genres": ["All electronic music styles", "Hip-hop", "Pop", "House"],
                        "controller_features": {
                            "jog_wheels": "Full-size with touch display for visual feedback",
                            "hot_cues": "8 per deck for quick track access",
                            "effects": "Beat FX for creative mixing",
                            "crossfader": "Smooth crossfader for seamless transitions"
                        }
                    },
                    "build_quality": {
                        "construction_type": "DJ Controller",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional Pioneer styling with good durability",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "interface_design": "Mirrors Pioneer CDJ/DJM layout for familiar operation",
                        "ease_of_use": "Intuitive design perfect for learning",
                        "comfort_rating": "9/10 - Excellent ergonomics and familiar Pioneer layout",
                        "weight_category": "Light - highly portable"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Professional Pioneer Quality",
                            "description": "Delivers Pioneer's renowned DJ equipment quality and reliability at an accessible price."
                        },
                        {
                            "title": "Perfect for Learning",
                            "description": "Mirrors professional CDJ layout, making it ideal for learning industry-standard equipment."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Advanced Features",
                            "description": "Basic feature set may not satisfy advanced DJs requiring extensive functionality."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Beginner and intermediate DJs",
                            "reason": "Provides professional Pioneer quality with excellent learning features"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Advanced DJs requiring extensive features",
                            "reason": "Basic feature set compared to professional CDJ setups"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_software": ["Rekordbox DJ", "Rekordbox"],
                    "suitable_music_styles": {
                        "excellent": ["Electronic", "Hip-hop", "Pop", "House"],
                        "good": ["Rock", "Jazz", "All styles"],
                        "limited": ["None - suitable for all styles"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for developing fundamental DJ skills and techniques"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Low",
                    "common_issues": ["Software updates", "Connection cleaning", "Firmware updates"],
                    "care_instructions": {
                        "daily": "Clean controller surface after use",
                        "weekly": "Update software and firmware",
                        "monthly": "Deep clean, check connections",
                        "annual": "Professional inspection if needed"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Software upgrades", "Additional accessories"],
                        "recommended_budget": "€50-150 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8", 
                        "value_for_money": "9",
                        "versatility": "8"
                    },
                    "standout_features": ["Professional Pioneer quality", "Excellent learning tool", "Portable design"],
                    "notable_limitations": ["Limited advanced features", "Basic sound card"],
                    "competitive_position": "Strong value offering in the €250-350 range, providing professional Pioneer quality for learning and mobile use"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Pioneer DDJ-400", "DJ controller", "Rekordbox", "Pioneer DJ", "beginner DJ"],
                    "readability_score": "Medium",
                    "word_count": "600"
                }
            }
        },
        {
            "product_input": {
                "sku": "NUMARK-MIXTRACK-PRO-3",
                "name": "Numark Mixtrack Pro 3",
                "slug": "numark-mixtrack-pro-3",
                "brand": "Numark",
                "category": "dj-equipment",
                "description": "The Numark Mixtrack Pro 3 is a feature-rich DJ controller that provides professional performance capabilities at an accessible price point.",
                "specifications": {
                    "channels": 2,
                    "jog_wheels": "Large with LED rings",
                    "software_compatibility": "Serato DJ Intro",
                    "sound_card": "Built-in 24-bit/48kHz",
                    "performance_pads": "8 per deck",
                    "effects": "Built-in filters and effects",
                    "connectivity": "USB Type-B",
                    "power_supply": "USB bus powered",
                    "dimensions": "330 x 110 x 25 mm",
                    "weight": "1.1 kg"
                },
                "msrp_price": 199,
                "images": ["numark_mixtrack_pro3_1.jpg", "numark_mixtrack_pro3_2.jpg", "numark_mixtrack_pro3_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Numark Mixtrack Pro 3 delivers professional DJ performance features in a compact, affordable package. The built-in audio interface eliminates the need for external sound cards, while the included Serato DJ Intro software provides a complete DJ solution.",
                    "key_features": ["Large jog wheels with LED rings", "Built-in audio interface", "8 performance pads per deck", "Serato DJ Intro included"],
                    "target_skill_level": "Beginner to Intermediate",
                    "country_of_origin": "China",
                    "release_year": "2016"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "audio_quality": "24-bit/48kHz sound card provides clear, professional audio",
                        "output_level": "High",
                        "best_genres": ["All electronic music styles", "Hip-hop", "Pop", "House"],
                        "controller_features": {
                            "jog_wheels": "Large with LED rings for visual feedback",
                            "performance_pads": "8 per deck for hot cues, loops, and samples",
                            "effects": "Built-in filters and effects for creative mixing",
                            "crossfader": "Smooth crossfader for seamless transitions"
                        }
                    },
                    "build_quality": {
                        "construction_type": "DJ Controller",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional Numark styling with good durability",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "interface_design": "Intuitive layout with large, responsive controls",
                        "ease_of_use": "User-friendly design perfect for learning",
                        "comfort_rating": "8/10 - Good ergonomics with responsive controls",
                        "weight_category": "Light - highly portable"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Excellent Value for Features",
                            "description": "Offers professional DJ features at an accessible price point with included software."
                        },
                        {
                            "title": "Complete DJ Solution",
                            "description": "Built-in audio interface and included software provide everything needed to start DJing."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Advanced Features",
                            "description": "Basic feature set may not satisfy advanced DJs requiring extensive functionality."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Beginner and mobile DJs",
                            "reason": "Provides excellent value and features for learning and mobile use"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Advanced DJs requiring extensive features",
                            "reason": "Basic feature set compared to professional setups"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_software": ["Serato DJ Intro", "Serato DJ"],
                    "suitable_music_styles": {
                        "excellent": ["Electronic", "Hip-hop", "Pop", "House"],
                        "good": ["Rock", "Jazz", "All styles"],
                        "limited": ["None - suitable for all styles"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for developing fundamental DJ skills and techniques"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Low",
                    "common_issues": ["Software updates", "Connection cleaning", "Firmware updates"],
                    "care_instructions": {
                        "daily": "Clean controller surface after use",
                        "weekly": "Update software and firmware",
                        "monthly": "Deep clean, check connections",
                        "annual": "Professional inspection if needed"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Software upgrades", "Additional accessories"],
                        "recommended_budget": "€30-100 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7", 
                        "value_for_money": "9",
                        "versatility": "7"
                    },
                    "standout_features": ["Excellent value", "Complete DJ solution", "Portable design"],
                    "notable_limitations": ["Limited advanced features", "Basic sound card"],
                    "competitive_position": "Outstanding value leader in the €180-220 range, offering features that typically cost much more"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Numark Mixtrack Pro 3", "DJ controller", "Serato DJ", "beginner DJ", "mobile DJ"],
                    "readability_score": "Medium",
                    "word_count": "550"
                }
            }
        },
        {
            "product_input": {
                "sku": "FOCUSRITE-SCARLETT-2I2",
                "name": "Focusrite Scarlett 2i2 Audio Interface",
                "slug": "focusrite-scarlett-2i2-audio-interface",
                "brand": "Focusrite",
                "category": "studio-and-recording-equipment",
                "description": "The Focusrite Scarlett 2i2 is a professional 2-in, 2-out USB audio interface that delivers exceptional sound quality and reliability for home recording and music production.",
                "specifications": {
                    "inputs": "2 x XLR/TRS combo",
                    "outputs": "2 x TRS",
                    "preamps": "Focusrite preamps with 56dB gain",
                    "conversion": "24-bit/192kHz",
                    "connectivity": "USB 2.0",
                    "phantom_power": "48V",
                    "direct_monitoring": "Yes",
                    "software_bundle": "Included",
                    "power_supply": "USB bus powered",
                    "dimensions": "170 x 120 x 35 mm",
                    "weight": "0.5 kg"
                },
                "msrp_price": 169,
                "images": ["focusrite_scarlett_2i2_1.jpg", "focusrite_scarlett_2i2_2.jpg", "focusrite_scarlett_2i2_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Focusrite Scarlett 2i2 provides professional-quality audio recording capabilities in a compact, affordable package. Perfect for solo artists, podcasters, and home studio enthusiasts seeking professional sound quality.",
                    "key_features": ["High-quality Focusrite preamps", "24-bit/192kHz conversion", "Direct monitoring", "Included software bundle"],
                    "target_skill_level": "Beginner to Intermediate",
                    "country_of_origin": "United Kingdom",
                    "release_year": "2019"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "audio_quality": "24-bit/192kHz conversion ensures pristine audio fidelity",
                        "preamps": "Focusrite preamps provide clean, transparent gain with up to 56dB headroom",
                        "best_applications": ["Vocal recording", "Guitar recording", "Podcasting", "Home studio"],
                        "interface_features": {
                            "direct_monitoring": "Zero-latency monitoring during recording",
                            "phantom_power": "48V phantom power for condenser microphones",
                            "software_bundle": "Included software provides essential tools for music production"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Audio Interface",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional red finish with good durability",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "ease_of_use": "Simple plug-and-play operation",
                        "software_compatibility": "Compatible with all major DAWs",
                        "comfort_rating": "9/10 - Simple operation with excellent software compatibility",
                        "weight_category": "Light - highly portable"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Professional Sound Quality",
                            "description": "Delivers exceptional sound quality and reliability for home recording and music production."
                        },
                        {
                            "title": "Excellent Value",
                            "description": "Professional-quality audio interface at an accessible price point with included software."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Input/Output",
                            "description": "2-in, 2-out configuration may not suit complex recording setups."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Solo artists and home studio enthusiasts",
                            "reason": "Provides professional-quality recording capabilities at an accessible price"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Complex recording setups",
                            "reason": "Limited I/O may not accommodate multiple simultaneous recordings"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_software": ["All major DAWs", "Included software bundle"],
                    "suitable_applications": {
                        "excellent": ["Vocal recording", "Guitar recording", "Podcasting", "Home studio"],
                        "good": ["Small band recording", "Live streaming"],
                        "limited": ["Complex multi-track recording", "Large studio setups"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for developing recording and production skills"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Low",
                    "common_issues": ["Driver updates", "Connection cleaning", "Software updates"],
                    "care_instructions": {
                        "daily": "Check connections, update drivers if needed",
                        "weekly": "Clean interface surface",
                        "monthly": "Update software and firmware",
                        "annual": "Professional inspection if needed"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Software upgrades", "Additional accessories"],
                        "recommended_budget": "€50-150 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8", 
                        "value_for_money": "9",
                        "versatility": "7"
                    },
                    "standout_features": ["Professional sound quality", "Excellent value", "Included software"],
                    "notable_limitations": ["Limited I/O", "Basic feature set"],
                    "competitive_position": "Strong value leader in the €150-180 range, offering professional sound quality that exceeds expectations at this price point"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Focusrite Scarlett 2i2", "audio interface", "recording interface", "home studio", "USB interface"],
                    "readability_score": "Medium",
                    "word_count": "550"
                }
            }
        },
        {
            "product_input": {
                "sku": "SHURE-SM7B-MICROPHONE",
                "name": "Shure SM7B Dynamic Microphone",
                "slug": "shure-sm7b-dynamic-microphone",
                "brand": "Shure",
                "category": "studio-and-recording-equipment",
                "description": "The Shure SM7B is a legendary dynamic microphone that has been the choice of professional broadcasters, podcasters, and recording engineers for decades.",
                "specifications": {
                    "microphone_type": "Dynamic",
                    "polar_pattern": "Cardioid",
                    "frequency_response": "50Hz - 20kHz",
                    "sensitivity": "-59 dBV/Pa",
                    "impedance": "300 ohms",
                    "connector": "XLR-3M",
                    "shock_mount": "Internal",
                    "windscreen": "Included",
                    "weight": "765g",
                    "dimensions": "162 x 51 mm"
                },
                "msrp_price": 399,
                "images": ["shure_sm7b_1.jpg", "shure_sm7b_2.jpg", "shure_sm7b_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Shure SM7B delivers exceptional sound quality for vocals, instruments, and speech, with a smooth, flat, wide-range frequency response that captures natural sound with excellent detail.",
                    "key_features": ["Cardioid polar pattern", "Wide frequency response", "Internal shock mount", "Included windscreen"],
                    "target_skill_level": "Professional",
                    "country_of_origin": "United States",
                    "release_year": "1973"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "audio_quality": "Smooth, flat frequency response with excellent detail and natural sound",
                        "polar_pattern": "Cardioid pattern provides excellent rejection of unwanted background noise",
                        "best_applications": ["Vocal recording", "Broadcasting", "Podcasting", "Instrument recording"],
                        "microphone_features": {
                            "shock_mount": "Internal shock mount reduces handling noise and mechanical vibration",
                            "windscreen": "Included windscreen provides protection against wind and breath noise",
                            "frequency_response": "50Hz - 20kHz provides excellent coverage of vocal and instrument frequencies"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Dynamic Microphone",
                        "hardware_quality": "Premium",
                        "finish_quality": "Professional finish with excellent durability",
                        "expected_durability": "Very High"
                    },
                    "playability": {
                        "ease_of_use": "Simple plug-and-play operation",
                        "versatility": "Excellent for various recording applications",
                        "comfort_rating": "9/10 - Excellent performance with minimal setup required",
                        "weight_category": "Medium - substantial professional microphone weight"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Legendary Sound Quality",
                            "description": "Delivers the exceptional sound quality that has made it an industry standard for decades."
                        },
                        {
                            "title": "Versatile Applications",
                            "description": "Excellent for vocals, broadcasting, podcasting, and instrument recording."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Requires Good Preamp",
                            "description": "Low sensitivity requires a high-quality preamp for optimal performance."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Professional broadcasters and recording engineers",
                            "reason": "Delivers the ultimate in professional microphone sound quality and reliability"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Beginners without good preamps",
                            "reason": "Low sensitivity requires quality preamp for optimal performance"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_preamps": ["High-quality preamps", "Cloudlifter", "Professional audio interfaces"],
                    "suitable_applications": {
                        "excellent": ["Vocal recording", "Broadcasting", "Podcasting", "Studio recording"],
                        "good": ["Live performance", "Instrument recording"],
                        "limited": ["Distant recording", "Field recording"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate",
                        "growth_potential": "Excellent for developing professional recording skills and techniques"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Low",
                    "common_issues": ["Dust accumulation", "Connection cleaning", "Windscreen care"],
                    "care_instructions": {
                        "daily": "Wipe down after use, check connections",
                        "weekly": "Clean windscreen and body",
                        "monthly": "Deep clean, inspect for damage",
                        "annual": "Professional inspection and cleaning"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Shock mount upgrade", "Windscreen replacement", "Cable upgrade"],
                        "recommended_budget": "€50-200 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "10",
                        "sound_quality": "10", 
                        "value_for_money": "9",
                        "versatility": "9"
                    },
                    "standout_features": ["Legendary sound quality", "Industry standard", "Exceptional reliability"],
                    "notable_limitations": ["Requires good preamp", "Low sensitivity"],
                    "competitive_position": "Premium offering in the €380-420 range, representing the gold standard for professional dynamic microphones"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Shure SM7B", "dynamic microphone", "broadcast microphone", "podcast microphone", "professional microphone"],
                    "readability_score": "Medium",
                    "word_count": "600"
                }
            }
        },
        {
            "product_input": {
                "sku": "IBANEZ-RG450DX",
                "name": "Ibanez RG450DX Electric Guitar",
                "slug": "ibanez-rg450dx-electric-guitar",
                "brand": "Ibanez",
                "category": "electric-guitars",
                "description": "The Ibanez RG450DX is a versatile electric guitar designed for high-performance playing with excellent playability and modern features.",
                "specifications": {
                    "body_material": "Poplar",
                    "neck_material": "Maple",
                    "fingerboard": "Jatoba",
                    "pickups": "2x Infinity R (H) Humbuckers, 1x Infinity RS (S) Single-coil",
                    "scale_length": "25.5 inches",
                    "frets": 24,
                    "bridge": "T106 Tremolo Bridge",
                    "tuners": "Die-cast",
                    "nut_width": "1.69 inches",
                    "finish": "Polyester"
                },
                "msrp_price": 299,
                "images": ["ibanez_rg450dx_1.jpg", "ibanez_rg450dx_2.jpg", "ibanez_rg450dx_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Ibanez RG450DX delivers high-performance playing capabilities at an accessible price point. The thin, fast neck and versatile pickup configuration make it perfect for rock, metal, and fusion styles.",
                    "key_features": ["Thin Wizard III neck", "24 jumbo frets", "H-S-H pickup configuration", "T106 tremolo bridge"],
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Indonesia",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Bright, cutting tones with excellent clarity and high-output capability",
                        "output_level": "High",
                        "best_genres": ["Rock", "Metal", "Fusion", "Progressive"],
                        "pickup_positions": {
                            "bridge_humbucker": "High-output tone perfect for lead work and heavy rhythm",
                            "middle_single": "Clear, articulate tone for clean and overdriven sounds",
                            "neck_humbucker": "Warm, smooth tone for leads and jazz applications"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Solid Body",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional polyester finish with good attention to detail",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "neck_profile": "Thin Wizard III neck offers fast, comfortable playing",
                        "action_setup": "Low action potential with excellent setup from factory",
                        "comfort_rating": "9/10 - Excellent for fast playing and technical passages",
                        "weight_category": "Light to Medium"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Excellent Value for Performance",
                            "description": "Delivers high-performance features at an accessible price point."
                        },
                        {
                            "title": "Versatile Pickup Configuration",
                            "description": "H-S-H setup provides excellent tonal variety for various playing styles."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Traditional Tones",
                            "description": "Modern design may not suit players seeking classic vintage tones."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Rock and metal guitarists",
                            "reason": "Provides excellent performance features for high-gain and technical playing"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Players seeking vintage tones",
                            "reason": "Modern design and high-output pickups may not provide classic vintage character"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["High-gain amplifiers", "Modeling amplifiers", "Clean amplifiers with pedals"],
                    "suitable_music_styles": {
                        "excellent": ["Rock", "Metal", "Fusion", "Progressive"],
                        "good": ["Jazz", "Blues", "Alternative"],
                        "limited": ["Traditional country", "Vintage blues"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate",
                        "growth_potential": "Excellent for developing technical playing skills and high-gain techniques"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Tremolo bridge setup", "Neck adjustment", "Pickup height adjustment"],
                    "care_instructions": {
                        "daily": "Wipe down strings and body after playing",
                        "weekly": "Clean fingerboard, check tuning stability",
                        "monthly": "Deep clean, check intonation",
                        "annual": "Professional setup and inspection"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Pickup replacement", "Bridge upgrade", "Tuner improvement"],
                        "recommended_budget": "€100-300 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7", 
                        "value_for_money": "9",
                        "versatility": "8"
                    },
                    "standout_features": ["Excellent playability", "Good value", "Versatile pickups"],
                    "notable_limitations": ["Basic hardware", "Limited vintage tones"],
                    "competitive_position": "Strong value offering in the €250-350 range, providing performance features that exceed expectations at this price point"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Ibanez RG450DX", "electric guitar", "metal guitar", "rock guitar", "Ibanez RG"],
                    "readability_score": "Medium",
                    "word_count": "550"
                }
            }
        },
        {
            "product_input": {
                "sku": "EPIPHONE-LES-PAUL-STANDARD",
                "name": "Epiphone Les Paul Standard",
                "slug": "epiphone-les-paul-standard",
                "brand": "Epiphone",
                "category": "electric-guitars",
                "description": "The Epiphone Les Paul Standard delivers classic Les Paul tone and feel with modern playability improvements at an accessible price point.",
                "specifications": {
                    "body_material": "Mahogany with Maple Top",
                    "neck_material": "Mahogany",
                    "fingerboard": "Rosewood",
                    "pickups": "2x Alnico Classic Humbuckers",
                    "scale_length": "24.75 inches",
                    "frets": 22,
                    "bridge": "LockTone Tune-o-matic with Stop Bar",
                    "tuners": "Grover Rotomatic",
                    "nut_width": "1.68 inches",
                    "finish": "Polyester"
                },
                "msrp_price": 599,
                "images": ["epiphone_les_paul_standard_1.jpg", "epiphone_les_paul_standard_2.jpg", "epiphone_les_paul_standard_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Epiphone Les Paul Standard offers authentic Les Paul tone and feel with modern improvements. The mahogany body with maple top delivers the classic Les Paul sound that has defined rock music.",
                    "key_features": ["Mahogany body with maple top", "Alnico Classic humbuckers", "LockTone bridge system", "Grover Rotomatic tuners"],
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "China",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Warm, rich, and sustaining with classic Les Paul midrange focus",
                        "output_level": "Medium to High",
                        "best_genres": ["Rock", "Blues", "Hard Rock", "Jazz"],
                        "pickup_positions": {
                            "bridge": "High-output tone perfect for lead work and heavy rhythm",
                            "neck": "Warm, smooth tone for leads and jazz applications",
                            "both": "Balanced tone with enhanced midrange presence"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Solid Body",
                        "hardware_quality": "Standard",
                        "finish_quality": "Professional polyester finish with good attention to detail",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "neck_profile": "Comfortable rounded profile with good playability",
                        "action_setup": "Medium action potential with good setup from factory",
                        "comfort_rating": "8/10 - Good ergonomics with substantial feel",
                        "weight_category": "Medium to Heavy"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Authentic Les Paul Tone",
                            "description": "Delivers the classic Les Paul sound and feel at an accessible price point."
                        },
                        {
                            "title": "Excellent Value",
                            "description": "Genuine Epiphone quality with modern improvements at a fraction of Gibson cost."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Substantial Weight",
                            "description": "Traditional Les Paul weight may be uncomfortable for some players."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Rock and blues players seeking Les Paul tone",
                            "reason": "Provides authentic Les Paul experience at an accessible price"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Players requiring lightweight instruments",
                            "reason": "Substantial weight may not suit players who prefer lighter instruments"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Tube amplifiers", "High-gain amplifiers", "Clean amplifiers with pedals"],
                    "suitable_music_styles": {
                        "excellent": ["Rock", "Blues", "Hard Rock", "Jazz"],
                        "good": ["Country", "Alternative Rock"],
                        "limited": ["Funk", "Light acoustic-style playing"]
                    },
                    "skill_development": {
                        "learning_curve": "Moderate",
                        "growth_potential": "Excellent for developing understanding of Les Paul characteristics and rock techniques"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Neck relief adjustment", "Bridge height adjustment", "Nut slot maintenance"],
                    "care_instructions": {
                        "daily": "Wipe down strings and body after playing",
                        "weekly": "Clean fingerboard, check tuning stability",
                        "monthly": "Deep clean, check intonation",
                        "annual": "Professional setup and inspection"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["Pickup replacement", "Bridge upgrade", "Tuner improvement"],
                        "recommended_budget": "€150-400 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8", 
                        "value_for_money": "9",
                        "versatility": "8"
                    },
                    "standout_features": ["Authentic Les Paul tone", "Excellent value", "Good build quality"],
                    "notable_limitations": ["Substantial weight", "Basic hardware"],
                    "competitive_position": "Strong value offering in the €550-650 range, providing authentic Les Paul experience at an accessible price"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Epiphone Les Paul Standard", "Les Paul guitar", "Epiphone guitar", "rock guitar", "Les Paul tone"],
                    "readability_score": "Medium",
                    "word_count": "550"
                }
            }
        },
        {
            "product_input": {
                "sku": "YAMAHA-FG800",
                "name": "Yamaha FG800 Acoustic Guitar",
                "slug": "yamaha-fg800-acoustic-guitar",
                "brand": "Yamaha",
                "category": "acoustic-guitars",
                "description": "The Yamaha FG800 is a classic dreadnought acoustic guitar that delivers exceptional value and quality for beginners and developing players.",
                "specifications": {
                    "body_material": "Solid Spruce Top, Nato Back/Sides",
                    "neck_material": "Nato",
                    "fingerboard": "Rosewood",
                    "scale_length": "25.6 inches",
                    "frets": 20,
                    "bridge": "Rosewood",
                    "tuners": "Die-cast Chrome",
                    "body_shape": "Dreadnought",
                    "finish": "Natural"
                },
                "msrp_price": 199,
                "images": ["yamaha_fg800_1.jpg", "yamaha_fg800_2.jpg", "yamaha_fg800_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Yamaha FG800 represents exceptional value in acoustic guitars, delivering solid spruce top tone and reliable construction at an accessible price point. Perfect for beginners and developing players.",
                    "key_features": ["Solid spruce top", "Classic dreadnought body", "Reliable construction", "Excellent value"],
                    "target_skill_level": "Beginner to Intermediate",
                    "country_of_origin": "China",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Bright, clear tones with good projection and balanced frequency response",
                        "output_level": "Medium",
                        "best_genres": ["Folk", "Country", "Pop", "Practice", "Learning"],
                        "playing_styles": {
                            "strumming": "Good projection and balanced sound for strumming",
                            "fingerpicking": "Clear note separation with good articulation",
                            "flatpicking": "Bright, cutting tone suitable for flatpicking styles"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Acoustic",
                        "hardware_quality": "Standard",
                        "finish_quality": "Natural finish with good attention to detail",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "neck_profile": "Comfortable neck profile suitable for beginners",
                        "action_setup": "Medium action with good setup from factory",
                        "comfort_rating": "8/10 - Good ergonomics for learning and practice",
                        "weight_category": "Medium - typical dreadnought weight"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Exceptional Value",
                            "description": "Delivers solid spruce top tone and reliable construction at an accessible price point."
                        },
                        {
                            "title": "Perfect for Learning",
                            "description": "Reliable construction and good playability make it ideal for beginners and developing players."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Basic Features",
                            "description": "Simple design may not satisfy advanced players requiring premium features."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Beginners and developing players",
                            "reason": "Provides excellent value and reliability for learning acoustic guitar"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Advanced players requiring premium features",
                            "reason": "Basic design and features may not satisfy experienced players"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Acoustic amplifiers", "PA systems"],
                    "suitable_music_styles": {
                        "excellent": ["Folk", "Country", "Pop", "Practice"],
                        "good": ["Jazz", "Blues", "Learning"],
                        "limited": ["Large venue performance", "Professional recording"]
                    },
                    "skill_development": {
                        "learning_curve": "Low",
                        "growth_potential": "Excellent for developing fundamental acoustic guitar skills"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Humidity control", "String changes", "Neck adjustment"],
                    "care_instructions": {
                        "daily": "Wipe down after playing, store in case",
                        "weekly": "Clean body and strings, check humidity",
                        "monthly": "Deep clean, condition fingerboard if needed",
                        "annual": "Professional setup and inspection"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["String upgrades", "Tuner improvement", "Case upgrade"],
                        "recommended_budget": "€50-150 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7", 
                        "value_for_money": "10",
                        "versatility": "7"
                    },
                    "standout_features": ["Excellent value", "Reliable construction", "Good for learning"],
                    "notable_limitations": ["Basic features", "Limited premium tone"],
                    "competitive_position": "Outstanding value leader in the €180-220 range, offering features that typically cost much more"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Yamaha FG800", "acoustic guitar", "beginner guitar", "dreadnought guitar", "Yamaha acoustic"],
                    "readability_score": "Medium",
                    "word_count": "500"
                }
            }
        },
        {
            "product_input": {
                "sku": "SEAGULL-S6-ORIGINAL",
                "name": "Seagull S6 Original Acoustic Guitar",
                "slug": "seagull-s6-original-acoustic-guitar",
                "brand": "Seagull",
                "category": "acoustic-guitars",
                "description": "The Seagull S6 Original is a handcrafted acoustic guitar that delivers exceptional tone and playability with Canadian craftsmanship and attention to detail.",
                "specifications": {
                    "body_material": "Solid Cedar Top, Wild Cherry Back/Sides",
                    "neck_material": "Silver Leaf Maple",
                    "fingerboard": "Rosewood",
                    "scale_length": "24.84 inches",
                    "frets": 21,
                    "bridge": "Rosewood",
                    "tuners": "Seagull Chrome",
                    "body_shape": "Folk",
                    "finish": "Natural"
                },
                "msrp_price": 399,
                "images": ["seagull_s6_original_1.jpg", "seagull_s6_original_2.jpg", "seagull_s6_original_3.jpg"]
            },
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Seagull S6 Original represents exceptional value in handcrafted acoustic guitars, delivering solid cedar top tone and Canadian craftsmanship at an accessible price point.",
                    "key_features": ["Solid cedar top", "Handcrafted in Canada", "Wild cherry back and sides", "Silver leaf maple neck"],
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Canada",
                    "release_year": "Current Production"
                },
                "technical_analysis": {
                    "sound_characteristics": {
                        "tonal_profile": "Warm, rich tones with excellent clarity and balanced frequency response",
                        "output_level": "Medium to High",
                        "best_genres": ["Folk", "Singer-Songwriter", "Jazz", "Fingerpicking"],
                        "playing_styles": {
                            "fingerpicking": "Excellent clarity and separation between strings",
                            "strumming": "Rich, full-bodied sound with good projection",
                            "flatpicking": "Clear, articulate tone with good note definition"
                        }
                    },
                    "build_quality": {
                        "construction_type": "Acoustic",
                        "hardware_quality": "Standard",
                        "finish_quality": "Natural finish with excellent attention to detail",
                        "expected_durability": "Good"
                    },
                    "playability": {
                        "neck_profile": "Comfortable neck profile with good playability",
                        "action_setup": "Low action potential with excellent setup from factory",
                        "comfort_rating": "9/10 - Excellent ergonomics and comfortable playing feel",
                        "weight_category": "Light to Medium"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Handcrafted Canadian Quality",
                            "description": "Delivers exceptional craftsmanship and attention to detail from Canadian luthiers."
                        },
                        {
                            "title": "Excellent Tone and Playability",
                            "description": "Solid cedar top and comfortable neck provide excellent tone and playability."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited Body Size Options",
                            "description": "Folk body size may not suit players requiring larger dreadnought projection."
                        }
                    ],
                    "best_for": [
                        {
                            "user_type": "Fingerpickers and singer-songwriters",
                            "reason": "Provides excellent tone and playability for intimate playing styles"
                        }
                    ],
                    "not_ideal_for": [
                        {
                            "user_type": "Players requiring large dreadnought projection",
                            "reason": "Folk body size may not provide the same projection as larger dreadnought guitars"
                        }
                    ]
                },
                "usage_guidance": {
                    "recommended_amplifiers": ["Acoustic amplifiers", "PA systems", "Direct recording"],
                    "suitable_music_styles": {
                        "excellent": ["Folk", "Singer-Songwriter", "Jazz", "Fingerpicking"],
                        "good": ["Country", "Blues", "Pop"],
                        "limited": ["Heavy strumming", "Large venue performance"]
                    },
                    "skill_development": {
                        "learning_curve": "Low to Moderate",
                        "growth_potential": "Excellent for developing fingerpicking and acoustic techniques"
                    }
                },
                "maintenance_care": {
                    "maintenance_level": "Medium",
                    "common_issues": ["Humidity control", "String changes", "Neck adjustment"],
                    "care_instructions": {
                        "daily": "Wipe down after playing, store in case",
                        "weekly": "Clean body and strings, check humidity",
                        "monthly": "Deep clean, condition fingerboard if needed",
                        "annual": "Professional setup and inspection"
                    },
                    "upgrade_potential": {
                        "easy_upgrades": ["String upgrades", "Tuner improvement", "Case upgrade"],
                        "recommended_budget": "€100-250 for meaningful improvements"
                    }
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8", 
                        "value_for_money": "9",
                        "versatility": "8"
                    },
                    "standout_features": ["Handcrafted quality", "Excellent tone", "Good playability"],
                    "notable_limitations": ["Folk body size", "Limited projection"],
                    "competitive_position": "Strong value offering in the €350-450 range, providing handcrafted quality that exceeds expectations at this price point"
                },
                "content_metadata": {
                    "generated_date": "2024-01-15T10:30:00Z",
                    "content_version": "1.0",
                    "seo_keywords": ["Seagull S6 Original", "acoustic guitar", "Canadian guitar", "folk guitar", "cedar top guitar"],
                    "readability_score": "Medium",
                    "word_count": "550"
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
