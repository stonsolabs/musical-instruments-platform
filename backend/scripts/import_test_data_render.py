#!/usr/bin/env python3
"""
Standalone script to import test data directly to Render database
Usage: python scripts/import_test_data_render.py
"""
import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.models import Base
from app.services.data_importer import DataImporter

DATABASE_URL = "postgresql+asyncpg://admin:qQqqDgXlIuBSZDUlgqzQEcoTPBkrCjVD@dpg-d2er32qdbo4c738oofng-a.frankfurt-postgres.render.com/musicgear_db"

async def main():
    print("🔌 Connecting to Render database...")
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    print("📋 Creating database tables if they don't exist...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("📦 Importing test data...")
    async with async_session() as session:
        importer = DataImporter(session)
        await importer.import_sample_data()
    
    await engine.dispose()
    print("✅ Test data imported successfully to Render database!")

if __name__ == "__main__":
    asyncio.run(main())