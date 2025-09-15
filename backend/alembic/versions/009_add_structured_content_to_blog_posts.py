"""Add structured_content JSONB to blog_posts

Revision ID: 009_structured_content
Revises: 008_enhance_blog_for_ai
Create Date: 2025-09-15 00:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '009_structured_content'
down_revision = '008_enhance_blog_for_ai'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('blog_posts') as batch_op:
        batch_op.add_column(sa.Column('structured_content', postgresql.JSONB(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('blog_posts') as batch_op:
        batch_op.drop_column('structured_content')
