"""Enhance blog system for AI generation

Revision ID: 008_enhance_blog_for_ai
Revises: 007_create_blog_system
Create Date: 2025-09-15 00:00:00.000000

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
    # Add AI fields to blog_posts
    with op.batch_alter_table('blog_posts') as batch_op:
        batch_op.add_column(sa.Column('generated_by_ai', sa.Boolean(), server_default='false'))
        batch_op.add_column(sa.Column('generation_prompt', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('generation_model', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('generation_params', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
        batch_op.add_column(sa.Column('ai_notes', sa.Text(), nullable=True))

    # Enhance blog_post_products columns for AI context
    with op.batch_alter_table('blog_post_products') as batch_op:
        batch_op.add_column(sa.Column('ai_context', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('relevance_score', sa.Numeric(3, 2), nullable=True))
        batch_op.add_column(sa.Column('mentioned_in_sections', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    # Create blog_generation_templates table
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
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.ForeignKeyConstraint(['category_id'], ['blog_categories.id'], ondelete='SET NULL')
    )

    # Create blog_generation_history table
    op.create_table(
        'blog_generation_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('blog_post_id', sa.Integer(), nullable=True),
        sa.Column('template_id', sa.Integer(), nullable=True),
        sa.Column('generation_status', sa.String(length=50), server_default='pending'),
        sa.Column('prompt_used', sa.Text(), nullable=True),
        sa.Column('model_used', sa.String(length=100), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('generation_time_ms', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('generation_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['blog_post_id'], ['blog_posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['template_id'], ['blog_generation_templates.id'], ondelete='SET NULL')
    )

    # Create blog_content_sections table
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
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['blog_post_id'], ['blog_posts.id'], ondelete='CASCADE')
    )

    # Indexes
    op.create_index('idx_blog_posts_generated_by_ai', 'blog_posts', ['generated_by_ai'])
    op.create_index('idx_blog_generation_templates_type', 'blog_generation_templates', ['template_type'])
    op.create_index('idx_blog_generation_templates_category', 'blog_generation_templates', ['category_id'])
    op.create_index('idx_blog_generation_history_status', 'blog_generation_history', ['generation_status'])
    op.create_index('idx_blog_content_sections_post_id', 'blog_content_sections', ['blog_post_id'])
    op.create_index('idx_blog_content_sections_type', 'blog_content_sections', ['section_type'])
    op.create_index('idx_blog_post_products_relevance', 'blog_post_products', ['relevance_score'])

    # Trigger for updated_at on blog_generation_templates
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_blog_generation_templates_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER blog_generation_templates_updated_at_trigger
            BEFORE UPDATE ON blog_generation_templates
            FOR EACH ROW
            EXECUTE FUNCTION update_blog_generation_templates_updated_at();
        """
    )


def downgrade() -> None:
    # Drop trigger and function
    op.execute("DROP TRIGGER IF EXISTS blog_generation_templates_updated_at_trigger ON blog_generation_templates;")
    op.execute("DROP FUNCTION IF EXISTS update_blog_generation_templates_updated_at();")

    # Drop indexes
    op.drop_index('idx_blog_post_products_relevance', table_name='blog_post_products')
    op.drop_index('idx_blog_content_sections_type', table_name='blog_content_sections')
    op.drop_index('idx_blog_content_sections_post_id', table_name='blog_content_sections')
    op.drop_index('idx_blog_generation_history_status', table_name='blog_generation_history')
    op.drop_index('idx_blog_generation_templates_category', table_name='blog_generation_templates')
    op.drop_index('idx_blog_generation_templates_type', table_name='blog_generation_templates')
    op.drop_index('idx_blog_posts_generated_by_ai', table_name='blog_posts')

    # Drop new tables
    op.drop_table('blog_content_sections')
    op.drop_table('blog_generation_history')
    op.drop_table('blog_generation_templates')

    # Remove columns from blog_post_products
    with op.batch_alter_table('blog_post_products') as batch_op:
        batch_op.drop_column('mentioned_in_sections')
        batch_op.drop_column('relevance_score')
        batch_op.drop_column('ai_context')

    # Remove columns from blog_posts
    with op.batch_alter_table('blog_posts') as batch_op:
        batch_op.drop_column('ai_notes')
        batch_op.drop_column('generation_params')
        batch_op.drop_column('generation_model')
        batch_op.drop_column('generation_prompt')
        batch_op.drop_column('generated_by_ai')

