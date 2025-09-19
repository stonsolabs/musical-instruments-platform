"""Simplify blog system - remove complex tables and use single JSONB column

Revision ID: 012_simplify_blog_system
Revises: 011_noindex_to_blog_posts
Create Date: 2025-09-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '012_simplify_blog_system'
down_revision = '011_noindex'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop complex blog tables that we don't need anymore (order matters for foreign keys)
    op.drop_table('blog_content_sections')
    op.drop_table('blog_post_products')
    op.drop_table('blog_post_tags')
    op.drop_table('blog_tags')
    op.drop_table('blog_generation_history')  # Drop this first (has FK to templates)
    op.drop_table('blog_generation_templates')
    
    # Simplify blog_posts table - keep only essential columns
    with op.batch_alter_table('blog_posts') as batch_op:
        # Remove unnecessary columns
        batch_op.drop_column('category_id')
        batch_op.drop_column('author_email')
        batch_op.drop_column('reading_time')
        batch_op.drop_column('view_count')
        batch_op.drop_column('featured')
        
        # Rename structured_content to content_json for clarity
        batch_op.alter_column('structured_content', new_column_name='content_json')
        
        # Make content_json the primary content field (content becomes fallback)
        batch_op.alter_column('content', nullable=True)
    
    # Drop blog_categories table as well - we'll use tags in JSON instead
    op.drop_table('blog_categories')
    
    # Drop unused indexes (if they exist)
    try:
        op.drop_index('idx_blog_posts_category')
    except:
        pass
    try:
        op.drop_index('idx_blog_posts_featured')
    except:
        pass
    
    # Drop unused triggers
    op.execute("DROP TRIGGER IF EXISTS blog_categories_updated_at_trigger ON blog_categories;")
    op.execute("DROP FUNCTION IF EXISTS update_blog_categories_updated_at();")
    
    # Create simple blog_templates table
    op.create_table(
        'blog_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('structure', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Insert default templates
    op.execute("""
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
    """)


def downgrade() -> None:
    # This is a destructive migration - we cannot restore the complex structure
    # without data loss. In a production environment, you would need to 
    # backup data before running this migration.
    pass