#!/usr/bin/env python3
"""
Remove Locale Table Migration

This script removes the unused locales table since we've moved to English-only content.

Usage:
    python remove_locale_table.py --check    # Check if table exists and has data
    python remove_locale_table.py --remove   # Remove the table
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.database import async_session_factory
from sqlalchemy import text
import argparse


async def check_locale_table():
    """Check if the locales table exists and has any data"""
    async with async_session_factory() as session:
        # Check if table exists
        result = await session.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'locales'
            );
        """))
        table_exists = result.fetchone()[0]
        
        if not table_exists:
            print("✅ Locales table does not exist - nothing to remove")
            return
        
        # Check if table has any data
        result = await session.execute(text("SELECT COUNT(*) FROM locales"))
        count = result.fetchone()[0]
        
        print(f"📊 Locales table status:")
        print(f"  - Table exists: {table_exists}")
        print(f"  - Records count: {count}")
        
        if count > 0:
            # Show sample data
            result = await session.execute(text("SELECT * FROM locales LIMIT 5"))
            rows = result.fetchall()
            print(f"  - Sample data:")
            for row in rows:
                print(f"    ID: {row.id}, Code: {row.code}, Name: {row.name}, Active: {row.is_active}")


async def remove_locale_table():
    """Remove the locales table"""
    async with async_session_factory() as session:
        # Check if table exists first
        result = await session.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'locales'
            );
        """))
        table_exists = result.fetchone()[0]
        
        if not table_exists:
            print("✅ Locales table does not exist - nothing to remove")
            return
        
        # Remove the table
        await session.execute(text("DROP TABLE IF EXISTS locales CASCADE"))
        await session.commit()
        
        print("✅ Locales table removed successfully")


async def main():
    parser = argparse.ArgumentParser(description="Remove Locale Table Migration")
    parser.add_argument("--check", action="store_true", help="Check if locales table exists and has data")
    parser.add_argument("--remove", action="store_true", help="Remove the locales table")
    
    args = parser.parse_args()
    
    if args.check:
        await check_locale_table()
    elif args.remove:
        await remove_locale_table()
    else:
        print("Please specify --check or --remove")
        print("Example: python remove_locale_table.py --check")


if __name__ == "__main__":
    asyncio.run(main())
