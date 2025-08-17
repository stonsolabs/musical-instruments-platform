-- Additional test data for musical instruments platform
-- This expands the existing dataset with more diverse instruments for better comparisons

-- Additional Brands
INSERT INTO brands (name, slug, description, created_at) VALUES 
('Taylor', 'taylor', 'Premium acoustic guitar manufacturer', CURRENT_TIMESTAMP),
('Martin', 'martin', 'Historic American guitar maker since 1833', CURRENT_TIMESTAMP),
('Korg', 'korg', 'Japanese electronic music instrument manufacturer', CURRENT_TIMESTAMP),
('Moog', 'moog', 'Pioneer in analog synthesizer technology', CURRENT_TIMESTAMP),
('PRS', 'prs', 'Paul Reed Smith high-end electric guitars', CURRENT_TIMESTAMP),
('Steinberg', 'steinberg', 'Professional audio software and hardware', CURRENT_TIMESTAMP),
('Shure', 'shure', 'Professional microphone manufacturer', CURRENT_TIMESTAMP),
('Boss', 'boss', 'Guitar effects and audio equipment', CURRENT_TIMESTAMP),
('ESP', 'esp', 'Japanese guitar manufacturer specializing in metal guitars', CURRENT_TIMESTAMP),
('Casio', 'casio', 'Electronic instruments and calculators', CURRENT_TIMESTAMP)
ON CONFLICT (slug) DO NOTHING;

-- Additional Categories
INSERT INTO categories (name, slug, description, is_active, created_at) VALUES 
('Bass Guitars', 'bass-guitars', 'Electric and acoustic bass guitars', TRUE, CURRENT_TIMESTAMP),
('Drums & Percussion', 'drums-percussion', 'Drums, cymbals, and percussion instruments', TRUE, CURRENT_TIMESTAMP),
('Microphones', 'microphones', 'Studio and live microphones', TRUE, CURRENT_TIMESTAMP),
('Effects Pedals', 'effects-pedals', 'Guitar and bass effects pedals', TRUE, CURRENT_TIMESTAMP),
('Studio Monitors', 'studio-monitors', 'Professional studio speakers', TRUE, CURRENT_TIMESTAMP),
('DJ Equipment', 'dj-equipment', 'DJ controllers, mixers, and turntables', TRUE, CURRENT_TIMESTAMP),
('Wind Instruments', 'wind-instruments', 'Saxophones, trumpets, and wind instruments', TRUE, CURRENT_TIMESTAMP),
('String Instruments', 'string-instruments', 'Violins, cellos, and orchestral strings', TRUE, CURRENT_TIMESTAMP)
ON CONFLICT (slug) DO NOTHING;

-- Additional Products with varied specifications and price ranges
INSERT INTO products (sku, name, slug, brand_id, category_id, description, msrp_price, specifications, images, ai_generated_content, avg_rating, review_count, is_active, created_at, updated_at) VALUES 

