"""Add instrument requests table

Revision ID: 006_add_instrument_requests
Revises: 005_clean_voting_feature
Create Date: 2025-09-07 16:56:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '006_add_instrument_requests'
down_revision = '005_clean_voting_feature'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the instrument_requests table"""
    
    # Create instrument_requests table
    op.create_table('instrument_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('brand', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('store_link', sa.Text(), nullable=True),
        sa.Column('additional_info', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('user_email', sa.String(length=255), nullable=True),
        sa.Column('user_ip', sa.String(length=45), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('brand', 'name', 'model', name='unique_brand_name_model'),
        sa.CheckConstraint("status IN ('pending', 'reviewing', 'approved', 'rejected', 'completed')", name='instrument_requests_status_check')
    )
    
    # Create indexes
    op.create_index('idx_instrument_requests_status', 'instrument_requests', ['status'], unique=False)
    op.create_index('idx_instrument_requests_category', 'instrument_requests', ['category'], unique=False)
    op.create_index('idx_instrument_requests_created_at', 'instrument_requests', ['created_at'], unique=False)
    op.create_index('idx_instrument_requests_priority', 'instrument_requests', ['priority'], unique=False)
    
    # Create trigger function for updated_at
    op.execute("""
    CREATE OR REPLACE FUNCTION update_instrument_requests_updated_at()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # Create trigger
    op.execute("""
    CREATE TRIGGER instrument_requests_updated_at_trigger
        BEFORE UPDATE ON instrument_requests
        FOR EACH ROW
        EXECUTE FUNCTION update_instrument_requests_updated_at();
    """)


def downgrade() -> None:
    """Remove the instrument_requests table"""
    
    # Drop trigger and function
    op.execute("DROP TRIGGER IF EXISTS instrument_requests_updated_at_trigger ON instrument_requests;")
    op.execute("DROP FUNCTION IF EXISTS update_instrument_requests_updated_at();")
    
    # Drop indexes
    op.drop_index('idx_instrument_requests_priority', table_name='instrument_requests')
    op.drop_index('idx_instrument_requests_created_at', table_name='instrument_requests')
    op.drop_index('idx_instrument_requests_category', table_name='instrument_requests')
    op.drop_index('idx_instrument_requests_status', table_name='instrument_requests')
    
    # Drop table
    op.drop_table('instrument_requests')