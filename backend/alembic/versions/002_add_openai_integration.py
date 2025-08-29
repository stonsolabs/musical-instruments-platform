"""Add OpenAI integration fields

Revision ID: 002
Revises: 001
Create Date: 2024-12-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001_crawler_integration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add OpenAI fields to products table
    op.add_column('products', sa.Column('openai_product_id', sa.String(100), nullable=True))
    op.add_column('products', sa.Column('openai_processing_status', sa.String(50), nullable=False, server_default='pending'))
    op.add_column('products', sa.Column('openai_batch_id', sa.String(100), nullable=True))
    op.add_column('products', sa.Column('openai_processed_at', sa.DateTime(), nullable=True))
    op.add_column('products', sa.Column('openai_error_message', sa.Text(), nullable=True))
    
    # Create indexes for OpenAI fields
    op.create_index(op.f('ix_products_openai_product_id'), 'products', ['openai_product_id'], unique=False)
    op.create_index(op.f('ix_products_openai_batch_id'), 'products', ['openai_batch_id'], unique=False)
    
    # Update crawler_sessions table
    op.drop_column('crawler_sessions', 'user_agent')
    op.drop_column('crawler_sessions', 'proxy_endpoint')
    op.drop_column('crawler_sessions', 'region')
    op.drop_column('crawler_sessions', 'request_count')
    op.drop_column('crawler_sessions', 'last_request_time')
    
    op.add_column('crawler_sessions', sa.Column('start_time', sa.DateTime(), nullable=False, server_default=sa.text('now()')))
    op.add_column('crawler_sessions', sa.Column('end_time', sa.DateTime(), nullable=True))
    op.add_column('crawler_sessions', sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'))
    op.add_column('crawler_sessions', sa.Column('status', sa.String(50), nullable=False, server_default='running'))
    
    # Update crawler_metrics table
    op.drop_column('crawler_metrics', 'response_time_ms')
    op.alter_column('crawler_metrics', 'created_at', new_column_name='timestamp')
    
    # Update crawler_config table
    op.drop_column('crawler_config', 'config_key')
    op.drop_column('crawler_config', 'config_value')
    op.drop_column('crawler_config', 'description')
    
    op.add_column('crawler_config', sa.Column('name', sa.String(100), nullable=False))
    op.add_column('crawler_config', sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'))
    op.add_column('crawler_config', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')))
    
    op.create_index(op.f('ix_crawler_config_name'), 'crawler_config', ['name'], unique=True)
    
    # Update crawler_jobs table
    op.drop_column('crawler_jobs', 'job_name')
    op.drop_column('crawler_jobs', 'products_found')
    op.drop_column('crawler_jobs', 'products_saved')
    op.drop_column('crawler_jobs', 'errors_count')
    op.drop_column('crawler_jobs', 'started_at')
    
    op.add_column('crawler_jobs', sa.Column('job_type', sa.String(100), nullable=False))
    op.add_column('crawler_jobs', sa.Column('parameters', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='{}'))
    op.add_column('crawler_jobs', sa.Column('priority', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('crawler_jobs', sa.Column('result', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('crawler_jobs', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')))
    op.alter_column('crawler_jobs', 'completed_at', existing_type=sa.DateTime(), nullable=True)
    
    # Create openai_batches table
    op.create_table('openai_batches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.String(100), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('product_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('openai_job_id', sa.String(100), nullable=True),
        sa.Column('result_file', sa.String(255), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_openai_batches_batch_id'), 'openai_batches', ['batch_id'], unique=True)
    op.create_index(op.f('ix_openai_batches_openai_job_id'), 'openai_batches', ['openai_job_id'], unique=False)
    
    # Create product_images table
    op.create_table('product_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('original_url', sa.Text(), nullable=False),
        sa.Column('azure_blob_url', sa.Text(), nullable=True),
        sa.Column('azure_blob_name', sa.String(255), nullable=True),
        sa.Column('image_type', sa.String(50), nullable=False, server_default='product'),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('processing_status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_images_product_id'), 'product_images', ['product_id'], unique=False)


def downgrade() -> None:
    # Drop new tables
    op.drop_index(op.f('ix_product_images_product_id'), table_name='product_images')
    op.drop_table('product_images')
    
    op.drop_index(op.f('ix_openai_batches_openai_job_id'), table_name='openai_batches')
    op.drop_index(op.f('ix_openai_batches_batch_id'), table_name='openai_batches')
    op.drop_table('openai_batches')
    
    # Revert crawler_jobs changes
    op.drop_column('crawler_jobs', 'result')
    op.drop_column('crawler_jobs', 'created_at')
    op.drop_column('crawler_jobs', 'priority')
    op.drop_column('crawler_jobs', 'parameters')
    op.drop_column('crawler_jobs', 'job_type')
    
    op.add_column('crawler_jobs', sa.Column('job_name', sa.String(100), nullable=False))
    op.add_column('crawler_jobs', sa.Column('products_found', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('crawler_jobs', sa.Column('products_saved', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('crawler_jobs', sa.Column('errors_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('crawler_jobs', sa.Column('started_at', sa.DateTime(), nullable=True))
    
    # Revert crawler_config changes
    op.drop_index(op.f('ix_crawler_config_name'), table_name='crawler_config')
    op.drop_column('crawler_config', 'created_at')
    op.drop_column('crawler_config', 'config')
    op.drop_column('crawler_config', 'name')
    
    op.add_column('crawler_config', sa.Column('config_key', sa.String(100), nullable=False))
    op.add_column('crawler_config', sa.Column('config_value', sa.Text(), nullable=True))
    op.add_column('crawler_config', sa.Column('description', sa.String(255), nullable=True))
    
    # Revert crawler_metrics changes
    op.alter_column('crawler_metrics', 'timestamp', new_column_name='created_at')
    op.add_column('crawler_metrics', sa.Column('response_time_ms', sa.Integer(), nullable=True))
    
    # Revert crawler_sessions changes
    op.drop_column('crawler_sessions', 'status')
    op.drop_column('crawler_sessions', 'config')
    op.drop_column('crawler_sessions', 'end_time')
    op.drop_column('crawler_sessions', 'start_time')
    
    op.add_column('crawler_sessions', sa.Column('user_agent', sa.Text(), nullable=True))
    op.add_column('crawler_sessions', sa.Column('proxy_endpoint', sa.String(255), nullable=True))
    op.add_column('crawler_sessions', sa.Column('region', sa.String(50), nullable=True))
    op.add_column('crawler_sessions', sa.Column('request_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('crawler_sessions', sa.Column('last_request_time', sa.DateTime(), nullable=True))
    
    # Revert products changes
    op.drop_index(op.f('ix_products_openai_batch_id'), table_name='products')
    op.drop_index(op.f('ix_products_openai_product_id'), table_name='products')
    
    op.drop_column('products', 'openai_error_message')
    op.drop_column('products', 'openai_processed_at')
    op.drop_column('products', 'openai_batch_id')
    op.drop_column('products', 'openai_processing_status')
    op.drop_column('products', 'openai_product_id')