-- High-end acoustic guitars
('TAYLOR-814CE-V3', 
 'Taylor 814ce V-Class Grand Auditorium', 
 'taylor-814ce-v-class-grand-auditorium',
 (SELECT id FROM brands WHERE slug = 'taylor'),
 (SELECT id FROM categories WHERE slug = 'acoustic-guitars'),
 'Premium acoustic-electric guitar with V-Class bracing for enhanced volume and sustain.',
 4299.00,
 '{"body_wood": "Indian Rosewood", "top_wood": "Sitka Spruce", "neck_wood": "Tropical Mahogany", "electronics": "ES2", "scale_length": "25.5\"", "nut_width": "1.75\""}',
 '{"https://example.com/taylor-814ce-1.jpg", "https://example.com/taylor-814ce-2.jpg"}',
 '{"sound_description": "Rich, balanced tone with excellent projection", "ideal_for": "Professional recording and live performance"}',
 4.8,
 47,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

('MARTIN-D28', 
 'Martin D-28 Dreadnought Acoustic Guitar', 
 'martin-d-28-dreadnought-acoustic-guitar',
 (SELECT id FROM brands WHERE slug = 'martin'),
 (SELECT id FROM categories WHERE slug = 'acoustic-guitars'),
 'Iconic dreadnought acoustic guitar with legendary Martin tone.',
 3199.00,
 '{"body_wood": "East Indian Rosewood", "top_wood": "Sitka Spruce", "neck_wood": "Select Hardwood", "fingerboard": "Ebony", "scale_length": "25.4\"", "nut_width": "1.75\""}',
 '{"https://example.com/martin-d28-1.jpg"}',
 '{"sound_description": "Bold, powerful bass with clear trebles", "ideal_for": "Bluegrass, country, and folk music"}',
 4.7,
 62,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Electric guitars - different price points and styles
('PRS-SE-CUSTOM-24', 
 'PRS SE Custom 24', 
 'prs-se-custom-24',
 (SELECT id FROM brands WHERE slug = 'prs'),
 (SELECT id FROM categories WHERE slug = 'electric-guitars'),
 'Versatile electric guitar with PRS design and Korean craftsmanship.',
 899.00,
 '{"body_wood": "Mahogany", "top_wood": "Maple Veneer", "neck_wood": "Maple", "fretboard": "Rosewood", "pickups": "85/15 \"S\" Humbuckers", "scale_length": "25\"", "frets": 24}',
 '{"https://example.com/prs-se-custom-24-1.jpg"}',
 '{"sound_description": "Balanced output perfect for clean and distorted tones", "ideal_for": "Rock, metal, and versatile playing styles"}',
 4.6,
 34,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

('ESP-LTD-EC-1000', 
 'ESP LTD EC-1000 Electric Guitar', 
 'esp-ltd-ec-1000-electric-guitar',
 (SELECT id FROM brands WHERE slug = 'esp'),
 (SELECT id FROM categories WHERE slug = 'electric-guitars'),
 'High-performance electric guitar designed for metal and hard rock.',
 1199.00,
 '{"body_wood": "Mahogany", "neck_wood": "3-piece Mahogany", "fretboard": "Ebony", "pickups": "EMG 81/60 Active", "scale_length": "24.75\"", "frets": 24, "binding": "Cream"}',
 '{"https://example.com/esp-ltd-ec-1000-1.jpg"}',
 '{"sound_description": "High-output pickups perfect for heavy music", "ideal_for": "Metal, hard rock, and high-gain applications"}',
 4.4,
 28,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Bass guitars
('FENDER-P-BASS-MX', 
 'Fender Player Precision Bass MX', 
 'fender-player-precision-bass-mx',
 (SELECT id FROM brands WHERE slug = 'fender'),
 (SELECT id FROM categories WHERE slug = 'bass-guitars'),
 'Classic Precision Bass with modern features and Mexican craftsmanship.',
 849.00,
 '{"body_wood": "Alder", "neck_wood": "Maple", "fretboard": "Maple", "pickups": "Player Series Split Single-Coil", "scale_length": "34\"", "frets": 20, "strings": 4}',
 '{"https://example.com/fender-p-bass-1.jpg"}',
 '{"sound_description": "Deep, punchy bass tone with excellent definition", "ideal_for": "Rock, funk, and all bass applications"}',
 4.5,
 41,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Digital keyboards and synthesizers
('KORG-MINILOGUE-XD', 
 'Korg Minilogue XD Analog Synthesizer', 
 'korg-minilogue-xd-analog-synthesizer',
 (SELECT id FROM brands WHERE slug = 'korg'),
 (SELECT id FROM categories WHERE slug = 'synthesizers'),
 'Polyphonic analog synthesizer with digital effects and user oscillators.',
 699.00,
 '{"voices": 4, "oscillators": "2 analog + 1 digital", "filter": "2-pole analog", "effects": "Digital reverb, delay, modulation", "keys": 37, "sequencer": "16-step"}',
 '{"https://example.com/korg-minilogue-xd-1.jpg"}',
 '{"sound_description": "Warm analog tones with modern digital flexibility", "ideal_for": "Electronic music production and live performance"}',
 4.3,
 25,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

('MOOG-SUBSEQUENT-37', 
 'Moog Subsequent 37 Analog Synthesizer', 
 'moog-subsequent-37-analog-synthesizer',
 (SELECT id FROM brands WHERE slug = 'moog'),
 (SELECT id FROM categories WHERE slug = 'synthesizers'),
 'Professional analog synthesizer with legendary Moog sound.',
 1599.00,
 '{"voices": 1, "oscillators": 2, "filter": "Moog 4-pole ladder", "keyboard": "37 keys", "sequencer": "256-step", "mod_sources": "Multiple LFOs and envelopes"}',
 '{"https://example.com/moog-subsequent-37-1.jpg"}',
 '{"sound_description": "Classic Moog warmth and power", "ideal_for": "Lead lines, bass, and experimental sounds"}',
 4.9,
 15,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

('CASIO-PRIVIA-PX-S1100', 
 'Casio Privia PX-S1100 Digital Piano', 
 'casio-privia-px-s1100-digital-piano',
 (SELECT id FROM brands WHERE slug = 'casio'),
 (SELECT id FROM categories WHERE slug = 'digital-keyboards'),
 'Ultra-compact digital piano with 88 weighted keys and premium sound.',
 799.00,
 '{"keys": 88, "key_action": "Smart Scaled Hammer Action", "voices": 18, "polyphony": 192, "speakers": "2 x 8W", "connectivity": "USB, Bluetooth"}',
 '{"https://example.com/casio-privia-px-s1100-1.jpg"}',
 '{"sound_description": "Authentic piano sound in an ultra-portable design", "ideal_for": "Home practice and portable performance"}',
 4.1,
 33,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Audio interfaces and studio equipment
('STEINBERG-UR22C', 
 'Steinberg UR22C USB Audio Interface', 
 'steinberg-ur22c-usb-audio-interface',
 (SELECT id FROM brands WHERE slug = 'steinberg'),
 (SELECT id FROM categories WHERE slug = 'audio-interfaces'),
 '2x2 USB-C audio interface with premium D-PRE preamps.',
 189.00,
 '{"inputs": "2 x XLR/TRS combo", "outputs": "2 x TRS", "sample_rate": "192 kHz", "bit_depth": "32-bit", "connectivity": "USB-C", "software": "Cubase AI included"}',
 '{"https://example.com/steinberg-ur22c-1.jpg"}',
 '{"sound_description": "Crystal clear audio conversion with professional preamps", "ideal_for": "Home recording and podcasting"}',
 4.2,
 67,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Microphones
('SHURE-SM57', 
 'Shure SM57 Dynamic Microphone', 
 'shure-sm57-dynamic-microphone',
 (SELECT id FROM brands WHERE slug = 'shure'),
 (SELECT id FROM categories WHERE slug = 'microphones'),
 'Industry standard dynamic microphone for instruments and vocals.',
 109.00,
 '{"type": "Dynamic", "polar_pattern": "Cardioid", "frequency_response": "40 Hz - 15 kHz", "impedance": "150 ohms", "connector": "XLR", "weight": "284g"}',
 '{"https://example.com/shure-sm57-1.jpg"}',
 '{"sound_description": "Clear, punchy sound that cuts through any mix", "ideal_for": "Guitar amps, snare drums, and live vocals"}',
 4.8,
 156,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

('SHURE-SM58', 
 'Shure SM58 Vocal Microphone', 
 'shure-sm58-vocal-microphone',
 (SELECT id FROM brands WHERE slug = 'shure'),
 (SELECT id FROM categories WHERE slug = 'microphones'),
 'World standard handheld vocal microphone.',
 119.00,
 '{"type": "Dynamic", "polar_pattern": "Cardioid", "frequency_response": "50 Hz - 15 kHz", "impedance": "150 ohms", "connector": "XLR", "weight": "298g"}',
 '{"https://example.com/shure-sm58-1.jpg"}',
 '{"sound_description": "Warm, clear vocal reproduction with excellent feedback rejection", "ideal_for": "Live vocals and speech"}',
 4.7,
 203,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Effects pedals
('BOSS-DS-1', 
 'Boss DS-1 Distortion Pedal', 
 'boss-ds-1-distortion-pedal',
 (SELECT id FROM brands WHERE slug = 'boss'),
 (SELECT id FROM categories WHERE slug = 'effects-pedals'),
 'Classic distortion pedal used by countless guitarists worldwide.',
 55.00,
 '{"type": "Distortion", "controls": "Level, Tone, Distortion", "input_impedance": "1 MOhm", "power": "9V battery or PSA", "dimensions": "70 x 125 x 59 mm"}',
 '{"https://example.com/boss-ds-1-1.jpg"}',
 '{"sound_description": "Classic rock distortion with versatile tone shaping", "ideal_for": "Rock, punk, and alternative music"}',
 4.3,
 89,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

('BOSS-DD-8', 
 'Boss DD-8 Digital Delay Pedal', 
 'boss-dd-8-digital-delay-pedal',
 (SELECT id FROM brands WHERE slug = 'boss'),
 (SELECT id FROM categories WHERE slug = 'effects-pedals'),
 'Advanced digital delay with 10 modes and tap tempo.',
 179.00,
 '{"type": "Digital Delay", "modes": 10, "delay_time": "40ms - 10 seconds", "controls": "Level, Feedback, Time, Mode", "tap_tempo": "Yes", "stereo": "Yes"}',
 '{"https://example.com/boss-dd-8-1.jpg"}',
 '{"sound_description": "Crystal clear delays with vintage analog modeling", "ideal_for": "Ambient textures and rhythmic delays"}',
 4.6,
 45,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

-- Budget-friendly options
('YAMAHA-FG800', 
 'Yamaha FG800 Acoustic Guitar', 
 'yamaha-fg800-acoustic-guitar',
 (SELECT id FROM brands WHERE slug = 'yamaha'),
 (SELECT id FROM categories WHERE slug = 'acoustic-guitars'),
 'Affordable solid-top acoustic guitar with excellent build quality.',
 219.00,
 '{"body_wood": "Nato", "top_wood": "Solid Sitka Spruce", "neck_wood": "Nato", "fingerboard": "Rosewood", "scale_length": "25.6\"", "nut_width": "1.65\""}',
 '{"https://example.com/yamaha-fg800-1.jpg"}',
 '{"sound_description": "Balanced tone with solid spruce top projection", "ideal_for": "Beginners and budget-conscious players"}',
 4.4,
 127,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),

('IBANEZ-GRG121DX', 
 'Ibanez GRG121DX Electric Guitar', 
 'ibanez-grg121dx-electric-guitar',
 (SELECT id FROM brands WHERE slug = 'ibanez'),
 (SELECT id FROM categories WHERE slug = 'electric-guitars'),
 'Entry-level electric guitar with modern features and comfortable playability.',
 199.00,
 '{"body_wood": "Poplar", "neck_wood": "Maple", "fretboard": "Jatoba", "pickups": "IBZ-6 Humbuckers", "scale_length": "25.5\"", "frets": 24, "bridge": "Fixed"}',
 '{"https://example.com/ibanez-grg121dx-1.jpg"}',
 '{"sound_description": "Versatile pickup combination suitable for various genres", "ideal_for": "Beginning guitarists and practice"}',
 4.0,
 94,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP)

ON CONFLICT (sku) DO UPDATE SET updated_at = CURRENT_TIMESTAMP;

-- Additional Product Prices for better comparison data
INSERT INTO product_prices (product_id, store_id, price, currency, affiliate_url, is_available, last_checked, created_at) VALUES 

-- Taylor 814ce prices (high-end)
((SELECT id FROM products WHERE sku = 'TAYLOR-814CE-V3'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 3869.10, 'EUR', 'https://amazon.com/product/TAYLOR-814CE-V3?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'TAYLOR-814CE-V3'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 4099.00, 'EUR', 'https://thomann.com/product/TAYLOR-814CE-V3?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'TAYLOR-814CE-V3'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 4299.00, 'EUR', 'https://gear4music.com/product/TAYLOR-814CE-V3?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Martin D-28 prices
((SELECT id FROM products WHERE sku = 'MARTIN-D28'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 2879.10, 'EUR', 'https://amazon.com/product/MARTIN-D28?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'MARTIN-D28'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 3049.00, 'EUR', 'https://thomann.com/product/MARTIN-D28?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'MARTIN-D28'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 3199.00, 'EUR', 'https://gear4music.com/product/MARTIN-D28?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- PRS SE Custom 24 prices
((SELECT id FROM products WHERE sku = 'PRS-SE-CUSTOM-24'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 809.10, 'EUR', 'https://amazon.com/product/PRS-SE-CUSTOM-24?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'PRS-SE-CUSTOM-24'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 855.00, 'EUR', 'https://thomann.com/product/PRS-SE-CUSTOM-24?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'PRS-SE-CUSTOM-24'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 899.00, 'EUR', 'https://gear4music.com/product/PRS-SE-CUSTOM-24?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Fender Precision Bass prices
((SELECT id FROM products WHERE sku = 'FENDER-P-BASS-MX'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 764.10, 'EUR', 'https://amazon.com/product/FENDER-P-BASS-MX?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'FENDER-P-BASS-MX'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 809.00, 'EUR', 'https://thomann.com/product/FENDER-P-BASS-MX?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'FENDER-P-BASS-MX'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 849.00, 'EUR', 'https://gear4music.com/product/FENDER-P-BASS-MX?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Korg Minilogue XD prices
((SELECT id FROM products WHERE sku = 'KORG-MINILOGUE-XD'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 629.10, 'EUR', 'https://amazon.com/product/KORG-MINILOGUE-XD?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'KORG-MINILOGUE-XD'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 665.00, 'EUR', 'https://thomann.com/product/KORG-MINILOGUE-XD?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'KORG-MINILOGUE-XD'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 699.00, 'EUR', 'https://gear4music.com/product/KORG-MINILOGUE-XD?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Moog Subsequent 37 prices
((SELECT id FROM products WHERE sku = 'MOOG-SUBSEQUENT-37'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 1439.10, 'EUR', 'https://amazon.com/product/MOOG-SUBSEQUENT-37?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'MOOG-SUBSEQUENT-37'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 1519.00, 'EUR', 'https://thomann.com/product/MOOG-SUBSEQUENT-37?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'MOOG-SUBSEQUENT-37'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 1599.00, 'EUR', 'https://gear4music.com/product/MOOG-SUBSEQUENT-37?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Shure SM57 prices
((SELECT id FROM products WHERE sku = 'SHURE-SM57'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 98.10, 'EUR', 'https://amazon.com/product/SHURE-SM57?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'SHURE-SM57'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 103.50, 'EUR', 'https://thomann.com/product/SHURE-SM57?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'SHURE-SM57'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 109.00, 'EUR', 'https://gear4music.com/product/SHURE-SM57?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Yamaha FG800 prices (budget option)
((SELECT id FROM products WHERE sku = 'YAMAHA-FG800'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 197.10, 'EUR', 'https://amazon.com/product/YAMAHA-FG800?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'YAMAHA-FG800'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 208.50, 'EUR', 'https://thomann.com/product/YAMAHA-FG800?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'YAMAHA-FG800'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 219.00, 'EUR', 'https://gear4music.com/product/YAMAHA-FG800?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Boss DS-1 prices (budget pedal)
((SELECT id FROM products WHERE sku = 'BOSS-DS-1'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 49.50, 'EUR', 'https://amazon.com/product/BOSS-DS-1?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'BOSS-DS-1'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 52.25, 'EUR', 'https://thomann.com/product/BOSS-DS-1?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'BOSS-DS-1'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 55.00, 'EUR', 'https://gear4music.com/product/BOSS-DS-1?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)

ON CONFLICT DO NOTHING;

-- Additional comparison views with the new products
INSERT INTO comparison_views (product_ids, user_ip, user_country, created_at) VALUES 

-- Acoustic guitar comparisons
(ARRAY[(SELECT id FROM products WHERE sku = 'TAYLOR-814CE-V3'), (SELECT id FROM products WHERE sku = 'MARTIN-D28'), (SELECT id FROM products WHERE sku = 'YAMAHA-FG800')], '192.168.1.101', 'ES', CURRENT_TIMESTAMP - INTERVAL '3 hours'),

-- Electric guitar comparisons across price ranges
(ARRAY[(SELECT id FROM products WHERE sku = 'FENDER-STRAT-MX-SSS'), (SELECT id FROM products WHERE sku = 'PRS-SE-CUSTOM-24'), (SELECT id FROM products WHERE sku = 'ESP-LTD-EC-1000')], '10.0.0.51', 'DE', CURRENT_TIMESTAMP - INTERVAL '2 hours'),

-- Synthesizer comparisons
(ARRAY[(SELECT id FROM products WHERE sku = 'KORG-MINILOGUE-XD'), (SELECT id FROM products WHERE sku = 'MOOG-SUBSEQUENT-37')], '172.16.0.26', 'FR', CURRENT_TIMESTAMP - INTERVAL '1 hour'),

-- Digital piano comparisons
(ARRAY[(SELECT id FROM products WHERE sku = 'YAMAHA-P45'), (SELECT id FROM products WHERE sku = 'CASIO-PRIVIA-PX-S1100')], '203.0.113.16', 'IT', CURRENT_TIMESTAMP - INTERVAL '45 minutes'),

-- Microphone comparisons
(ARRAY[(SELECT id FROM products WHERE sku = 'SHURE-SM57'), (SELECT id FROM products WHERE sku = 'SHURE-SM58')], '198.51.100.76', 'NL', CURRENT_TIMESTAMP - INTERVAL '30 minutes'),

-- Budget vs premium acoustic guitars
(ARRAY[(SELECT id FROM products WHERE sku = 'YAMAHA-FG800'), (SELECT id FROM products WHERE sku = 'TAYLOR-814CE-V3')], '192.168.1.102', 'ES', CURRENT_TIMESTAMP - INTERVAL '20 minutes'),

-- Effects pedal comparisons
(ARRAY[(SELECT id FROM products WHERE sku = 'BOSS-DS-1'), (SELECT id FROM products WHERE sku = 'BOSS-DD-8')], '10.0.0.52', 'DE', CURRENT_TIMESTAMP - INTERVAL '10 minutes');

-- Display summary of new data
SELECT 'Additional test data inserted successfully!' as status;
SELECT COUNT(*) as total_brands_count FROM brands;
SELECT COUNT(*) as total_categories_count FROM categories;
SELECT COUNT(*) as total_products_count FROM products;
SELECT COUNT(*) as total_prices_count FROM product_prices;
SELECT COUNT(*) as total_comparison_views_count FROM comparison_views;

-- Show price range distribution
SELECT 
    CASE 
        WHEN msrp_price < 100 THEN 'Under €100'
        WHEN msrp_price < 500 THEN '€100-€500'
        WHEN msrp_price < 1000 THEN '€500-€1000'
        WHEN msrp_price < 2000 THEN '€1000-€2000'
        ELSE 'Over €2000'
    END as price_range,
    COUNT(*) as product_count
FROM products 
WHERE msrp_price IS NOT NULL
GROUP BY 
    CASE 
        WHEN msrp_price < 100 THEN 'Under €100'
        WHEN msrp_price < 500 THEN '€100-€500'
        WHEN msrp_price < 1000 THEN '€500-€1000'
        WHEN msrp_price < 2000 THEN '€1000-€2000'
        ELSE 'Over €2000'
    END
ORDER BY MIN(msrp_price);