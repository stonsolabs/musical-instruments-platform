"""Enhanced affiliate system with brand exclusivity and regional preferences

Revision ID: 004_enhanced_affiliate_system
Revises: 003_enhance_affiliate_system
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004_enhanced_affiliate_system'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new fields to affiliate_stores table
    op.add_column('affiliate_stores', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('affiliate_stores', sa.Column('has_affiliate_program', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('affiliate_stores', sa.Column('affiliate_base_url', sa.Text(), nullable=True))
    op.add_column('affiliate_stores', sa.Column('affiliate_id', sa.String(100), nullable=True))
    op.add_column('affiliate_stores', sa.Column('domain_affiliate_ids', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'))
    op.add_column('affiliate_stores', sa.Column('affiliate_parameters', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'))
    op.add_column('affiliate_stores', sa.Column('show_affiliate_buttons', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('affiliate_stores', sa.Column('priority', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('affiliate_stores', sa.Column('available_regions', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('affiliate_stores', sa.Column('primary_region', sa.String(10), nullable=True))
    op.add_column('affiliate_stores', sa.Column('regional_priority', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'))
    op.add_column('affiliate_stores', sa.Column('use_store_fallback', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('affiliate_stores', sa.Column('store_fallback_url', sa.Text(), nullable=True))
    op.add_column('affiliate_stores', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')))
    
    # Create indexes for new fields
    op.create_index(op.f('ix_affiliate_stores_has_affiliate_program'), 'affiliate_stores', ['has_affiliate_program'], unique=False)
    op.create_index(op.f('ix_affiliate_stores_show_affiliate_buttons'), 'affiliate_stores', ['show_affiliate_buttons'], unique=False)
    op.create_index(op.f('ix_affiliate_stores_priority'), 'affiliate_stores', ['priority'], unique=False)
    
    # Create brand_exclusivities table
    op.create_table('brand_exclusivities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('brand_name', sa.String(100), nullable=False),
        sa.Column('store_id', sa.Integer(), nullable=False),
        sa.Column('is_exclusive', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('regions', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('priority_boost', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['store_id'], ['affiliate_stores.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('brand_name', 'store_id', name='uq_brand_store_exclusivity')
    )
    
    # Create indexes for brand_exclusivities table
    op.create_index(op.f('ix_brand_exclusivities_id'), 'brand_exclusivities', ['id'], unique=False)
    op.create_index(op.f('ix_brand_exclusivities_brand_name'), 'brand_exclusivities', ['brand_name'], unique=False)
    op.create_index(op.f('ix_brand_exclusivities_store_id'), 'brand_exclusivities', ['store_id'], unique=False)
    op.create_index(op.f('ix_brand_exclusivities_is_exclusive'), 'brand_exclusivities', ['is_exclusive'], unique=False)


def downgrade() -> None:
    # Drop brand_exclusivities table
    op.drop_index(op.f('ix_brand_exclusivities_is_exclusive'), table_name='brand_exclusivities')
    op.drop_index(op.f('ix_brand_exclusivities_store_id'), table_name='brand_exclusivities')
    op.drop_index(op.f('ix_brand_exclusivities_brand_name'), table_name='brand_exclusivities')
    op.drop_index(op.f('ix_brand_exclusivities_id'), table_name='brand_exclusivities')
    op.drop_table('brand_exclusivities')
    
    # Drop indexes from affiliate_stores
    op.drop_index(op.f('ix_affiliate_stores_priority'), table_name='affiliate_stores')
    op.drop_index(op.f('ix_affiliate_stores_show_affiliate_buttons'), table_name='affiliate_stores')
    op.drop_index(op.f('ix_affiliate_stores_has_affiliate_program'), table_name='affiliate_stores')
    
    # Drop columns from affiliate_stores
    op.drop_column('affiliate_stores', 'updated_at')
    op.drop_column('affiliate_stores', 'store_fallback_url')
    op.drop_column('affiliate_stores', 'use_store_fallback')
    op.drop_column('affiliate_stores', 'regional_priority')
    op.drop_column('affiliate_stores', 'primary_region')
    op.drop_column('affiliate_stores', 'available_regions')
    op.drop_column('affiliate_stores', 'priority')
    op.drop_column('affiliate_stores', 'show_affiliate_buttons')
    op.drop_column('affiliate_stores', 'affiliate_parameters')
    op.drop_column('affiliate_stores', 'domain_affiliate_ids')
    op.drop_column('affiliate_stores', 'affiliate_id')
    op.drop_column('affiliate_stores', 'affiliate_base_url')
    op.drop_column('affiliate_stores', 'has_affiliate_program')
    op.drop_column('affiliate_stores', 'description')
