import asyncio

from src.database.connection import populate
from src.database.populate import add_to_db
from src.file_manager.dump_data import make_dump
from src.scripts.parser import scrape


async def main():
    await populate()

    data = await scrape()
    await add_to_db(data)
    await make_dump()


if __name__ == "__main__":
    asyncio.run(main())
