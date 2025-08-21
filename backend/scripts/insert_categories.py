import asyncio
import asyncpg
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import text
from datetime import datetime


async def main():
    # Direct connection without needing the models file
    connection_string = "postgresql://admin:qQqqDgXlIuBSZDUlgqzQEcoTPBkrCjVD@dpg-d2er32qdbo4c738oofng-a.frankfurt-postgres.render.com/musicgear_db"
    
    conn = await asyncpg.connect(connection_string)
    
    # Create categories table if it doesn't exist
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            slug VARCHAR(100) UNIQUE NOT NULL,
            parent_id INTEGER REFERENCES categories(id),
            description TEXT,
            image_url TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    categories_data = [
        ("Electric Guitars", "electric-guitars", "Electric guitars for all styles and genres"),
        ("Acoustic Guitars", "acoustic-guitars", "Acoustic and classical guitars"),
        ("Bass Guitars", "bass-guitars", "Electric and acoustic bass guitars"),
        ("Drums & Percussion", "drums-percussion", "Drum kits, percussion instruments and accessories"),
        ("Pianos & Keyboards", "pianos-keyboards", "Digital pianos, keyboards and synthesizers"),
        ("Orchestral", "orchestral", "String, brass, woodwind and orchestral instruments"),
        ("Live Sound & Lighting", "live-sound-lighting", "PA systems, mixers, and stage lighting equipment"),
        ("Studio & Production", "studio-production", "Recording interfaces, monitors and studio equipment"),
        ("Music Software", "music-software", "DAWs, plugins and music production software"),
        ("DJ Equipment", "dj-equipment", "DJ controllers, turntables and mixing equipment"),
        ("Home Audio", "home-audio", "Home stereo systems, speakers and audio equipment"),
    ]
    
    for name, slug, description in categories_data:
        # Check if category already exists
        existing = await conn.fetchrow("SELECT id FROM categories WHERE slug = $1", slug)
        if existing:
            print(f"⚠️  Category already exists: {name}")
        else:
            await conn.execute(
                "INSERT INTO categories (name, slug, description, is_active, created_at) VALUES ($1, $2, $3, $4, $5)",
                name, slug, description, True, datetime.utcnow()
            )
            print(f"✅ Added category: {name}")
    
    await conn.close()
    print("✅ All categories have been processed successfully!")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())