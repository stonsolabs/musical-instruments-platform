"""Create batch blog generation system

Revision ID: 009_create_batch_system
Revises: 008_enhance_blog_for_ai
Create Date: 2024-01-22 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '009_create_batch_system'
down_revision = '008_enhance_blog_for_ai'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Blog batch jobs table
    op.create_table(
        'blog_batch_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.String(length=255), nullable=False),
        sa.Column('batch_name', sa.String(length=255), nullable=False),
        sa.Column('request_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('status', sa.String(length=50), server_default='created'),
        sa.Column('batch_file_path', sa.Text(), nullable=True),
        sa.Column('metadata_file_path', sa.Text(), nullable=True),
        sa.Column('results_file_path', sa.Text(), nullable=True),
        sa.Column('azure_batch_id', sa.String(length=255), nullable=True),
        sa.Column('input_file_id', sa.String(length=255), nullable=True),
        sa.Column('output_file_id', sa.String(length=255), nullable=True),
        sa.Column('error_file_id', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('azure_created_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('total_requests', sa.Integer(), server_default='0'),
        sa.Column('completed_requests', sa.Integer(), server_default='0'),
        sa.Column('failed_requests', sa.Integer(), server_default='0'),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_by_email', sa.String(length=255), nullable=True),
        sa.CheckConstraint("status IN ('created', 'uploading', 'uploaded', 'running', 'completed', 'failed')", name='blog_batch_jobs_status_check'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('batch_id'),
        sa.UniqueConstraint('azure_batch_id')
    )

    # Blog batch processing history table
    op.create_table(
        'blog_batch_processing_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.String(length=255), nullable=False),
        sa.Column('successful_count', sa.Integer(), server_default='0'),
        sa.Column('failed_count', sa.Integer(), server_default='0'),
        sa.Column('successful_posts', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('failed_posts', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('processed_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('auto_published', sa.Boolean(), server_default='false'),
        sa.ForeignKeyConstraint(['batch_id'], ['blog_batch_jobs.batch_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Add batch tracking columns to existing tables
    op.add_column('blog_posts', sa.Column('batch_id', sa.String(length=255), nullable=True))
    op.add_column('blog_posts', sa.Column('batch_custom_id', sa.String(length=255), nullable=True))
    
    op.add_column('blog_generation_history', sa.Column('batch_id', sa.String(length=255), nullable=True))
    op.add_column('blog_generation_history', sa.Column('batch_custom_id', sa.String(length=255), nullable=True))
    op.add_column('blog_generation_history', sa.Column('processing_type', sa.String(length=50), server_default='single'))

    # Add check constraint to blog_generation_history
    op.create_check_constraint(
        'blog_generation_history_processing_type_check',
        'blog_generation_history',
        "processing_type IN ('single', 'batch')"
    )

    # Create indexes
    op.create_index('idx_blog_batch_jobs_batch_id', 'blog_batch_jobs', ['batch_id'])
    op.create_index('idx_blog_batch_jobs_status', 'blog_batch_jobs', ['status'])
    op.create_index('idx_blog_batch_jobs_azure_batch_id', 'blog_batch_jobs', ['azure_batch_id'])
    op.create_index('idx_blog_batch_jobs_created_by', 'blog_batch_jobs', ['created_by_email'])
    op.create_index('idx_blog_posts_batch_id', 'blog_posts', ['batch_id'])
    op.create_index('idx_blog_generation_history_batch_id', 'blog_generation_history', ['batch_id'])

    # Create update trigger for blog_batch_jobs
    op.execute("""
        CREATE OR REPLACE FUNCTION update_blog_batch_jobs_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER blog_batch_jobs_updated_at_trigger
            BEFORE UPDATE ON blog_batch_jobs
            FOR EACH ROW
            EXECUTE FUNCTION update_blog_batch_jobs_updated_at();
    """)


def downgrade() -> None:
    # Drop trigger
    op.execute("DROP TRIGGER IF EXISTS blog_batch_jobs_updated_at_trigger ON blog_batch_jobs;")
    op.execute("DROP FUNCTION IF EXISTS update_blog_batch_jobs_updated_at();")
    
    # Drop indexes
    op.drop_index('idx_blog_generation_history_batch_id')
    op.drop_index('idx_blog_posts_batch_id')
    op.drop_index('idx_blog_batch_jobs_created_by')
    op.drop_index('idx_blog_batch_jobs_azure_batch_id')
    op.drop_index('idx_blog_batch_jobs_status')
    op.drop_index('idx_blog_batch_jobs_batch_id')
    
    # Remove check constraint
    op.drop_constraint('blog_generation_history_processing_type_check', 'blog_generation_history')
    
    # Remove columns from existing tables
    op.drop_column('blog_generation_history', 'processing_type')
    op.drop_column('blog_generation_history', 'batch_custom_id')
    op.drop_column('blog_generation_history', 'batch_id')
    op.drop_column('blog_posts', 'batch_custom_id')
    op.drop_column('blog_posts', 'batch_id')
    
    # Drop tables
    op.drop_table('blog_batch_processing_history')
    op.drop_table('blog_batch_jobs')