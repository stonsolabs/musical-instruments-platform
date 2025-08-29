"""Enhance affiliate system with store availability and affiliate link management

Revision ID: 003
Revises: 002
Create Date: 2024-12-01 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add affiliate program management fields to affiliate_stores table
    op.add_column('affiliate_stores', sa.Column('has_affiliate_program', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('affiliate_stores', sa.Column('affiliate_base_url', sa.Text(), nullable=True))
    op.add_column('affiliate_stores', sa.Column('affiliate_id', sa.String(100), nullable=True))
    op.add_column('affiliate_stores', sa.Column('affiliate_parameters', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'))
    
    # Add store availability control fields
    op.add_column('affiliate_stores', sa.Column('show_affiliate_buttons', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('affiliate_stores', sa.Column('priority', sa.Integer(), nullable=False, server_default='0'))
    
    # Create indexes for new fields
    op.create_index(op.f('ix_affiliate_stores_has_affiliate_program'), 'affiliate_stores', ['has_affiliate_program'], unique=False)
    op.create_index(op.f('ix_affiliate_stores_show_affiliate_buttons'), 'affiliate_stores', ['show_affiliate_buttons'], unique=False)
    op.create_index(op.f('ix_affiliate_stores_priority'), 'affiliate_stores', ['priority'], unique=False)
    



def downgrade() -> None:
    # Drop indexes from affiliate_stores
    op.drop_index(op.f('ix_affiliate_stores_priority'), table_name='affiliate_stores')
    op.drop_index(op.f('ix_affiliate_stores_show_affiliate_buttons'), table_name='affiliate_stores')
    op.drop_index(op.f('ix_affiliate_stores_has_affiliate_program'), table_name='affiliate_stores')
    
    # Drop columns from affiliate_stores
    op.drop_column('affiliate_stores', 'priority')
    op.drop_column('affiliate_stores', 'show_affiliate_buttons')
    op.drop_column('affiliate_stores', 'affiliate_parameters')
    op.drop_column('affiliate_stores', 'affiliate_id')
    op.drop_column('affiliate_stores', 'affiliate_base_url')
    op.drop_column('affiliate_stores', 'has_affiliate_program')
