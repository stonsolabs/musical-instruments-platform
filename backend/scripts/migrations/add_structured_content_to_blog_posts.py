"""
Add structured_content JSONB to blog_posts to store full AI parts
"""

import asyncio
import asyncpg
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/musicgear_db')

SQL = """
ALTER TABLE blog_posts ADD COLUMN IF NOT EXISTS structured_content JSONB;
"""

async def main():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute(SQL)
        print("✓ Added structured_content JSONB column to blog_posts")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())

