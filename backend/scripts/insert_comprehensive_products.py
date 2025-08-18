#!/usr/bin/env python3
"""
Script to insert comprehensive product dataset with AI-generated content into the database.
This script creates products across all 9 categories with detailed AI content.
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

async def get_session():
    """Create database session."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Complete product dataset with AI content
PRODUCTS_DATA = {
    "electric-guitars": [
        {
            "sku": "FENDER-PLAYER-STRAT-SSS",
            "name": "Fender Player Stratocaster MIM",
            "slug": "fender-player-stratocaster-mim",
            "brand": "Fender",
            "description": "The Player Stratocaster takes the best elements of the 60+ year-old Strat design and updates them for today's players.",
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
            "images": ["fender_player_strat_1.jpg", "fender_player_strat_2.jpg", "fender_player_strat_3.jpg"],
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
                        "finish_quality": "Professional polyester finish with good attention to detail and consistent application",
                        "expected_durability": "High"
                    },
                    "playability": {
                        "neck_profile": "Modern 'C' shape offers comfortable grip for most hand sizes with smooth playing feel",
                        "action_setup": "Medium action potential with good setup from factory",
                        "comfort_rating": "8/10 - Excellent ergonomics with well-balanced weight distribution",
                        "weight_category": "Medium with approximately 3.2-3.6 kg"
                    }
                },
                "purchase_decision": {
                    "why_buy": [
                        {
                            "title": "Authentic Fender Quality at Mid-Tier Price",
                            "description": "Genuine Fender craftsmanship from the Corona factory with quality control standards that ensure consistent playability and tone across instruments."
                        },
                        {
                            "title": "Exceptional Versatility Across Genres",
                            "description": "The five-way pickup selector and balanced pickup outputs make this guitar suitable for everything from clean jazz to high-gain rock, making it ideal for players exploring different styles."
                        }
                    ],
                    "why_not_buy": [
                        {
                            "title": "Limited High-Output Capability",
                            "description": "Single-coil pickups may not provide enough output for metal or very high-gain applications without additional pedals or amp modifications."
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
            "sku": "GIBSON-LP-STUDIO-EB",
            "name": "Gibson Les Paul Studio Ebony",
            "slug": "gibson-les-paul-studio-ebony",
            "brand": "Gibson",
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
            "images": ["gibson_lp_studio_1.jpg", "gibson_lp_studio_2.jpg", "gibson_lp_studio_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Gibson Les Paul Studio delivers authentic American-made Les Paul tone with classic mahogany/maple construction and powerful humbucking pickups. This model strips away cosmetic extras to focus on pure sonic performance and playability.",
                    "key_features": ["490R/498T humbucking pickups", "Mahogany body with maple cap", "Nitrocellulose lacquer finish", "Grover Rotomatic tuners"],
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "United States",
                    "release_year": "Current Production"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "9",
                        "sound_quality": "9",
                        "value_for_money": "7",
                        "versatility": "7"
                    }
                }
            }
        },
        {
            "sku": "PRS-SE-CUSTOM-24",
            "name": "PRS SE Custom 24",
            "slug": "prs-se-custom-24",
            "brand": "PRS",
            "description": "The PRS SE Custom 24 offers PRS design excellence and versatility with 85/15 S pickups and a wide thin neck profile.",
            "specifications": {
                "body_material": "Mahogany",
                "neck_material": "Maple",
                "fingerboard": "Rosewood",
                "pickups": "2x 85/15 S Humbucking",
                "scale_length": "25 inches",
                "frets": 24,
                "bridge": "PRS Tremolo",
                "tuners": "PRS Designed",
                "nut_width": "1.685 inches",
                "finish": "Gloss Polyurethane",
                "inlays": "Bird"
            },
            "msrp_price": 829,
            "images": ["prs_se_custom24_1.jpg", "prs_se_custom24_2.jpg", "prs_se_custom24_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The PRS SE Custom 24 bridges the gap between Fender and Gibson designs, offering versatile tones from crystalline cleans to aggressive overdrive. The 24-fret neck and coil-tap capability make it exceptionally adaptable for modern players.",
                    "key_features": ["85/15 S humbucking pickups with coil-tap", "24-fret wide thin neck", "PRS tremolo bridge", "Iconic bird inlays"],
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "South Korea",
                    "release_year": "Current Production"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8",
                        "value_for_money": "9",
                        "versatility": "10"
                    }
                }
            }
        }
    ],
    "acoustic-guitars": [
        {
            "sku": "MARTIN-D-28-STANDARD",
            "name": "Martin D-28 Standard",
            "slug": "martin-d-28-standard",
            "brand": "Martin",
            "description": "The Martin D-28 is the most famous dreadnought acoustic guitar, offering legendary tone with East Indian rosewood back and sides.",
            "specifications": {
                "top_material": "Solid Sitka Spruce",
                "back_sides": "East Indian Rosewood",
                "neck_material": "Select Hardwood",
                "fingerboard": "East Indian Rosewood",
                "bridge": "East Indian Rosewood",
                "scale_length": "25.4 inches",
                "nut_width": "1.75 inches",
                "frets": 20,
                "bracing": "Forward-Shifted X-Bracing",
                "finish": "Gloss",
                "tuners": "Nickel Open-Gear"
            },
            "msrp_price": 3199,
            "images": ["martin_d28_1.jpg", "martin_d28_2.jpg", "martin_d28_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Martin D-28 Standard represents the pinnacle of American acoustic guitar craftsmanship, delivering the legendary dreadnought tone that has defined country, folk, and rock music for generations.",
                    "target_skill_level": "Professional",
                    "country_of_origin": "United States"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "10",
                        "sound_quality": "10",
                        "value_for_money": "7",
                        "versatility": "8"
                    }
                }
            }
        },
        {
            "sku": "YAMAHA-FG830-NAT",
            "name": "Yamaha FG830 Natural",
            "slug": "yamaha-fg830-natural",
            "brand": "Yamaha",
            "description": "The Yamaha FG830 offers remarkable value with its solid spruce top and traditional dreadnought construction.",
            "specifications": {
                "top_material": "Solid Sitka Spruce",
                "back_sides": "Rosewood",
                "neck_material": "Nato",
                "fingerboard": "Rosewood",
                "bridge": "Rosewood",
                "scale_length": "25 inches",
                "nut_width": "1.69 inches",
                "frets": 20,
                "bracing": "Scalloped X-bracing",
                "finish": "Natural Gloss",
                "tuners": "Die-cast Chrome"
            },
            "msrp_price": 299,
            "images": ["yamaha_fg830_1.jpg", "yamaha_fg830_2.jpg", "yamaha_fg830_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Yamaha FG830 offers remarkable value with its solid spruce top and traditional dreadnought construction. This guitar delivers professional-level tone and playability at an entry-to-intermediate price point.",
                    "target_skill_level": "Beginner",
                    "country_of_origin": "China"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7",
                        "value_for_money": "9",
                        "versatility": "8"
                    }
                }
            }
        },
        {
            "sku": "TAYLOR-114CE-WALNUT",
            "name": "Taylor 114ce Walnut",
            "slug": "taylor-114ce-walnut",
            "brand": "Taylor",
            "description": "The Taylor 114ce combines Taylor's renowned playability with walnut back and sides and ES2 electronics.",
            "specifications": {
                "top_material": "Solid Sitka Spruce",
                "back_sides": "Layered Walnut",
                "neck_material": "Tropical Mahogany",
                "fingerboard": "West African Ebony",
                "bridge": "West African Ebony",
                "scale_length": "25.5 inches",
                "nut_width": "1.6875 inches",
                "frets": 20,
                "bracing": "X-Class Bracing",
                "finish": "Gloss",
                "tuners": "Nickel",
                "electronics": "ES2"
            },
            "msrp_price": 899,
            "images": ["taylor_114ce_1.jpg", "taylor_114ce_2.jpg", "taylor_114ce_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Taylor 114ce Walnut offers Taylor's signature playability and innovative design at an accessible price point. Featuring solid spruce top, layered walnut back/sides, and ES2 electronics.",
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Mexico"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "7",
                        "value_for_money": "8",
                        "versatility": "9"
                    }
                }
            }
        }
    ],
    "digital-keyboards": [
        {
            "sku": "ROLAND-FP30X-BK",
            "name": "Roland FP-30X Digital Piano",
            "slug": "roland-fp-30x-digital-piano",
            "brand": "Roland",
            "description": "The Roland FP-30X combines authentic piano feel with modern digital convenience in a portable package.",
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
            "images": ["roland_fp30x_1.jpg", "roland_fp30x_2.jpg", "roland_fp30x_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "The Roland FP-30X combines authentic piano feel with modern digital convenience in a portable package. Featuring Roland's acclaimed PHA-4 keyboard action and SuperNATURAL sound engine.",
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Malaysia"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "9",
                        "sound_quality": "8",
                        "value_for_money": "8",
                        "versatility": "7"
                    }
                }
            }
        },
        {
            "sku": "CASIO-PX-S1100-BK",
            "name": "Casio PX-S1100 Privia",
            "slug": "casio-px-s1100-privia",
            "brand": "Casio",
            "description": "Ultra-slim 88-key digital piano with Smart Scaled Hammer Action and comprehensive connectivity.",
            "specifications": {
                "keys": 88,
                "key_action": "Smart Scaled Hammer Action",
                "sound_engine": "AiR Sound Source",
                "polyphony": 192,
                "voices": 18,
                "built_in_songs": 60,
                "connectivity": "USB, Bluetooth, Audio Input, Sustain Pedal",
                "speakers": "2 x 8W",
                "dimensions": "1322 x 232 x 102 mm",
                "weight": "11.2 kg"
            },
            "msrp_price": 599,
            "images": ["casio_px_s1100_1.jpg", "casio_px_s1100_2.jpg", "casio_px_s1100_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Ultra-slim 88-key digital piano with Smart Scaled Hammer Action and comprehensive connectivity, offering excellent value for home and stage use.",
                    "target_skill_level": "Beginner",
                    "country_of_origin": "China"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7",
                        "value_for_money": "9",
                        "versatility": "8"
                    }
                }
            }
        },
        {
            "sku": "YAMAHA-P125A-BK",
            "name": "Yamaha P-125a Digital Piano",
            "slug": "yamaha-p-125a-digital-piano",
            "brand": "Yamaha",
            "description": "Compact and portable digital piano with GHS weighted action and high-quality Yamaha sound.",
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
            "images": ["yamaha_p125a_1.jpg", "yamaha_p125a_2.jpg", "yamaha_p125a_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Compact and portable digital piano with GHS weighted action and high-quality Yamaha sound, perfect for students and home players.",
                    "target_skill_level": "Beginner",
                    "country_of_origin": "Indonesia"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8",
                        "value_for_money": "8",
                        "versatility": "7"
                    }
                }
            }
        }
    ],
    "amplifiers": [
        {
            "sku": "FENDER-MUSTANG-LT25",
            "name": "Fender Mustang LT25",
            "slug": "fender-mustang-lt25",
            "brand": "Fender",
            "description": "25-watt modeling amplifier with multiple amp models and effects for home practice and small venues.",
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
            "images": ["fender_mustang_lt25_1.jpg", "fender_mustang_lt25_2.jpg", "fender_mustang_lt25_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "25-watt modeling amplifier with multiple amp models and effects for home practice and small venues. Easy-to-use interface with extensive tonal possibilities.",
                    "target_skill_level": "Beginner",
                    "country_of_origin": "China"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7",
                        "value_for_money": "9",
                        "versatility": "9"
                    }
                }
            }
        },
        {
            "sku": "MARSHALL-DSL20CR",
            "name": "Marshall DSL20CR Combo",
            "slug": "marshall-dsl20cr-combo",
            "brand": "Marshall",
            "description": "20-watt all-tube combo amplifier with classic Marshall tone and modern features.",
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
            "images": ["marshall_dsl20cr_1.jpg", "marshall_dsl20cr_2.jpg", "marshall_dsl20cr_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "20-watt all-tube combo amplifier with classic Marshall tone and modern features. Perfect balance of power and portability for studio and stage use.",
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Vietnam"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "9",
                        "value_for_money": "8",
                        "versatility": "7"
                    }
                }
            }
        },
        {
            "sku": "VOX-AC15C1-TBX",
            "name": "Vox AC15C1 Tube Combo",
            "slug": "vox-ac15c1-tube-combo",
            "brand": "Vox",
            "description": "15-watt tube combo amplifier with classic Vox chime and built-in reverb and tremolo.",
            "specifications": {
                "power": "15 watts",
                "tubes": "3 x ECC83, 2 x EL84",
                "speaker": "12-inch Celestion Greenback",
                "channels": 2,
                "effects": "Reverb, Tremolo",
                "connectivity": "External speaker out, Effects loop",
                "controls": "Volume, Treble, Bass per channel, Reverb, Speed, Depth",
                "dimensions": "590 x 445 x 260 mm",
                "weight": "23.2 kg"
            },
            "msrp_price": 899,
            "images": ["vox_ac15c1_1.jpg", "vox_ac15c1_2.jpg", "vox_ac15c1_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "15-watt tube combo amplifier with classic Vox chime and built-in reverb and tremolo. Delivers the legendary AC30 tone in a more manageable package.",
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "China"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "9",
                        "value_for_money": "7",
                        "versatility": "6"
                    }
                }
            }
        }
    ],
    "bass-guitars": [
        {
            "sku": "FENDER-PLAYER-P-BASS",
            "name": "Fender Player Precision Bass",
            "slug": "fender-player-precision-bass",
            "brand": "Fender",
            "description": "Classic Precision Bass with split-coil pickup and modern playability improvements.",
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
            "images": ["fender_player_pbass_1.jpg", "fender_player_pbass_2.jpg", "fender_player_pbass_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Classic Precision Bass with split-coil pickup and modern playability improvements. The foundation of countless recordings across all genres.",
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Mexico"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "9",
                        "value_for_money": "8",
                        "versatility": "7"
                    }
                }
            }
        },
        {
            "sku": "MUSICMAN-STINGRAY-4",
            "name": "Music Man StingRay 4",
            "slug": "music-man-stingray-4",
            "brand": "Music Man",
            "description": "Iconic 4-string bass with powerful humbucker pickup and 3-band EQ.",
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
            "images": ["musicman_stingray_1.jpg", "musicman_stingray_2.jpg", "musicman_stingray_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Iconic 4-string bass with powerful humbucker pickup and 3-band EQ. The definitive modern bass sound used by countless professionals.",
                    "target_skill_level": "Professional",
                    "country_of_origin": "United States"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "9",
                        "sound_quality": "9",
                        "value_for_money": "7",
                        "versatility": "8"
                    }
                }
            }
        },
        {
            "sku": "IBANEZ-SR500E-BM",
            "name": "Ibanez SR500E Brown Mahogany",
            "slug": "ibanez-sr500e-brown-mahogany",
            "brand": "Ibanez",
            "description": "Versatile 4-string bass with dual humbuckers and active electronics.",
            "specifications": {
                "body_material": "Mahogany",
                "neck_material": "Jatoba/Walnut",
                "fingerboard": "Jatoba",
                "pickups": "2x PowerSpan Dual Coil",
                "scale_length": "34 inches",
                "frets": 24,
                "bridge": "Accu-cast B305",
                "tuners": "Die-cast",
                "preamp": "Ibanez Custom Electronics 3-band EQ",
                "strings": 4
            },
            "msrp_price": 649,
            "images": ["ibanez_sr500e_1.jpg", "ibanez_sr500e_2.jpg", "ibanez_sr500e_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Versatile 4-string bass with dual humbuckers and active electronics. Modern design with excellent playability and tonal flexibility.",
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Indonesia"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8",
                        "value_for_money": "9",
                        "versatility": "9"
                    }
                }
            }
        }
    ],
    "drums-percussion": [
        {
            "sku": "PEARL-EXPORT-EXX725S",
            "name": "Pearl Export EXX 5-Piece Kit",
            "slug": "pearl-export-exx-5-piece-kit",
            "brand": "Pearl",
            "description": "Complete 5-piece drum kit with hardware and cymbals, perfect for beginners and intermediate players.",
            "specifications": {
                "configuration": "5-piece",
                "shell_material": "Poplar/Asian Mahogany",
                "sizes": "22x18 BD, 10x7 TT, 12x8 TT, 16x14 FT, 14x5.5 SD",
                "hardware": "830 Series",
                "cymbals": "Sabian SBR Series",
                "finish": "Smokey Chrome",
                "lugs": "Super-Sonic Lugs",
                "hoops": "Triple-flanged steel"
            },
            "msrp_price": 899,
            "images": ["pearl_export_1.jpg", "pearl_export_2.jpg", "pearl_export_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Complete 5-piece drum kit with hardware and cymbals, perfect for beginners and intermediate players. Excellent value with professional features.",
                    "target_skill_level": "Beginner",
                    "country_of_origin": "China"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7",
                        "value_for_money": "9",
                        "versatility": "8"
                    }
                }
            }
        },
        {
            "sku": "ROLAND-TD-17KVX-V-DRUMS",
            "name": "Roland TD-17KVX V-Drums",
            "slug": "roland-td-17kvx-v-drums",
            "brand": "Roland",
            "description": "Electronic drum kit with mesh heads and advanced sound module for realistic playing experience.",
            "specifications": {
                "configuration": "5-piece electronic",
                "sound_module": "TD-17",
                "pads": "Mesh head snare and toms",
                "cymbals": "CY-12C, CY-13R, CY-5",
                "kick": "KD-10 Kick Pad",
                "hi_hat": "VH-10 V-Hi-Hat",
                "voices": 310,
                "kits": 50,
                "connectivity": "USB, MIDI, Audio"
            },
            "msrp_price": 1699,
            "images": ["roland_td17kvx_1.jpg", "roland_td17kvx_2.jpg", "roland_td17kvx_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Electronic drum kit with mesh heads and advanced sound module for realistic playing experience. Perfect for practice and recording.",
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "Malaysia"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "9",
                        "sound_quality": "8",
                        "value_for_money": "7",
                        "versatility": "9"
                    }
                }
            }
        },
        {
            "sku": "DW-PERFORMANCE-SERIES",
            "name": "DW Performance Series 4-Piece Kit",
            "slug": "dw-performance-series-4-piece-kit",
            "brand": "DW",
            "description": "Professional-grade drum kit with maple shells and DW's renowned craftsmanship.",
            "specifications": {
                "configuration": "4-piece",
                "shell_material": "Maple",
                "sizes": "22x18 BD, 12x9 TT, 16x14 FT, 14x6.5 SD",
                "hardware": "DW 9000 Series",
                "finish": "Lacquer Specialty",
                "lugs": "STM (Suspension Tom Mount)",
                "hoops": "True-Pitch 50",
                "bearing_edges": "45-degree"
            },
            "msrp_price": 2199,
            "images": ["dw_performance_1.jpg", "dw_performance_2.jpg", "dw_performance_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Professional-grade drum kit with maple shells and DW's renowned craftsmanship. Studio and stage ready with superior build quality.",
                    "target_skill_level": "Professional",
                    "country_of_origin": "United States"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "10",
                        "sound_quality": "9",
                        "value_for_money": "6",
                        "versatility": "7"
                    }
                }
            }
        }
    ],
    "effects-pedals": [
        {
            "sku": "BOSS-DS-1-DISTORTION",
            "name": "Boss DS-1 Distortion",
            "slug": "boss-ds-1-distortion",
            "brand": "Boss",
            "description": "Classic distortion pedal used by countless guitarists for over 40 years.",
            "specifications": {
                "effect_type": "Distortion",
                "controls": "Level, Tone, Distortion",
                "input_impedance": "1 MΩ",
                "output_impedance": "1 kΩ",
                "power": "9V DC",
                "current_draw": "4 mA",
                "dimensions": "70 x 125 x 59 mm",
                "weight": "400g",
                "bypass": "Buffered"
            },
            "msrp_price": 69,
            "images": ["boss_ds1_1.jpg", "boss_ds1_2.jpg", "boss_ds1_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Classic distortion pedal used by countless guitarists for over 40 years. Simple, reliable, and versatile with that iconic orange sound.",
                    "target_skill_level": "Beginner",
                    "country_of_origin": "Taiwan"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "7",
                        "value_for_money": "10",
                        "versatility": "8"
                    }
                }
            }
        },
        {
            "sku": "STRYMON-TIMELINE-DELAY",
            "name": "Strymon Timeline Delay",
            "slug": "strymon-timeline-delay",
            "brand": "Strymon",
            "description": "Premium digital delay pedal with 12 delay machines and extensive tweaking capabilities.",
            "specifications": {
                "effect_type": "Digital Delay",
                "delay_time": "30 seconds maximum",
                "machines": 12,
                "presets": 200,
                "controls": "Value, Repeats, Mix, Filter, Speed, Depth",
                "connectivity": "Expression pedal, MIDI",
                "power": "9V DC (300mA)",
                "dimensions": "145 x 122 x 57 mm",
                "bypass": "True Bypass or Buffered"
            },
            "msrp_price": 449,
            "images": ["strymon_timeline_1.jpg", "strymon_timeline_2.jpg", "strymon_timeline_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Premium digital delay pedal with 12 delay machines and extensive tweaking capabilities. The ultimate delay pedal for professionals.",
                    "target_skill_level": "Professional",
                    "country_of_origin": "United States"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "10",
                        "sound_quality": "10",
                        "value_for_money": "7",
                        "versatility": "10"
                    }
                }
            }
        },
        {
            "sku": "ELECTRO-HARMONIX-BIG-MUFF",
            "name": "Electro-Harmonix Big Muff Pi",
            "slug": "electro-harmonix-big-muff-pi",
            "brand": "Electro-Harmonix",
            "description": "Iconic fuzz pedal that has defined the sound of countless rock and alternative recordings.",
            "specifications": {
                "effect_type": "Fuzz",
                "controls": "Volume, Tone, Sustain",
                "input_impedance": "100 kΩ",
                "output_impedance": "Less than 10 kΩ",
                "power": "9V DC",
                "current_draw": "3 mA",
                "dimensions": "115 x 70 x 54 mm",
                "weight": "340g",
                "bypass": "True Bypass"
            },
            "msrp_price": 89,
            "images": ["ehx_bigmuff_1.jpg", "ehx_bigmuff_2.jpg", "ehx_bigmuff_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Iconic fuzz pedal that has defined the sound of countless rock and alternative recordings. Legendary sustain and character.",
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "United States"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "9",
                        "value_for_money": "9",
                        "versatility": "6"
                    }
                }
            }
        }
    ],
    "dj-equipment": [
        {
            "sku": "PIONEER-DDJ-FLX4",
            "name": "Pioneer DDJ-FLX4 DJ Controller",
            "slug": "pioneer-ddj-flx4-dj-controller",
            "brand": "Pioneer",
            "description": "Entry-level 2-channel DJ controller compatible with multiple DJ software platforms.",
            "specifications": {
                "channels": 2,
                "software": "Serato DJ Lite, rekordbox",
                "jog_wheels": "Touch-sensitive",
                "pads": "8 per deck",
                "faders": "60mm channel, 60mm crossfader",
                "connectivity": "USB-C",
                "dimensions": "482 x 272 x 58 mm",
                "weight": "2.1 kg",
                "power": "USB Bus Power"
            },
            "msrp_price": 199,
            "images": ["pioneer_ddj_flx4_1.jpg", "pioneer_ddj_flx4_2.jpg", "pioneer_ddj_flx4_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Entry-level 2-channel DJ controller compatible with multiple DJ software platforms. Perfect introduction to digital DJing with professional features.",
                    "target_skill_level": "Beginner",
                    "country_of_origin": "China"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "7",
                        "sound_quality": "7",
                        "value_for_money": "9",
                        "versatility": "8"
                    }
                }
            }
        },
        {
            "sku": "TECHNICS-SL-1200MK7",
            "name": "Technics SL-1200MK7 Turntable",
            "slug": "technics-sl-1200mk7-turntable",
            "brand": "Technics",
            "description": "Professional direct-drive turntable with improved motor and updated features for modern DJs.",
            "specifications": {
                "drive_type": "Direct Drive",
                "motor": "Coreless direct-drive motor",
                "torque": "4.5 kg⋅cm",
                "speeds": "33⅓ and 45 RPM",
                "pitch_control": "±8%, ±16%, ±50%",
                "wow_flutter": "0.01% WRMS",
                "connectivity": "RCA, USB",
                "dimensions": "453 x 353 x 169 mm",
                "weight": "18.8 kg"
            },
            "msrp_price": 1199,
            "images": ["technics_sl1200mk7_1.jpg", "technics_sl1200mk7_2.jpg", "technics_sl1200mk7_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Professional direct-drive turntable with improved motor and updated features for modern DJs. The legendary SL-1200 continues its legacy.",
                    "target_skill_level": "Professional",
                    "country_of_origin": "Malaysia"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "10",
                        "sound_quality": "9",
                        "value_for_money": "7",
                        "versatility": "7"
                    }
                }
            }
        },
        {
            "sku": "NATIVE-TRAKTOR-S4-MK3",
            "name": "Native Instruments Traktor Kontrol S4 MK3",
            "slug": "native-instruments-traktor-kontrol-s4-mk3",
            "brand": "Native Instruments",
            "description": "Professional 4-channel DJ controller with haptic drive jog wheels and premium build quality.",
            "specifications": {
                "channels": 4,
                "software": "Traktor Pro 3",
                "jog_wheels": "Haptic Drive with motorized resistance",
                "mixer": "4-channel with 3-band EQ and filters",
                "displays": "4 high-resolution color screens",
                "connectivity": "USB, Master/Booth outputs, Mic input",
                "dimensions": "651 x 370 x 77 mm",
                "weight": "7.8 kg",
                "audio_interface": "24-bit/96kHz"
            },
            "msrp_price": 999,
            "images": ["ni_traktor_s4_mk3_1.jpg", "ni_traktor_s4_mk3_2.jpg", "ni_traktor_s4_mk3_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Professional 4-channel DJ controller with haptic drive jog wheels and premium build quality. Advanced features for serious DJs and producers.",
                    "target_skill_level": "Professional",
                    "country_of_origin": "China"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "9",
                        "sound_quality": "9",
                        "value_for_money": "8",
                        "versatility": "9"
                    }
                }
            }
        }
    ],
    "studio-and-recording-equipment": [
        {
            "sku": "FOCUSRITE-SCARLETT-2I2-4TH",
            "name": "Focusrite Scarlett 2i2 4th Gen",
            "slug": "focusrite-scarlett-2i2-4th-gen",
            "brand": "Focusrite",
            "description": "Professional 2-input USB audio interface with high-quality preamps and 24-bit/192kHz recording.",
            "specifications": {
                "inputs": "2 x Combo XLR/TRS",
                "outputs": "2 x TRS (balanced)",
                "preamps": "4th Gen Scarlett preamps",
                "sample_rate": "Up to 192 kHz",
                "bit_depth": "24-bit",
                "connectivity": "USB-C",
                "phantom_power": "48V",
                "direct_monitoring": "Yes",
                "dimensions": "107 x 110 x 52 mm",
                "weight": "0.7 kg"
            },
            "msrp_price": 199,
            "images": ["focusrite_2i2_4th_1.jpg", "focusrite_2i2_4th_2.jpg", "focusrite_2i2_4th_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Professional 2-input USB audio interface with high-quality preamps and 24-bit/192kHz recording. The world's most popular home studio interface.",
                    "target_skill_level": "Beginner",
                    "country_of_origin": "China"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8",
                        "value_for_money": "9",
                        "versatility": "7"
                    }
                }
            }
        },
        {
            "sku": "SHURE-SM57-LC",
            "name": "Shure SM57 Dynamic Microphone",
            "slug": "shure-sm57-dynamic-microphone",
            "brand": "Shure",
            "description": "Industry-standard dynamic microphone for instruments and vocals, used in studios and live venues worldwide.",
            "specifications": {
                "type": "Dynamic",
                "polar_pattern": "Cardioid",
                "frequency_response": "40 Hz to 15 kHz",
                "sensitivity": "-56 dBV/Pa",
                "impedance": "310 Ω",
                "connector": "XLR",
                "dimensions": "157 x 32 mm",
                "weight": "284g",
                "max_spl": "140 dB"
            },
            "msrp_price": 109,
            "images": ["shure_sm57_1.jpg", "shure_sm57_2.jpg", "shure_sm57_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Industry-standard dynamic microphone for instruments and vocals, used in studios and live venues worldwide. The most recorded microphone in history.",
                    "target_skill_level": "Professional",
                    "country_of_origin": "Mexico"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "10",
                        "sound_quality": "8",
                        "value_for_money": "10",
                        "versatility": "9"
                    }
                }
            }
        },
        {
            "sku": "KRK-ROKIT-RP5-G4",
            "name": "KRK Rokit RP5 G4 Studio Monitor",
            "slug": "krk-rokit-rp5-g4-studio-monitor",
            "brand": "KRK",
            "description": "Professional 5-inch powered studio monitor with room correction and versatile connectivity.",
            "specifications": {
                "driver_config": "5-inch woofer, 1-inch tweeter",
                "power": "55W total (35W woofer, 20W tweeter)",
                "frequency_response": "43 Hz - 40 kHz",
                "max_spl": "104 dB",
                "inputs": "XLR, TRS, RCA",
                "eq": "25 graphic EQ settings",
                "room_correction": "DSP-driven",
                "dimensions": "185 x 284 x 242 mm",
                "weight": "4.8 kg"
            },
            "msrp_price": 179,
            "images": ["krk_rp5_g4_1.jpg", "krk_rp5_g4_2.jpg", "krk_rp5_g4_3.jpg"],
            "ai_generated_content": {
                "basic_info": {
                    "overview": "Professional 5-inch powered studio monitor with room correction and versatile connectivity. Accurate monitoring for home and professional studios.",
                    "target_skill_level": "Intermediate",
                    "country_of_origin": "China"
                },
                "professional_assessment": {
                    "expert_rating": {
                        "build_quality": "8",
                        "sound_quality": "8",
                        "value_for_money": "8",
                        "versatility": "7"
                    }
                }
            }
        }
    ]
}


