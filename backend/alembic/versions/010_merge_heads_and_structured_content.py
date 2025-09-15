"""Merge multiple heads and ensure structured_content

Revision ID: 010_merge_heads
Revises: 009_extend_template_types, 009_create_batch_system, 009_structured_content
Create Date: 2025-09-15 00:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '010_merge_heads'
down_revision = (
    '009_extend_template_types',
    '009_create_batch_system',
    '009_structured_content',
)
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Safety: ensure structured_content exists even if branch order differs.
    # Use IF NOT EXISTS to avoid duplicate column errors during merge.
    op.execute("ALTER TABLE blog_posts ADD COLUMN IF NOT EXISTS structured_content JSONB")


def downgrade() -> None:
    # Do not drop on merge downgrade; leave column in place
    pass
