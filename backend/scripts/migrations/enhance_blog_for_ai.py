"""
Enhanced blog system for AI-generated content with improved product associations
Run this script to add AI generation capabilities to the blog system
"""

import asyncio
import asyncpg
import os
from datetime import datetime

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/musicgear_db')

async def enhance_blog_system():
    """Add AI generation capabilities to the blog system"""
    
    enhance_tables_sql = """
    -- Add AI generation fields to blog_posts
    ALTER TABLE blog_posts ADD COLUMN IF NOT EXISTS generated_by_ai BOOLEAN DEFAULT FALSE;
    ALTER TABLE blog_posts ADD COLUMN IF NOT EXISTS generation_prompt TEXT;
    ALTER TABLE blog_posts ADD COLUMN IF NOT EXISTS generation_model VARCHAR(100);
    ALTER TABLE blog_posts ADD COLUMN IF NOT EXISTS generation_params JSONB;
    ALTER TABLE blog_posts ADD COLUMN IF NOT EXISTS ai_notes TEXT;
    
    -- Create blog generation templates table
    CREATE TABLE IF NOT EXISTS blog_generation_templates (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT,
        category_id INTEGER REFERENCES blog_categories(id),
        template_type VARCHAR(50) DEFAULT 'general' CHECK (template_type IN ('general', 'buying_guide', 'review', 'comparison', 'tutorial', 'history')),
        base_prompt TEXT NOT NULL,
        system_prompt TEXT,
        product_context_prompt TEXT, -- How to incorporate products
        required_product_types JSONB, -- Array of category/subcategory requirements
        min_products INTEGER DEFAULT 0,
        max_products INTEGER DEFAULT 10,
        suggested_tags JSONB, -- Array of suggested tags
        seo_title_template VARCHAR(255),
        seo_description_template TEXT,
        content_structure JSONB, -- JSON schema for content sections
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create blog generation history table
    CREATE TABLE IF NOT EXISTS blog_generation_history (
        id SERIAL PRIMARY KEY,
        blog_post_id INTEGER REFERENCES blog_posts(id) ON DELETE CASCADE,
        template_id INTEGER REFERENCES blog_generation_templates(id),
        generation_status VARCHAR(50) DEFAULT 'pending' CHECK (generation_status IN ('pending', 'generating', 'completed', 'failed', 'cancelled')),
        prompt_used TEXT,
        model_used VARCHAR(100),
        tokens_used INTEGER,
        generation_time_ms INTEGER,
        error_message TEXT,
        generation_metadata JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Enhanced product association with AI context
    ALTER TABLE blog_post_products ADD COLUMN IF NOT EXISTS ai_context TEXT; -- AI's reason for including this product
    ALTER TABLE blog_post_products ADD COLUMN IF NOT EXISTS relevance_score DECIMAL(3,2); -- 0.00 to 1.00 relevance score
    ALTER TABLE blog_post_products ADD COLUMN IF NOT EXISTS mentioned_in_sections JSONB; -- Which sections mention this product
    
    -- Create blog content sections table for structured content
    CREATE TABLE IF NOT EXISTS blog_content_sections (
        id SERIAL PRIMARY KEY,
        blog_post_id INTEGER REFERENCES blog_posts(id) ON DELETE CASCADE,
        section_type VARCHAR(100) NOT NULL, -- 'introduction', 'buying_guide', 'product_comparison', 'conclusion', etc.
        section_title VARCHAR(255),
        section_content TEXT NOT NULL,
        section_order INTEGER DEFAULT 0,
        products_featured JSONB, -- Array of product IDs featured in this section
        ai_generated BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_blog_posts_generated_by_ai ON blog_posts(generated_by_ai);
    CREATE INDEX IF NOT EXISTS idx_blog_generation_templates_type ON blog_generation_templates(template_type);
    CREATE INDEX IF NOT EXISTS idx_blog_generation_templates_category ON blog_generation_templates(category_id);
    CREATE INDEX IF NOT EXISTS idx_blog_generation_history_status ON blog_generation_history(generation_status);
    CREATE INDEX IF NOT EXISTS idx_blog_content_sections_post_id ON blog_content_sections(blog_post_id);
    CREATE INDEX IF NOT EXISTS idx_blog_content_sections_type ON blog_content_sections(section_type);
    CREATE INDEX IF NOT EXISTS idx_blog_post_products_relevance ON blog_post_products(relevance_score DESC);
    
    -- Create update triggers
    CREATE OR REPLACE FUNCTION update_blog_generation_templates_updated_at()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER blog_generation_templates_updated_at_trigger
        BEFORE UPDATE ON blog_generation_templates
        FOR EACH ROW
        EXECUTE FUNCTION update_blog_generation_templates_updated_at();
    """
    
    insert_sample_templates = """
    -- Insert default blog generation templates
    INSERT INTO blog_generation_templates (
        name, description, category_id, template_type, base_prompt, system_prompt, 
        product_context_prompt, required_product_types, min_products, max_products,
        suggested_tags, seo_title_template, seo_description_template, content_structure
    ) VALUES 
    (
        'Buying Guide Template',
        'Comprehensive buying guide for musical instruments',
        (SELECT id FROM blog_categories WHERE slug = 'buying-guide'),
        'buying_guide',
        'Write a comprehensive buying guide for {category} instruments. Focus on what beginners and experienced players should consider when purchasing. Include key features, price ranges, and recommendations.',
        'You are an expert musical instrument advisor with 20+ years of experience helping musicians choose the right gear. Write informative, helpful, and engaging content that helps readers make informed purchasing decisions.',
        'For each featured product, explain why it''s recommended, what makes it special, who it''s best for, and how it compares to alternatives in its price range. Include specific technical details and practical considerations.',
        '["guitars", "keyboards", "drums", "brass", "woodwinds", "strings"]',
        3,
        8,
        '["buying-guide", "beginner", "professional", "gear-guide", "recommendations"]',
        'Best {category} {year} - Complete Buying Guide',
        'Expert buying guide for {category} instruments. Compare top brands, features, and prices. Find the perfect instrument for your skill level and budget.',
        '{"sections": ["introduction", "key_considerations", "price_ranges", "top_recommendations", "buying_tips", "conclusion"]}'
    ),
    (
        'Product Review Template', 
        'In-depth product review template',
        (SELECT id FROM blog_categories WHERE slug = 'reviews'),
        'review',
        'Write a detailed review of the {product_name}. Cover build quality, sound, playability, value for money, and who this instrument is best suited for. Include pros and cons.',
        'You are a professional music gear reviewer with extensive hands-on experience. Provide honest, detailed, and balanced reviews that help musicians make informed decisions.',
        'Focus on the main product being reviewed, but include comparisons with similar alternatives. Explain what sets this product apart and in what scenarios it excels or falls short.',
        '["same_category"]',
        1,
        3,
        '["review", "hands-on", "sound-quality", "build-quality", "value"]',
        '{product_name} Review {year} - Is It Worth It?',
        'Comprehensive review of the {product_name}. Sound quality, build, pros/cons, and value analysis from our expert team.',
        '{"sections": ["overview", "build_quality", "sound_performance", "features", "pros_cons", "verdict"]}'
    ),
    (
        'Comparison Guide Template',
        'Compare multiple products in the same category',
        (SELECT id FROM blog_categories WHERE slug = 'buying-guide'),
        'comparison',
        'Compare and contrast {product_count} popular {category} instruments. Create a detailed comparison covering features, sound, build quality, price, and value. Help readers choose the best option for their needs.',
        'You are an expert instrument reviewer who specializes in detailed product comparisons. Present fair, balanced comparisons that highlight each product''s strengths and ideal use cases.',
        'For each product in the comparison, provide specific details about features, sound characteristics, build quality, and value proposition. Use comparison tables where helpful.',
        '["same_category"]',
        2,
        5,
        '["comparison", "vs", "guide", "features", "specifications"]',
        '{product_1} vs {product_2} vs {product_3} - Which Is Best?',
        'Detailed comparison of top {category} instruments. Features, sound, build quality, and value analysis to help you choose the right instrument.',
        '{"sections": ["introduction", "comparison_table", "detailed_analysis", "use_cases", "recommendations", "conclusion"]}'
    ),
    (
        'Tutorial Guide Template',
        'Educational content about instruments and techniques',
        (SELECT id FROM blog_categories WHERE slug = 'tutorial'),
        'tutorial',
        'Create a tutorial about {topic} for {skill_level} musicians. Include step-by-step instructions, common mistakes to avoid, and recommended gear.',
        'You are an experienced music educator who excels at breaking down complex concepts into easy-to-understand steps. Make learning engaging and accessible.',
        'Recommend specific products that are ideal for this tutorial or skill level. Explain why these particular instruments or accessories are recommended for learners.',
        '["tutorial_relevant"]',
        1,
        4,
        '["tutorial", "how-to", "technique", "learning", "education"]',
        'How to {topic} - Complete Guide for {skill_level}',
        'Learn {topic} with our step-by-step guide. Tips, techniques, and gear recommendations for {skill_level} musicians.',
        '{"sections": ["introduction", "prerequisites", "step_by_step", "common_mistakes", "gear_recommendations", "next_steps"]}'
    ),
    (
        'Historical Article Template',
        'Historical and cultural content about instruments',
        (SELECT id FROM blog_categories WHERE slug = 'history'),
        'history',
        'Write about the history and cultural significance of {topic}. Include key historical moments, influential musicians, and how the instrument/genre evolved over time.',
        'You are a music historian and cultural expert who brings historical context to life through engaging storytelling. Make history interesting and relevant to modern musicians.',
        'Feature vintage and historically significant instruments, as well as modern recreations. Explain the connection between historical context and today''s instruments.',
        '["vintage", "historical", "cultural_significance"]',
        0,
        3,
        '["history", "vintage", "culture", "evolution", "heritage"]',
        'The History of {topic} - From Origins to Modern Day',
        'Explore the fascinating history of {topic}. Key moments, influential musicians, and evolution from historical origins to modern instruments.',
        '{"sections": ["origins", "key_periods", "influential_figures", "evolution", "modern_legacy", "conclusion"]}'
    )
    ON CONFLICT (name) DO NOTHING;
    """
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("Enhancing blog system for AI generation...")
        await conn.execute(enhance_tables_sql)
        print("✓ Blog system enhanced successfully!")
        
        print("Inserting AI generation templates...")
        await conn.execute(insert_sample_templates)
        print("✓ AI generation templates created!")
        
        await conn.close()
        
    except Exception as e:
        print(f"Error enhancing blog system: {e}")
        raise

async def main():
    """Main enhancement function"""
    print(f"Starting blog AI enhancement at {datetime.now()}")
    await enhance_blog_system()
    print("Blog AI enhancement completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())