async def get_brand_id(db: AsyncSession, brand_name: str) -> int:
    """Get brand ID by name, create if not exists."""
    result = await db.execute(select(Brand).where(Brand.name == brand_name))
    brand = result.scalar_one_or_none()
    
    if not brand:
        # Create brand if it doesn't exist
        brand = Brand(
            name=brand_name,
            slug=brand_name.lower().replace(' ', '-'),
            description=f"{brand_name} musical instruments and equipment",
            website_url=f"https://{brand_name.lower().replace(' ', '')}.com"
        )
        db.add(brand)
        await db.commit()
        await db.refresh(brand)
    
    return brand.id


async def get_category_id(db: AsyncSession, category_slug: str) -> int:
    """Get category ID by slug."""
    result = await db.execute(select(Category).where(Category.slug == category_slug))
    category = result.scalar_one_or_none()
    
    if not category:
        raise ValueError(f"Category with slug '{category_slug}' not found")
    
    return category.id


async def insert_product(db: AsyncSession, product_data: dict, category_slug: str):
    """Insert a single product into the database."""
    try:
        # Get brand and category IDs
        brand_id = await get_brand_id(db, product_data['brand'])
        category_id = await get_category_id(db, category_slug)
        
        # Check if product already exists
        result = await db.execute(select(Product).where(Product.sku == product_data['sku']))
        existing_product = result.scalar_one_or_none()
        
        if existing_product:
            print(f"⏭️  Product {product_data['sku']} already exists, skipping...")
            return
        
        # Create product
        product = Product(
            sku=product_data['sku'],
            name=product_data['name'],
            slug=product_data['slug'],
            brand_id=brand_id,
            category_id=category_id,
            description=product_data.get('description', ''),
            specifications=product_data.get('specifications', {}),
            images=product_data.get('images', []),
            msrp_price=Decimal(str(product_data['msrp_price'])) if product_data.get('msrp_price') else None,
            ai_generated_content=product_data.get('ai_generated_content', {}),
            avg_rating=Decimal('0'),
            review_count=0,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(product)
        await db.commit()
        
        print(f"✅ Successfully inserted: {product.name} ({product.sku})")
        
    except Exception as e:
        await db.rollback()
        print(f"❌ Error inserting product {product_data.get('sku', 'unknown')}: {str(e)}")
        raise


async def main():
    """Main function to insert all products."""
    print("🚀 Starting comprehensive product insertion...")
    
    async with async_session_factory() as db:
        total_products = 0
        successful_inserts = 0
        
        # Insert products for each category
        for category_slug, products in PRODUCTS_DATA.items():
            print(f"\n📂 Processing category: {category_slug}")
            print(f"   Products to insert: {len(products)}")
            
            for product_data in products:
                try:
                    await insert_product(db, product_data, category_slug)
                    successful_inserts += 1
                except Exception as e:
                    print(f"   ❌ Failed to insert {product_data.get('name', 'unknown')}: {str(e)}")
                
                total_products += 1
        
        print(f"\n🎉 Insertion complete!")
        print(f"   Total products processed: {total_products}")
        print(f"   Successful insertions: {successful_inserts}")
        print(f"   Failed insertions: {total_products - successful_inserts}")


if __name__ == "__main__":
    asyncio.run(main())