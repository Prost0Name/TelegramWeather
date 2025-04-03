import asyncio
import database
from bot import setup


async def main():
    await database.setup()
    await setup()


if __name__ == "__main__":
    asyncio.run(main())
