-- Test data for musical instruments platform
-- Copy and paste this entire script into the Render CLI SQL console

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    logo_url TEXT,
    website_url TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    parent_id INTEGER REFERENCES categories(id),
    description TEXT,
    image_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS affiliate_stores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    website_url TEXT NOT NULL,
    logo_url TEXT,
    commission_rate DECIMAL(5,2),
    api_endpoint TEXT,
    api_key_encrypted TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    brand_id INTEGER REFERENCES brands(id) NOT NULL,
    category_id INTEGER REFERENCES categories(id) NOT NULL,
    description TEXT,
    specifications JSONB DEFAULT '{}',
    images TEXT[],
    msrp_price DECIMAL(10,2),
    ai_generated_content JSONB DEFAULT '{}',
    avg_rating DECIMAL(3,2) DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_prices (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) NOT NULL,
    store_id INTEGER REFERENCES affiliate_stores(id) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    affiliate_url TEXT NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert test data
-- Brands
INSERT INTO brands (name, slug, description, created_at) VALUES 
('Fender', 'fender', 'Iconic American guitar manufacturer', CURRENT_TIMESTAMP),
('Gibson', 'gibson', 'Legendary guitar and instrument maker', CURRENT_TIMESTAMP),
('Yamaha', 'yamaha', 'Japanese musical instrument giant', CURRENT_TIMESTAMP),
('Roland', 'roland', 'Electronic music instrument pioneer', CURRENT_TIMESTAMP),
('Marshall', 'marshall', 'British amplifier manufacturer', CURRENT_TIMESTAMP),
('Ibanez', 'ibanez', 'Japanese guitar manufacturer', CURRENT_TIMESTAMP)
ON CONFLICT (slug) DO NOTHING;

-- Categories
INSERT INTO categories (name, slug, description, is_active, created_at) VALUES 
('Electric Guitars', 'electric-guitars', 'Electric guitars and basses', TRUE, CURRENT_TIMESTAMP),
('Acoustic Guitars', 'acoustic-guitars', 'Acoustic and classical guitars', TRUE, CURRENT_TIMESTAMP),
('Digital Keyboards', 'digital-keyboards', 'Digital pianos and keyboards', TRUE, CURRENT_TIMESTAMP),
('Synthesizers', 'synthesizers', 'Analog and digital synthesizers', TRUE, CURRENT_TIMESTAMP),
('Amplifiers', 'amplifiers', 'Guitar and bass amplifiers', TRUE, CURRENT_TIMESTAMP),
('Studio and Recording Equipment', 'studio-and-recording-equipment', 'Recording interfaces and equipment', TRUE, CURRENT_TIMESTAMP)
ON CONFLICT (slug) DO NOTHING;

-- Affiliate Stores
INSERT INTO affiliate_stores (name, slug, website_url, commission_rate, is_active, created_at) VALUES 
('Amazon', 'amazon', 'https://amazon.es', 4.5, TRUE, CURRENT_TIMESTAMP),
('Thomann', 'thomann', 'https://thomann.de', 3.0, TRUE, CURRENT_TIMESTAMP),
('Gear4Music', 'gear4music', 'https://gear4music.com', 4.0, TRUE, CURRENT_TIMESTAMP),
('Kytary', 'kytary', 'https://kytary.de', 2.5, TRUE, CURRENT_TIMESTAMP)
ON CONFLICT (slug) DO NOTHING;

-- Products
INSERT INTO products (sku, name, slug, brand_id, category_id, description, msrp_price, specifications, images, ai_generated_content, avg_rating, review_count, is_active, created_at, updated_at) VALUES 
('FENDER-STRAT-MX-SSS', 
 'Fender Player Stratocaster MX', 
 'fender-player-stratocaster-mx',
 (SELECT id FROM brands WHERE slug = 'fender'),
 (SELECT id FROM categories WHERE slug = 'electric-guitars'),
 'The Player Stratocaster takes the best features of the original and adds modern improvements.',
 799.00,
 '{"body_wood": "Alder", "neck_wood": "Maple", "fretboard": "Maple", "pickups": "Player Series Alnico 5 Strat Single-Coil", "scale_length": "25.5\"", "frets": 22}',
 '{"https://example.com/fender-strat-1.jpg", "https://example.com/fender-strat-2.jpg"}',
 '{}',
 4.5,
 23,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),
('YAMAHA-P45',
 'Yamaha P-45 Digital Piano',
 'yamaha-p-45-digital-piano',
 (SELECT id FROM brands WHERE slug = 'yamaha'),
 (SELECT id FROM categories WHERE slug = 'digital-keyboards'),
 'Compact digital piano with 88 weighted keys and authentic piano sound.',
 549.00,
 '{"keys": 88, "key_action": "Graded Hammer Standard (GHS)", "voices": 10, "polyphony": 64, "weight": "11.5 kg"}',
 '{"https://example.com/yamaha-p45-1.jpg"}',
 '{}',
 4.2,
 18,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP),
