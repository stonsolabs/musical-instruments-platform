#!/usr/bin/env python3
"""
Create Authors Table - Creates the authors table for blog post attribution
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.database import async_session_factory
from sqlalchemy import text

async def create_authors_table():
    """Create the authors table and insert sample authors"""
    async with async_session_factory() as session:
        print("Creating authors table...")
        
        # Create authors table
        await session.execute(text('''
            CREATE TABLE IF NOT EXISTS authors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                bio TEXT,
                avatar_url VARCHAR(500),
                social_links JSONB,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''))
        
        # Create index on email
        await session.execute(text('''
            CREATE INDEX IF NOT EXISTS idx_authors_email ON authors(email)
        '''))
        
        # Create index on is_active
        await session.execute(text('''
            CREATE INDEX IF NOT EXISTS idx_authors_active ON authors(is_active)
        '''))
        
        print("✅ Authors table created successfully")
        
        # Insert sample authors
        sample_authors = [
            {
                'name': 'Alex Rodriguez',
                'email': 'alex.rodriguez@getyourmusicgear.com',
                'bio': 'Guitar expert with 15+ years of experience in rock and metal. Former touring musician and current gear reviewer.',
                'social_links': json.dumps({
                    'twitter': '@alexguitar',
                    'instagram': '@alexrodriguez_music'
                })
            },
            {
                'name': 'Sarah Chen',
                'email': 'sarah.chen@getyourmusicgear.com',
                'bio': 'Bass specialist and music educator. Passionate about helping beginners find their perfect instrument.',
                'social_links': json.dumps({
                    'youtube': 'Sarah Chen Bass',
                    'instagram': '@sarahchenbass'
                })
            },
            {
                'name': 'Marcus Johnson',
                'email': 'marcus.johnson@getyourmusicgear.com',
                'bio': 'Piano and keyboard expert with classical training. Specializes in digital pianos and synthesizers.',
                'social_links': json.dumps({
                    'twitter': '@marcuspiano',
                    'facebook': 'Marcus Johnson Music'
                })
            },
            {
                'name': 'Emma Thompson',
                'email': 'emma.thompson@getyourmusicgear.com',
                'bio': 'Acoustic guitar enthusiast and folk musician. Loves discovering hidden gems in the guitar world.',
                'social_links': json.dumps({
                    'instagram': '@emmaacoustic',
                    'youtube': 'Emma Thompson Music'
                })
            },
            {
                'name': 'David Park',
                'email': 'david.park@getyourmusicgear.com',
                'bio': 'Effects pedal guru and studio engineer. Knows everything about guitar tone and signal processing.',
                'social_links': json.dumps({
                    'twitter': '@davidpedals',
                    'instagram': '@davidpark_audio'
                })
            },
            {
                'name': 'Lisa Martinez',
                'email': 'lisa.martinez@getyourmusicgear.com',
                'bio': 'Violin and string instrument specialist. Classical musician with a passion for helping students.',
                'social_links': json.dumps({
                    'instagram': '@lisaviolin',
                    'facebook': 'Lisa Martinez Violin'
                })
            },
            {
                'name': 'James Wilson',
                'email': 'james.wilson@getyourmusicgear.com',
                'bio': 'Drum and percussion expert. Former session drummer with extensive studio experience.',
                'social_links': json.dumps({
                    'twitter': '@jamesdrums',
                    'youtube': 'James Wilson Drums'
                })
            },
            {
                'name': 'Rachel Green',
                'email': 'rachel.green@getyourmusicgear.com',
                'bio': 'Music production and home recording specialist. Helps musicians create professional recordings.',
                'social_links': json.dumps({
                    'instagram': '@rachelproduces',
                    'twitter': '@rachelmusicprod'
                })
            },
            {
                'name': 'Michael Brown',
                'email': 'michael.brown@getyourmusicgear.com',
                'bio': 'Guitar amplifier expert and tone specialist. Former amp technician with deep technical knowledge.',
                'social_links': json.dumps({
                    'youtube': 'Michael Brown Amps',
                    'instagram': '@michaelampguy'
                })
            },
            {
                'name': 'Jennifer Lee',
                'email': 'jennifer.lee@getyourmusicgear.com',
                'bio': 'Music technology and digital instruments expert. Passionate about the latest in music tech.',
                'social_links': json.dumps({
                    'twitter': '@jennifermusictech',
                    'instagram': '@jennifermusictech'
                })
            }
        ]
        
        # Insert sample authors
        for author in sample_authors:
            await session.execute(text('''
                INSERT INTO authors (name, email, bio, social_links, created_at, updated_at)
                VALUES (:name, :email, :bio, :social_links, :created_at, :updated_at)
                ON CONFLICT (email) DO NOTHING
            '''), {
                'name': author['name'],
                'email': author['email'],
                'bio': author['bio'],
                'social_links': author['social_links'],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            })
        
        await session.commit()
        print(f"✅ Inserted {len(sample_authors)} sample authors")
        
        # Verify authors were created
        result = await session.execute(text('SELECT COUNT(*) FROM authors'))
        count = result.scalar()
        print(f"✅ Total authors in database: {count}")

async def main():
    """Main function to create authors table"""
    print("🚀 Creating Authors Table")
    print("=" * 30)
    
    await create_authors_table()
    
    print("\n🎉 Authors table setup completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
