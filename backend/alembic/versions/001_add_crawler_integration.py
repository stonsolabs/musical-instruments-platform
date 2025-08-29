"""Add crawler integration fields and tables

Revision ID: 001_crawler_integration
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_crawler_integration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add crawler fields to products table
    op.add_column('products', sa.Column('gtin12', sa.String(length=12), nullable=True))
    op.add_column('products', sa.Column('gtin13', sa.String(length=13), nullable=True))
    op.add_column('products', sa.Column('mpn', sa.String(length=100), nullable=True))
    op.add_column('products', sa.Column('category_attributes', sa.JSON(), nullable=True))
    op.add_column('products', sa.Column('last_crawled', sa.DateTime(), nullable=True))
    
    # Create indexes for the new fields
    op.create_index(op.f('ix_products_gtin12'), 'products', ['gtin12'], unique=False)
    op.create_index(op.f('ix_products_gtin13'), 'products', ['gtin13'], unique=False)
    op.create_index(op.f('ix_products_mpn'), 'products', ['mpn'], unique=False)

    # Create crawler_sessions table
    op.create_table('crawler_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.String(length=100), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=True),
    sa.Column('proxy_endpoint', sa.String(length=255), nullable=True),
    sa.Column('region', sa.String(length=50), nullable=True),
    sa.Column('request_count', sa.Integer(), nullable=True),
    sa.Column('last_request_time', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crawler_sessions_id'), 'crawler_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_crawler_sessions_session_id'), 'crawler_sessions', ['session_id'], unique=True)

    # Create crawler_metrics table
    op.create_table('crawler_metrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.String(length=100), nullable=True),
    sa.Column('request_url', sa.Text(), nullable=True),
    sa.Column('response_status', sa.Integer(), nullable=True),
    sa.Column('response_time_ms', sa.Integer(), nullable=True),
    sa.Column('success', sa.Boolean(), nullable=True),
    sa.Column('blocked', sa.Boolean(), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crawler_metrics_id'), 'crawler_metrics', ['id'], unique=False)
    op.create_index(op.f('ix_crawler_metrics_session_id'), 'crawler_metrics', ['session_id'], unique=False)

    # Create crawler_config table
    op.create_table('crawler_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('config_key', sa.String(length=100), nullable=False),
    sa.Column('config_value', sa.Text(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crawler_config_id'), 'crawler_config', ['id'], unique=False)
    op.create_index(op.f('ix_crawler_config_config_key'), 'crawler_config', ['config_key'], unique=True)

    # Create crawler_jobs table
    op.create_table('crawler_jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_name', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('products_found', sa.Integer(), nullable=True),
    sa.Column('products_saved', sa.Integer(), nullable=True),
    sa.Column('errors_count', sa.Integer(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crawler_jobs_id'), 'crawler_jobs', ['id'], unique=False)


def downgrade() -> None:
    # Drop crawler tables
    op.drop_index(op.f('ix_crawler_jobs_id'), table_name='crawler_jobs')
    op.drop_table('crawler_jobs')
    
    op.drop_index(op.f('ix_crawler_config_config_key'), table_name='crawler_config')
    op.drop_index(op.f('ix_crawler_config_id'), table_name='crawler_config')
    op.drop_table('crawler_config')
    
    op.drop_index(op.f('ix_crawler_metrics_session_id'), table_name='crawler_metrics')
    op.drop_index(op.f('ix_crawler_metrics_id'), table_name='crawler_metrics')
    op.drop_table('crawler_metrics')
    
    op.drop_index(op.f('ix_crawler_sessions_session_id'), table_name='crawler_sessions')
    op.drop_index(op.f('ix_crawler_sessions_id'), table_name='crawler_sessions')
    op.drop_table('crawler_sessions')

    # Remove crawler fields from products table
    op.drop_index(op.f('ix_products_mpn'), table_name='products')
    op.drop_index(op.f('ix_products_gtin13'), table_name='products')
    op.drop_index(op.f('ix_products_gtin12'), table_name='products')
    
    op.drop_column('products', 'last_crawled')
    op.drop_column('products', 'category_attributes')
    op.drop_column('products', 'mpn')
    op.drop_column('products', 'gtin13')
    op.drop_column('products', 'gtin12')