('MARSHALL-DSL40CR',
 'Marshall DSL40CR Guitar Amplifier',
 'marshall-dsl40cr-guitar-amplifier',
 (SELECT id FROM brands WHERE slug = 'marshall'),
 (SELECT id FROM categories WHERE slug = 'amplifiers'),
 '40-watt tube guitar amplifier with classic Marshall tone.',
 899.00,
 '{"power": "40W", "tubes": "ECC83, EL34", "channels": 2, "speaker": "12\" Celestion V-Type", "effects": "Reverb"}',
 '{"https://example.com/marshall-dsl40cr-1.jpg"}',
 '{}',
 4.7,
 31,
 TRUE,
 CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP)
ON CONFLICT (sku) DO UPDATE SET updated_at = CURRENT_TIMESTAMP;

-- Product Prices
INSERT INTO product_prices (product_id, store_id, price, currency, affiliate_url, is_available, last_checked, created_at) VALUES 
-- Fender Stratocaster prices
((SELECT id FROM products WHERE sku = 'FENDER-STRAT-MX-SSS'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 719.10, 'EUR', 'https://amazon.com/product/FENDER-STRAT-MX-SSS?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'FENDER-STRAT-MX-SSS'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 759.05, 'EUR', 'https://thomann.com/product/FENDER-STRAT-MX-SSS?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'FENDER-STRAT-MX-SSS'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 799.00, 'EUR', 'https://gear4music.com/product/FENDER-STRAT-MX-SSS?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Yamaha P-45 prices
((SELECT id FROM products WHERE sku = 'YAMAHA-P45'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 494.10, 'EUR', 'https://amazon.com/product/YAMAHA-P45?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'YAMAHA-P45'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 521.55, 'EUR', 'https://thomann.com/product/YAMAHA-P45?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'YAMAHA-P45'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 549.00, 'EUR', 'https://gear4music.com/product/YAMAHA-P45?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Marshall DSL40CR prices
((SELECT id FROM products WHERE sku = 'MARSHALL-DSL40CR'), (SELECT id FROM affiliate_stores WHERE slug = 'amazon'), 809.10, 'EUR', 'https://amazon.com/product/MARSHALL-DSL40CR?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'MARSHALL-DSL40CR'), (SELECT id FROM affiliate_stores WHERE slug = 'thomann'), 854.05, 'EUR', 'https://thomann.com/product/MARSHALL-DSL40CR?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
((SELECT id FROM products WHERE sku = 'MARSHALL-DSL40CR'), (SELECT id FROM affiliate_stores WHERE slug = 'gear4music'), 899.00, 'EUR', 'https://gear4music.com/product/MARSHALL-DSL40CR?aff=123', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;

-- Create comparison_views table if not exists
CREATE TABLE IF NOT EXISTS comparison_views (
    id SERIAL PRIMARY KEY,
    product_ids INTEGER[],
    user_ip VARCHAR(45),
    user_country VARCHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comparison Views (simulating users comparing products)
INSERT INTO comparison_views (product_ids, user_ip, user_country, created_at) VALUES 
-- User comparing Fender and Yamaha
(ARRAY[(SELECT id FROM products WHERE sku = 'FENDER-STRAT-MX-SSS'), (SELECT id FROM products WHERE sku = 'YAMAHA-P45')], '192.168.1.100', 'ES', CURRENT_TIMESTAMP - INTERVAL '2 hours'),

-- User comparing all three products
(ARRAY[(SELECT id FROM products WHERE sku = 'FENDER-STRAT-MX-SSS'), (SELECT id FROM products WHERE sku = 'YAMAHA-P45'), (SELECT id FROM products WHERE sku = 'MARSHALL-DSL40CR')], '10.0.0.50', 'DE', CURRENT_TIMESTAMP - INTERVAL '1 hour'),

-- User comparing Fender and Marshall
(ARRAY[(SELECT id FROM products WHERE sku = 'FENDER-STRAT-MX-SSS'), (SELECT id FROM products WHERE sku = 'MARSHALL-DSL40CR')], '172.16.0.25', 'FR', CURRENT_TIMESTAMP - INTERVAL '30 minutes'),

-- User comparing Yamaha and Marshall
(ARRAY[(SELECT id FROM products WHERE sku = 'YAMAHA-P45'), (SELECT id FROM products WHERE sku = 'MARSHALL-DSL40CR')], '203.0.113.15', 'IT', CURRENT_TIMESTAMP - INTERVAL '15 minutes'),

-- Recent comparison of all products
(ARRAY[(SELECT id FROM products WHERE sku = 'FENDER-STRAT-MX-SSS'), (SELECT id FROM products WHERE sku = 'YAMAHA-P45'), (SELECT id FROM products WHERE sku = 'MARSHALL-DSL40CR')], '198.51.100.75', 'NL', CURRENT_TIMESTAMP - INTERVAL '5 minutes');

-- Display summary
SELECT 'Test data inserted successfully!' as status;
SELECT COUNT(*) as brands_count FROM brands;
SELECT COUNT(*) as categories_count FROM categories;
SELECT COUNT(*) as stores_count FROM affiliate_stores;
SELECT COUNT(*) as products_count FROM products;
SELECT COUNT(*) as prices_count FROM product_prices;
SELECT COUNT(*) as comparison_views_count FROM comparison_views;