# 🎵 European Musical Instruments Comparison Platform

A modern, scalable platform for comparing musical instrument prices across Europe, built with FastAPI and Next.js. Features comprehensive AI-generated product analysis and detailed comparison tools.

## 🚀 Quick Start

### Development
```bash
# Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Frontend  
cd frontend && npm run dev
```

### Production Deployment
See `API_KEY_SETUP.md` for complete deployment guide with security setup.

## 🎯 Features

- **Comprehensive Product Analysis**: Detailed AI-generated content for every instrument
- **Advanced Product Comparison**: Compare 2-10 musical instruments with detailed insights
- **Price Tracking**: Real-time prices from major European stores
- **AI Content Generation**: Automated product descriptions, reviews, and technical analysis
- **Smart Search**: Advanced filtering and search capabilities
- **Mobile Responsive**: Optimized for all devices
- **SEO Optimized**: Built for search engine visibility
- **Expert Ratings**: Professional assessment scores for build quality, sound, value, and versatility

## 🛠️ Tech Stack

- **Backend**: FastAPI + PostgreSQL + Redis + OpenAI API
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Deployment**: Vercel (Frontend) + Render (Backend)
- **Security**: API key authentication + Cloudflare protection

## 📋 Product Data Structure

The platform uses a comprehensive JSON structure for each product with detailed AI-generated content:

### Basic Product Information
```json
{
  "id": 1,
  "sku": "FENDER-PLAYER-STRAT-SSS",
  "name": "Fender Player Stratocaster MIM",
  "slug": "fender-player-stratocaster-mim",
  "brand": {
    "id": 1,
    "name": "Fender",
    "slug": "fender",
    "logo_url": "https://example.com/fender-logo.png"
  },
  "category": {
    "id": 1,
    "name": "Electric Guitars",
    "slug": "electric-guitars"
  },
  "description": "The Player Stratocaster takes the best elements of the 60+ year-old Strat design...",
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
  "images": ["fender_player_strat_1.jpg", "fender_player_strat_2.jpg"],
  "avg_rating": 4.5,
  "review_count": 150
}
```

### Comprehensive AI-Generated Content
```json
{
  "ai_content": {
    "basic_info": {
      "overview": "The Fender Player Stratocaster MIM delivers the iconic Strat sound and feel with modern refinements...",
      "key_features": [
        "Player Series Alnico 5 single-coil pickups",
        "2-point synchronized tremolo bridge",
        "Modern 'C' shaped neck profile",
        "22-fret pau ferro fingerboard"
      ],
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
          "description": "Genuine Fender craftsmanship from the Corona factory with quality control standards..."
        },
        {
          "title": "Exceptional Versatility Across Genres",
          "description": "The five-way pickup selector and balanced pickup outputs make this guitar suitable for everything..."
        }
      ],
      "why_not_buy": [
        {
          "title": "Limited High-Output Capability",
          "description": "Single-coil pickups may not provide enough output for metal or very high-gain applications..."
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
          "reason": "Single-coil pickups and traditional output levels may not provide the high-gain characteristics..."
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
        "growth_potential": "This instrument will serve players from intermediate through advanced levels..."
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
      "competitive_position": "Strong value leader in the €700-800 range, offering genuine Fender quality..."
    },
    "content_metadata": {
      "generated_date": "2024-01-15T10:30:00Z",
      "content_version": "1.0",
      "seo_keywords": ["Fender Player Stratocaster", "Mexican Stratocaster", "intermediate electric guitar"],
      "readability_score": "Medium",
      "word_count": "750"
    }
  }
}
```

### Price Information
```json
{
  "prices": [
    {
      "id": 1,
      "store": {
        "id": 1,
        "name": "Thomann",
        "logo_url": "https://example.com/thomann-logo.png",
        "website_url": "https://thomann.de"
      },
      "price": 749.00,
      "currency": "EUR",
      "affiliate_url": "https://thomann.de/affiliate-link",
      "last_checked": "2024-01-15T10:30:00Z",
      "is_available": true
    }
  ],
  "best_price": {
    "price": 749.00,
    "currency": "EUR",
    "store": {
      "id": 1,
      "name": "Thomann"
    },
    "affiliate_url": "https://thomann.de/affiliate-link"
  }
}
```

## 🔐 Security

- **API Key Authentication**: Backend protected with secure API keys
- **Server-Side Proxy**: API keys never exposed to client-side
- **Cloudflare Protection**: DDoS protection, WAF, rate limiting
- **CORS Configuration**: Restricted to authorized domains only

## 💰 Revenue Model

- Affiliate commissions from Amazon, Thomann, Gear4Music, Kytary
- Google AdSense advertisements in sidebar
- Target: €25K-€75K monthly revenue within 12 months

## 📢 Google AdSense Setup

The platform includes integrated Google AdSense support with sidebar advertisements:

### 1. Environment Configuration
Add your Google AdSense publisher ID to your environment variables:
```bash
# In frontend/.env.local or Vercel environment variables
NEXT_PUBLIC_GOOGLE_ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXX
```

### 2. Ad Slot Configuration
Update the ad slot IDs in `frontend/src/components/AdSidebar.tsx`:
```typescript
// Replace placeholder ad slot IDs with your actual AdSense ad unit IDs
adSlot="1234567890" // Top sidebar ad
adSlot="0987654321" // Middle sidebar ad  
adSlot="1122334455" // Bottom sidebar ad
```

### 3. Ad Placement
- **Desktop**: Right sidebar with 3 advertisement sections
- **Mobile**: Ads stack below content for better mobile experience
- **Responsive**: Automatically adjusts to different screen sizes

### 4. Ad Formats Supported
- Rectangle ads (300x250, 336x280)
- Responsive ads that adapt to container size
- Placeholder ads shown during development/testing

### 5. Implementation Features
- Ad blocker detection with fallback messages
- Sticky positioning for top ad on desktop
- Proper spacing and styling integration
- SEO-friendly implementation

## 📊 Project Status

- ✅ Complete backend API implementation
- ✅ Full frontend React components with comprehensive product details
- ✅ AI content generation system with detailed analysis
- ✅ Multi-store price comparison with real-time tracking
- ✅ Comprehensive product comparison tools
- ✅ Expert ratings and professional assessments
- ✅ Maintenance and care guidance
- ✅ Usage recommendations and skill development insights
- ✅ Production deployment scripts
- ✅ Security implementation
- ✅ Google AdSense integration with sidebar advertisements
- 🔄 Ready for launch

## 🎸 Supported Categories

- **Electric Guitars**: Stratocasters, Les Pauls, Telecasters, and more
- **Acoustic Guitars**: Classical, folk, and steel-string acoustics
- **Bass Guitars**: Electric and acoustic bass guitars
- **Digital Keyboards**: Pianos, synthesizers, and workstations
- **Amplifiers**: Guitar and bass amplifiers
- **Studio Equipment**: Recording interfaces, microphones, headphones
- **Effects Pedals**: Guitar effects and processors
- **DJ Equipment**: Turntables, mixers, and controllers

## 📄 License

MIT License - see LICENSE file for details.
