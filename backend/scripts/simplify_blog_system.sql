-- Manual SQL script to simplify blog system
-- Run this script manually if the migration fails

BEGIN;

-- Drop complex blog tables (order matters for foreign keys)
DROP TABLE IF EXISTS blog_content_sections CASCADE;
DROP TABLE IF EXISTS blog_post_products CASCADE;
DROP TABLE IF EXISTS blog_post_tags CASCADE;
DROP TABLE IF EXISTS blog_tags CASCADE;
DROP TABLE IF EXISTS blog_generation_history CASCADE;
DROP TABLE IF EXISTS blog_generation_templates CASCADE;

-- Simplify blog_posts table - remove unnecessary columns
ALTER TABLE blog_posts 
    DROP COLUMN IF EXISTS category_id,
    DROP COLUMN IF EXISTS author_email,
    DROP COLUMN IF EXISTS reading_time,
    DROP COLUMN IF EXISTS view_count,
    DROP COLUMN IF EXISTS featured;

-- Rename structured_content to content_json for clarity
ALTER TABLE blog_posts 
    RENAME COLUMN structured_content TO content_json;

-- Make content_json the primary content field (content becomes fallback)
ALTER TABLE blog_posts 
    ALTER COLUMN content DROP NOT NULL;

-- Drop blog_categories table 
DROP TABLE IF EXISTS blog_categories CASCADE;

-- Drop unused indexes if they exist
DROP INDEX IF EXISTS idx_blog_posts_category;
DROP INDEX IF EXISTS idx_blog_posts_featured;

-- Drop unused triggers and functions
DROP TRIGGER IF EXISTS blog_categories_updated_at_trigger ON blog_categories;
DROP FUNCTION IF EXISTS update_blog_categories_updated_at();

-- Create simple blog_templates table
CREATE TABLE IF NOT EXISTS blog_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    prompt TEXT NOT NULL,
    structure JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default templates
INSERT INTO blog_templates (name, prompt, structure) VALUES
(
    'buying-guide',
    'Create a comprehensive buying guide for {topic}. Focus on helping readers choose the right product by explaining key features, comparing options, and providing clear recommendations. Include product recommendations with affiliate links naturally integrated into the content.',
    '{"sections": ["intro", "quick_picks", "buying_criteria", "detailed_reviews", "comparison", "conclusion"], "affiliate_integration": "seamless", "tone": "expert_friendly"}'
),
(
    'review',
    'Write an in-depth review of {topic}. Provide honest, detailed analysis covering performance, build quality, value for money, and who this product is best for. Include pros/cons and compare to similar products.',
    '{"sections": ["intro", "overview", "performance", "pros_cons", "comparison", "conclusion"], "affiliate_integration": "moderate", "tone": "honest_expert"}'
),
(
    'comparison',
    'Create a detailed comparison between {topic}. Help readers understand the key differences and choose the best option for their needs and budget. Include feature comparisons and clear recommendations.',
    '{"sections": ["intro", "comparison_table", "detailed_analysis", "recommendations", "conclusion"], "affiliate_integration": "high", "tone": "analytical"}'
),
(
    'artist-spotlight',
    'Write an engaging article celebrating {topic}. Tell their story, highlight their impact on music, discuss their iconic instruments and gear, and inspire readers. Include subtle product recommendations related to their signature sound.',
    '{"sections": ["intro", "biography", "musical_impact", "signature_gear", "legacy", "conclusion"], "affiliate_integration": "subtle", "tone": "celebratory_inspiring"}'
),
(
    'instrument-history',
    'Create a fascinating deep-dive into the history of {topic}. Cover its origins, evolution, key innovations, and cultural impact. Include stories about famous players and iconic moments.',
    '{"sections": ["intro", "origins", "evolution", "innovations", "cultural_impact", "famous_players", "conclusion"], "affiliate_integration": "light", "tone": "educational_engaging"}'
),
(
    'gear-tips',
    'Write practical tips and advice about {topic}. Share expert knowledge, common mistakes to avoid, maintenance tips, and how to get the best results. Make it actionable and helpful.',
    '{"sections": ["intro", "essential_tips", "common_mistakes", "maintenance", "pro_techniques", "conclusion"], "affiliate_integration": "moderate", "tone": "helpful_expert"}'
),
(
    'news-feature',
    'Create an informative news feature about {topic}. Provide context, explain why it matters to musicians, and offer expert perspective. Keep it current and engaging.',
    '{"sections": ["intro", "background", "key_details", "industry_impact", "expert_analysis", "conclusion"], "affiliate_integration": "minimal", "tone": "journalistic_informative"}'
)
ON CONFLICT (name) DO NOTHING;

-- Update alembic version table
UPDATE alembic_version SET version_num = '012_simplify_blog_system';

COMMIT;