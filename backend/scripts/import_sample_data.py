import asyncio
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.database import async_session_factory, init_db  # noqa: E402
from app.services.data_importer import DataImporter  # noqa: E402


async def main():
    await init_db()
    async with async_session_factory() as session:
        importer = DataImporter(session)
        await importer.import_sample_data()
    print("✅ Sample data imported successfully!")


if __name__ == "__main__":
    asyncio.run(main())


