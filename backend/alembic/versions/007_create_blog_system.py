"""Create blog system

Revision ID: 007_create_blog_system
Revises: 006_add_instrument_requests
Create Date: 2024-01-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '007_create_blog_system'
down_revision = '006_add_instrument_requests'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Blog categories table
    op.create_table(
        'blog_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('sort_order', sa.Integer(), server_default='0'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )

    # Blog posts table
    op.create_table(
        'blog_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('excerpt', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('featured_image', sa.Text(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('author_name', sa.String(length=100), server_default='GetYourMusicGear Team'),
        sa.Column('author_email', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=20), server_default='draft'),
        sa.Column('seo_title', sa.String(length=255), nullable=True),
        sa.Column('seo_description', sa.Text(), nullable=True),
        sa.Column('reading_time', sa.Integer(), nullable=True),
        sa.Column('view_count', sa.Integer(), server_default='0'),
        sa.Column('featured', sa.Boolean(), server_default='false'),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("status IN ('draft', 'published', 'archived')", name='blog_posts_status_check'),
        sa.ForeignKeyConstraint(['category_id'], ['blog_categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # Blog tags table
    op.create_table(
        'blog_tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )

    # Blog post products (many-to-many relationship)
    op.create_table(
        'blog_post_products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('blog_post_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('position', sa.Integer(), server_default='0'),
        sa.Column('context', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['blog_post_id'], ['blog_posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('blog_post_id', 'product_id', name='uq_blog_post_product')
    )

    # Blog post tags (many-to-many relationship)
    op.create_table(
        'blog_post_tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('blog_post_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['blog_post_id'], ['blog_posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['blog_tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('blog_post_id', 'tag_id', name='uq_blog_post_tag')
    )

    # Create indexes
    op.create_index('idx_blog_posts_category', 'blog_posts', ['category_id'])
    op.create_index('idx_blog_posts_status', 'blog_posts', ['status'])
    op.create_index('idx_blog_posts_published_at', 'blog_posts', [sa.text('published_at DESC')])
    op.create_index('idx_blog_posts_featured', 'blog_posts', ['featured'])
    op.create_index('idx_blog_posts_slug', 'blog_posts', ['slug'])
    op.create_index('idx_blog_post_products_post_id', 'blog_post_products', ['blog_post_id'])
    op.create_index('idx_blog_post_products_product_id', 'blog_post_products', ['product_id'])
    op.create_index('idx_blog_post_tags_post_id', 'blog_post_tags', ['blog_post_id'])

    # Create update triggers
    op.execute("""
        CREATE OR REPLACE FUNCTION update_blog_posts_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER blog_posts_updated_at_trigger
            BEFORE UPDATE ON blog_posts
            FOR EACH ROW
            EXECUTE FUNCTION update_blog_posts_updated_at();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_blog_categories_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER blog_categories_updated_at_trigger
            BEFORE UPDATE ON blog_categories
            FOR EACH ROW
            EXECUTE FUNCTION update_blog_categories_updated_at();
    """)

    # Insert default blog categories
    op.execute("""
        INSERT INTO blog_categories (name, slug, description, icon, color, sort_order) VALUES
        ('Buying Guide', 'buying-guide', 'Expert advice on choosing the right instruments', '🛒', '#3B82F6', 1),
        ('Reviews', 'reviews', 'In-depth reviews of musical instruments and gear', '⭐', '#10B981', 2),
        ('Tutorial', 'tutorial', 'Learn how to play, maintain, and get the most from your instruments', '📚', '#F59E0B', 3),
        ('History', 'history', 'Stories behind iconic instruments and music industry milestones', '🏛️', '#8B5CF6', 4);
    """)

    # Insert sample tags
    op.execute("""
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
        ('Vintage', 'vintage');
    """)


def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS blog_categories_updated_at_trigger ON blog_categories;")
    op.execute("DROP TRIGGER IF EXISTS blog_posts_updated_at_trigger ON blog_posts;")
    op.execute("DROP FUNCTION IF EXISTS update_blog_categories_updated_at();")
    op.execute("DROP FUNCTION IF EXISTS update_blog_posts_updated_at();")
    
    # Drop indexes
    op.drop_index('idx_blog_post_tags_post_id')
    op.drop_index('idx_blog_post_products_product_id')
    op.drop_index('idx_blog_post_products_post_id')
    op.drop_index('idx_blog_posts_slug')
    op.drop_index('idx_blog_posts_featured')
    op.drop_index('idx_blog_posts_published_at')
    op.drop_index('idx_blog_posts_status')
    op.drop_index('idx_blog_posts_category')
    
    # Drop tables
    op.drop_table('blog_post_tags')
    op.drop_table('blog_post_products')
    op.drop_table('blog_tags')
    op.drop_table('blog_posts')
    op.drop_table('blog_categories')