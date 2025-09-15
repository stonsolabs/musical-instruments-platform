"""Add noindex flag to blog_posts

Revision ID: 011_noindex
Revises: 010_merge_heads
Create Date: 2025-09-15 01:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '011_noindex'
down_revision = '010_merge_heads'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('blog_posts') as batch_op:
        batch_op.add_column(sa.Column('noindex', sa.Boolean(), server_default='false', nullable=False))


def downgrade() -> None:
    with op.batch_alter_table('blog_posts') as batch_op:
        batch_op.drop_column('noindex')

