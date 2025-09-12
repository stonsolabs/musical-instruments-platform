"""Enhance blog system for AI generation

Revision ID: 008_enhance_blog_for_ai
Revises: 007_create_blog_system
Create Date: 2024-01-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '008_enhance_blog_for_ai'
down_revision = '007_create_blog_system'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add AI generation fields to blog_posts
    op.add_column('blog_posts', sa.Column('generated_by_ai', sa.Boolean(), server_default='false'))
    op.add_column('blog_posts', sa.Column('generation_prompt', sa.Text(), nullable=True))
    op.add_column('blog_posts', sa.Column('generation_model', sa.String(length=100), nullable=True))
    op.add_column('blog_posts', sa.Column('generation_params', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('blog_posts', sa.Column('ai_notes', sa.Text(), nullable=True))

    # Create blog generation templates table
    op.create_table(
        'blog_generation_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('template_type', sa.String(length=50), server_default='general'),
        sa.Column('base_prompt', sa.Text(), nullable=False),
        sa.Column('system_prompt', sa.Text(), nullable=True),
        sa.Column('product_context_prompt', sa.Text(), nullable=True),
        sa.Column('required_product_types', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('min_products', sa.Integer(), server_default='0'),
        sa.Column('max_products', sa.Integer(), server_default='10'),
        sa.Column('suggested_tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('seo_title_template', sa.String(length=255), nullable=True),
        sa.Column('seo_description_template', sa.Text(), nullable=True),
        sa.Column('content_structure', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("template_type IN ('general', 'buying_guide', 'review', 'comparison', 'tutorial', 'history')", name='blog_templates_type_check'),
        sa.ForeignKeyConstraint(['category_id'], ['blog_categories.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create blog generation history table
    op.create_table(
        'blog_generation_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('blog_post_id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=True),
        sa.Column('generation_status', sa.String(length=50), server_default='pending'),
        sa.Column('prompt_used', sa.Text(), nullable=True),
        sa.Column('model_used', sa.String(length=100), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('generation_time_ms', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('generation_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("generation_status IN ('pending', 'generating', 'completed', 'failed', 'cancelled')", name='blog_generation_status_check'),
        sa.ForeignKeyConstraint(['blog_post_id'], ['blog_posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['template_id'], ['blog_generation_templates.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create blog content sections table
    op.create_table(
        'blog_content_sections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('blog_post_id', sa.Integer(), nullable=False),
        sa.Column('section_type', sa.String(length=100), nullable=False),
        sa.Column('section_title', sa.String(length=255), nullable=True),
        sa.Column('section_content', sa.Text(), nullable=False),
        sa.Column('section_order', sa.Integer(), server_default='0'),
        sa.Column('products_featured', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ai_generated', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['blog_post_id'], ['blog_posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Enhanced product association columns
    op.add_column('blog_post_products', sa.Column('ai_context', sa.Text(), nullable=True))
    op.add_column('blog_post_products', sa.Column('relevance_score', sa.Numeric(precision=3, scale=2), nullable=True))
    op.add_column('blog_post_products', sa.Column('mentioned_in_sections', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    # Create indexes
    op.create_index('idx_blog_posts_generated_by_ai', 'blog_posts', ['generated_by_ai'])
    op.create_index('idx_blog_generation_templates_type', 'blog_generation_templates', ['template_type'])
    op.create_index('idx_blog_generation_templates_category', 'blog_generation_templates', ['category_id'])
    op.create_index('idx_blog_generation_history_status', 'blog_generation_history', ['generation_status'])
    op.create_index('idx_blog_content_sections_post_id', 'blog_content_sections', ['blog_post_id'])
    op.create_index('idx_blog_content_sections_type', 'blog_content_sections', ['section_type'])
    op.create_index('idx_blog_post_products_relevance', 'blog_post_products', [sa.text('relevance_score DESC')])

    # Create update trigger for blog_generation_templates
    op.execute("""
        CREATE OR REPLACE FUNCTION update_blog_generation_templates_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER blog_generation_templates_updated_at_trigger
            BEFORE UPDATE ON blog_generation_templates
            FOR EACH ROW
            EXECUTE FUNCTION update_blog_generation_templates_updated_at();
    """)


def downgrade() -> None:
    # Drop trigger
    op.execute("DROP TRIGGER IF EXISTS blog_generation_templates_updated_at_trigger ON blog_generation_templates;")
    op.execute("DROP FUNCTION IF EXISTS update_blog_generation_templates_updated_at();")
    
    # Drop indexes
    op.drop_index('idx_blog_post_products_relevance')
    op.drop_index('idx_blog_content_sections_type')
    op.drop_index('idx_blog_content_sections_post_id')
    op.drop_index('idx_blog_generation_history_status')
    op.drop_index('idx_blog_generation_templates_category')
    op.drop_index('idx_blog_generation_templates_type')
    op.drop_index('idx_blog_posts_generated_by_ai')
    
    # Remove columns from blog_post_products
    op.drop_column('blog_post_products', 'mentioned_in_sections')
    op.drop_column('blog_post_products', 'relevance_score')
    op.drop_column('blog_post_products', 'ai_context')
    
    # Drop tables
    op.drop_table('blog_content_sections')
    op.drop_table('blog_generation_history')
    op.drop_table('blog_generation_templates')
    
    # Remove columns from blog_posts
    op.drop_column('blog_posts', 'ai_notes')
    op.drop_column('blog_posts', 'generation_params')
    op.drop_column('blog_posts', 'generation_model')
    op.drop_column('blog_posts', 'generation_prompt')
    op.drop_column('blog_posts', 'generated_by_ai')