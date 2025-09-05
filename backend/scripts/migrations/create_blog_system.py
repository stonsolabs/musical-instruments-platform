"""
Database migration to create blog system with categories and product integration
Run this script to add the blog functionality
"""

import asyncio
import asyncpg
import os
from datetime import datetime

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/musicgear_db')

async def create_blog_system():
    """Create the blog system tables"""
    
    create_tables_sql = """
    -- Blog categories table
    CREATE TABLE IF NOT EXISTS blog_categories (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        slug VARCHAR(100) NOT NULL UNIQUE,
        description TEXT,
        icon VARCHAR(50),
        color VARCHAR(50),
        sort_order INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Blog posts table
    CREATE TABLE IF NOT EXISTS blog_posts (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        slug VARCHAR(255) NOT NULL UNIQUE,
        excerpt TEXT,
        content TEXT NOT NULL,
        featured_image TEXT,
        category_id INTEGER REFERENCES blog_categories(id) ON DELETE CASCADE,
        author_name VARCHAR(100) DEFAULT 'GetYourMusicGear Team',
        author_email VARCHAR(255),
        status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
        seo_title VARCHAR(255),
        seo_description TEXT,
        reading_time INTEGER, -- estimated reading time in minutes
        view_count INTEGER DEFAULT 0,
        featured BOOLEAN DEFAULT FALSE,
        published_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Blog post products (many-to-many relationship)
    CREATE TABLE IF NOT EXISTS blog_post_products (
        id SERIAL PRIMARY KEY,
        blog_post_id INTEGER REFERENCES blog_posts(id) ON DELETE CASCADE,
        product_id INTEGER, -- references products table
        position INTEGER DEFAULT 0, -- order in the post
        context TEXT, -- context of how product is mentioned (e.g., "recommended", "compared", "featured")
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(blog_post_id, product_id)
    );
    
    -- Blog tags table
    CREATE TABLE IF NOT EXISTS blog_tags (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        slug VARCHAR(100) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Blog post tags (many-to-many relationship)
    CREATE TABLE IF NOT EXISTS blog_post_tags (
        id SERIAL PRIMARY KEY,
        blog_post_id INTEGER REFERENCES blog_posts(id) ON DELETE CASCADE,
        tag_id INTEGER REFERENCES blog_tags(id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(blog_post_id, tag_id)
    );
    
    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_blog_posts_category ON blog_posts(category_id);
    CREATE INDEX IF NOT EXISTS idx_blog_posts_status ON blog_posts(status);
    CREATE INDEX IF NOT EXISTS idx_blog_posts_published_at ON blog_posts(published_at DESC);
    CREATE INDEX IF NOT EXISTS idx_blog_posts_featured ON blog_posts(featured);
    CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON blog_posts(slug);
    CREATE INDEX IF NOT EXISTS idx_blog_post_products_post_id ON blog_post_products(blog_post_id);
    CREATE INDEX IF NOT EXISTS idx_blog_post_products_product_id ON blog_post_products(product_id);
    CREATE INDEX IF NOT EXISTS idx_blog_post_tags_post_id ON blog_post_tags(blog_post_id);
    
    -- Create update trigger for blog_posts
    CREATE OR REPLACE FUNCTION update_blog_posts_updated_at()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER blog_posts_updated_at_trigger
        BEFORE UPDATE ON blog_posts
        FOR EACH ROW
        EXECUTE FUNCTION update_blog_posts_updated_at();
    
    -- Create update trigger for blog_categories
    CREATE OR REPLACE FUNCTION update_blog_categories_updated_at()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER blog_categories_updated_at_trigger
        BEFORE UPDATE ON blog_categories
        FOR EACH ROW
        EXECUTE FUNCTION update_blog_categories_updated_at();
    """
    
    insert_sample_data = """
    -- Insert default blog categories
    INSERT INTO blog_categories (name, slug, description, icon, color, sort_order) VALUES
    ('Buying Guide', 'buying-guide', 'Expert advice on choosing the right instruments', '🛒', '#3B82F6', 1),
    ('Reviews', 'reviews', 'In-depth reviews of musical instruments and gear', '⭐', '#10B981', 2),
    ('Tutorial', 'tutorial', 'Learn how to play, maintain, and get the most from your instruments', '📚', '#F59E0B', 3),
    ('History', 'history', 'Stories behind iconic instruments and music industry milestones', '🏛️', '#8B5CF6', 4)
    ON CONFLICT (slug) DO NOTHING;
    
    -- Insert some sample tags
    INSERT INTO blog_tags (name, slug) VALUES
    ('Electric Guitars', 'electric-guitars'),
    ('Acoustic Guitars', 'acoustic-guitars'),
    ('Bass', 'bass'),
    ('Keyboards', 'keyboards'),
    ('Beginner', 'beginner'),
    ('Professional', 'professional'),
    ('Recording', 'recording'),
    ('Live Performance', 'live-performance'),
    ('Maintenance', 'maintenance'),
    ('Vintage', 'vintage')
    ON CONFLICT (slug) DO NOTHING;
    
    -- Insert a sample blog post
    INSERT INTO blog_posts (
        title, 
        slug, 
        excerpt, 
        content, 
        category_id, 
        status, 
        seo_title, 
        seo_description,
        reading_time,
        featured,
        published_at
    ) VALUES (
        'The Ultimate Guide to Choosing Your First Electric Guitar',
        'ultimate-guide-first-electric-guitar',
        'Discover everything you need to know about selecting the perfect electric guitar for beginners, from body styles to pickup types.',
        '# The Ultimate Guide to Choosing Your First Electric Guitar

## Introduction

Starting your electric guitar journey can be overwhelming with so many options available. This comprehensive guide will help you make an informed decision when selecting your first electric guitar.

## Body Styles

### Stratocaster Style
The Stratocaster body style is perfect for beginners due to its comfortable contours and versatility.

### Les Paul Style  
Les Paul guitars offer a chunky, warm tone perfect for rock and blues.

## Pickup Types

### Single Coil Pickups
Single coil pickups provide bright, crisp tones but can be susceptible to noise.

### Humbucker Pickups
Humbuckers offer a fuller, warmer sound with less noise interference.

## Budget Considerations

For beginners, we recommend starting with a guitar in the $300-800 range to get good quality without breaking the bank.

## Our Top Recommendations

Based on our extensive testing, here are our top picks for beginner electric guitars.

## Conclusion

Remember, the best guitar is the one that feels comfortable in your hands and inspires you to play. Take your time, try different options, and choose based on your musical preferences.',
        (SELECT id FROM blog_categories WHERE slug = 'buying-guide'),
        'published',
        'Best Electric Guitars for Beginners 2024 - Complete Buying Guide',
        'Expert guide to choosing your first electric guitar. Compare Fender, Gibson, and other top brands. Read our comprehensive beginner buyer guide.',
        8,
        true,
        CURRENT_TIMESTAMP
    ) ON CONFLICT (slug) DO NOTHING;
    """
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("Creating blog system tables...")
        await conn.execute(create_tables_sql)
        print("✓ Blog system tables created successfully!")
        
        print("Inserting sample data...")
        await conn.execute(insert_sample_data)
        print("✓ Sample blog data inserted!")
        
        await conn.close()
        
    except Exception as e:
        print(f"Error creating blog system: {e}")
        raise

async def main():
    """Main migration function"""
    print(f"Starting blog system migration at {datetime.now()}")
    await create_blog_system()
    print("Blog system migration completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())