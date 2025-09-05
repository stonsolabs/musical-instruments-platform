"""
Database migration to create instrument_requests table
Run this script to add the instrument requests functionality
"""

import asyncio
import asyncpg
import os
from datetime import datetime

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/musicgear_db')

async def create_instrument_requests_table():
    """Create the instrument_requests table"""
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS instrument_requests (
        id SERIAL PRIMARY KEY,
        brand VARCHAR(100) NOT NULL,
        name VARCHAR(200) NOT NULL,
        model VARCHAR(100),
        category VARCHAR(100) NOT NULL,
        store_link TEXT,
        additional_info TEXT,
        status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewing', 'approved', 'rejected', 'completed')),
        user_email VARCHAR(255),
        user_ip VARCHAR(45),
        priority INTEGER DEFAULT 1,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reviewed_at TIMESTAMP,
        completed_at TIMESTAMP,
        
        -- Indexes for better query performance
        CONSTRAINT unique_brand_name_model UNIQUE (brand, name, model)
    );
    
    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_instrument_requests_status ON instrument_requests(status);
    CREATE INDEX IF NOT EXISTS idx_instrument_requests_category ON instrument_requests(category);
    CREATE INDEX IF NOT EXISTS idx_instrument_requests_created_at ON instrument_requests(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_instrument_requests_priority ON instrument_requests(priority DESC);
    
    -- Create trigger for updated_at
    CREATE OR REPLACE FUNCTION update_instrument_requests_updated_at()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER instrument_requests_updated_at_trigger
        BEFORE UPDATE ON instrument_requests
        FOR EACH ROW
        EXECUTE FUNCTION update_instrument_requests_updated_at();
    """
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("Creating instrument_requests table...")
        await conn.execute(create_table_sql)
        print("✓ instrument_requests table created successfully!")
        
        # Insert some example categories if they don't exist
        insert_example_data = """
        INSERT INTO instrument_requests (brand, name, model, category, store_link, additional_info, status, priority)
        VALUES 
            ('Fender', 'Player Telecaster', 'Butterscotch Blonde', 'electric-guitars', 'https://www.fender.com/en-US/electric-guitars/telecaster/player-telecaster/0145212550.html', 'Popular Fender electric guitar model', 'completed', 5),
            ('Gibson', 'Les Paul Studio', '2024', 'electric-guitars', 'https://www.gibson.com/en-US/Electric-Guitar/USELPS024EBCH1/Ebony', 'Classic Gibson Les Paul in Studio configuration', 'approved', 4),
            ('Yamaha', 'FG830', 'Natural', 'acoustic-guitars', 'https://usa.yamaha.com/products/musical_instruments/guitars_basses/acoustic_guitars/fg_series/fg830.html', 'Popular beginner acoustic guitar', 'pending', 3)
        ON CONFLICT (brand, name, model) DO NOTHING;
        """
        
        await conn.execute(insert_example_data)
        print("✓ Example instrument requests added!")
        
        await conn.close()
        
    except Exception as e:
        print(f"Error creating instrument_requests table: {e}")
        raise

async def main():
    """Main migration function"""
    print(f"Starting instrument requests table migration at {datetime.now()}")
    await create_instrument_requests_table()
    print("Migration completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())