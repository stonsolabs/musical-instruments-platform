"""
Database migration to create batch blog generation system
Run this script to add the batch functionality
"""

import asyncio
import asyncpg
import os
from datetime import datetime

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/musicgear_db')

async def create_batch_system():
    """Create the batch generation system tables"""
    
    create_tables_sql = """
    -- Blog batch jobs table
    CREATE TABLE IF NOT EXISTS blog_batch_jobs (
        id SERIAL PRIMARY KEY,
        batch_id VARCHAR(255) NOT NULL UNIQUE,
        batch_name VARCHAR(255) NOT NULL,
        request_count INTEGER NOT NULL DEFAULT 0,
        status VARCHAR(50) DEFAULT 'created' CHECK (status IN ('created', 'uploading', 'uploaded', 'running', 'completed', 'failed')),
        
        -- File paths (Azure Storage)
        batch_file_path TEXT,
        metadata_file_path TEXT,
        results_file_path TEXT,
        
        -- Azure OpenAI Batch API info
        azure_batch_id VARCHAR(255),
        input_file_id VARCHAR(255),
        output_file_id VARCHAR(255),
        error_file_id VARCHAR(255),
        
        -- Timestamps
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        azure_created_at TIMESTAMP,
        completed_at TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        -- Request counts from Azure
        total_requests INTEGER DEFAULT 0,
        completed_requests INTEGER DEFAULT 0,
        failed_requests INTEGER DEFAULT 0,
        
        -- Additional metadata
        metadata JSONB,
        error_message TEXT,
        
        -- Creator info
        created_by_email VARCHAR(255),
        
        UNIQUE(azure_batch_id)
    );
    
    -- Blog batch processing history table
    CREATE TABLE IF NOT EXISTS blog_batch_processing_history (
        id SERIAL PRIMARY KEY,
        batch_id VARCHAR(255) REFERENCES blog_batch_jobs(batch_id) ON DELETE CASCADE,
        successful_count INTEGER DEFAULT 0,
        failed_count INTEGER DEFAULT 0,
        successful_posts JSONB, -- Array of created post info
        failed_posts JSONB,     -- Array of failed post info
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        processing_time_ms INTEGER,
        auto_published BOOLEAN DEFAULT FALSE
    );
    
    -- Enhanced blog_posts table for batch tracking
    ALTER TABLE blog_posts ADD COLUMN IF NOT EXISTS batch_id VARCHAR(255);
    ALTER TABLE blog_posts ADD COLUMN IF NOT EXISTS batch_custom_id VARCHAR(255);
    
    -- Enhanced blog_generation_history for batch support
    ALTER TABLE blog_generation_history ADD COLUMN IF NOT EXISTS batch_id VARCHAR(255);
    ALTER TABLE blog_generation_history ADD COLUMN IF NOT EXISTS batch_custom_id VARCHAR(255);
    ALTER TABLE blog_generation_history ADD COLUMN IF NOT EXISTS processing_type VARCHAR(50) DEFAULT 'single' CHECK (processing_type IN ('single', 'batch'));
    
    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_blog_batch_jobs_batch_id ON blog_batch_jobs(batch_id);
    CREATE INDEX IF NOT EXISTS idx_blog_batch_jobs_status ON blog_batch_jobs(status);
    CREATE INDEX IF NOT EXISTS idx_blog_batch_jobs_azure_batch_id ON blog_batch_jobs(azure_batch_id);
    CREATE INDEX IF NOT EXISTS idx_blog_batch_jobs_created_by ON blog_batch_jobs(created_by_email);
    CREATE INDEX IF NOT EXISTS idx_blog_posts_batch_id ON blog_posts(batch_id);
    CREATE INDEX IF NOT EXISTS idx_blog_generation_history_batch_id ON blog_generation_history(batch_id);
    
    -- Create update trigger for blog_batch_jobs
    CREATE OR REPLACE FUNCTION update_blog_batch_jobs_updated_at()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER blog_batch_jobs_updated_at_trigger
        BEFORE UPDATE ON blog_batch_jobs
        FOR EACH ROW
        EXECUTE FUNCTION update_blog_batch_jobs_updated_at();
    """
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("Creating batch generation system tables...")
        await conn.execute(create_tables_sql)
        print("✓ Batch generation system tables created successfully!")
        
        await conn.close()
        
    except Exception as e:
        print(f"Error creating batch system: {e}")
        raise

async def main():
    """Main migration function"""
    print(f"Starting batch system migration at {datetime.now()}")
    await create_batch_system()
    print("Batch system migration completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())