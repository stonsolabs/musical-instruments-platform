"""Extend blog_generation_templates.template_type options

Revision ID: 009_extend_template_types
Revises: 008_enhance_blog_for_ai
Create Date: 2025-09-13 19:52:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '009_extend_template_types'
down_revision = '008_enhance_blog_for_ai'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop existing check constraints if they exist (name may vary by deployment)
    op.execute("ALTER TABLE blog_generation_templates DROP CONSTRAINT IF EXISTS blog_templates_type_check;")
    op.execute("ALTER TABLE blog_generation_templates DROP CONSTRAINT IF EXISTS blog_generation_templates_template_type_check;")

    # Create new check constraint including new types
    op.create_check_constraint(
        'blog_templates_type_check',
        'blog_generation_templates',
        "template_type IN ('general', 'buying_guide', 'review', 'comparison', 'tutorial', 'history', 'deals', 'quiz', 'new_release', 'artist_spotlight')",
    )


def downgrade() -> None:
    # Revert to original limited set
    op.execute("ALTER TABLE blog_generation_templates DROP CONSTRAINT IF EXISTS blog_templates_type_check;")
    op.execute("ALTER TABLE blog_generation_templates DROP CONSTRAINT IF EXISTS blog_generation_templates_template_type_check;")
    op.create_check_constraint(
        'blog_templates_type_check',
        'blog_generation_templates',
        "template_type IN ('general', 'buying_guide', 'review', 'comparison', 'tutorial', 'history')",
    )

