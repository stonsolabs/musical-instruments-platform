"""Clean voting feature implementation

Revision ID: 005_clean_voting_feature
Revises: 004_enhanced_affiliate_system
Create Date: 2025-09-02 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005_clean_voting_feature'
down_revision = '004_enhanced_affiliate_system'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the product voting system"""
    
    # Create product_votes table
    op.create_table('product_votes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('user_ip', sa.String(length=45), nullable=False),
        sa.Column('vote_type', sa.String(length=10), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('product_id', 'user_ip', name='uq_product_user_vote'),
        sa.CheckConstraint("vote_type IN ('up', 'down')", name='product_votes_vote_type_check')
    )
    
    # Create indexes for product_votes table
    op.create_index('ix_product_votes_id', 'product_votes', ['id'], unique=False)
    op.create_index('ix_product_votes_product_id', 'product_votes', ['product_id'], unique=False)
    op.create_index('ix_product_votes_user_ip', 'product_votes', ['user_ip'], unique=False)
    op.create_index('ix_product_votes_vote_type', 'product_votes', ['vote_type'], unique=False)
    op.create_index('ix_product_votes_created_at', 'product_votes', ['created_at'], unique=False)

    # Create view for easy vote statistics calculation
    op.execute("""
    CREATE OR REPLACE VIEW product_vote_stats AS
    SELECT 
        p.id as product_id,
        COALESCE(SUM(CASE WHEN pv.vote_type = 'up' THEN 1 ELSE 0 END), 0) as thumbs_up_count,
        COALESCE(SUM(CASE WHEN pv.vote_type = 'down' THEN 1 ELSE 0 END), 0) as thumbs_down_count,
        COALESCE(COUNT(pv.id), 0) as total_votes,
        COALESCE(SUM(CASE WHEN pv.vote_type = 'up' THEN 1 ELSE 0 END), 0) - 
        COALESCE(SUM(CASE WHEN pv.vote_type = 'down' THEN 1 ELSE 0 END), 0) as vote_score
    FROM products p
    LEFT JOIN product_votes pv ON p.id = pv.product_id
    GROUP BY p.id;
    """)

    # Create helper function for vote statistics
    op.execute("""
    CREATE OR REPLACE FUNCTION get_product_vote_stats(p_product_id INTEGER)
    RETURNS TABLE(
        thumbs_up_count BIGINT,
        thumbs_down_count BIGINT, 
        total_votes BIGINT,
        vote_score BIGINT
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT 
            COALESCE(SUM(CASE WHEN vote_type = 'up' THEN 1 ELSE 0 END), 0) as thumbs_up_count,
            COALESCE(SUM(CASE WHEN vote_type = 'down' THEN 1 ELSE 0 END), 0) as thumbs_down_count,
            COALESCE(COUNT(*), 0) as total_votes,
            COALESCE(SUM(CASE WHEN vote_type = 'up' THEN 1 ELSE 0 END), 0) - 
            COALESCE(SUM(CASE WHEN vote_type = 'down' THEN 1 ELSE 0 END), 0) as vote_score
        FROM product_votes 
        WHERE product_id = p_product_id;
    END;
    $$ LANGUAGE plpgsql;
    """)


def downgrade() -> None:
    """Remove the product voting system"""
    
    # Drop function and view
    op.execute("DROP FUNCTION IF EXISTS get_product_vote_stats(INTEGER);")
    op.execute("DROP VIEW IF EXISTS product_vote_stats;")
    
    # Drop indexes
    op.drop_index('ix_product_votes_created_at', table_name='product_votes')
    op.drop_index('ix_product_votes_vote_type', table_name='product_votes')
    op.drop_index('ix_product_votes_user_ip', table_name='product_votes')
    op.drop_index('ix_product_votes_product_id', table_name='product_votes')
    op.drop_index('ix_product_votes_id', table_name='product_votes')
    
    # Drop table
    op.drop_table('product_votes')
