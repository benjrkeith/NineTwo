import asyncio

from database import Database
from ninetwo import NineTwo
from config import TOKEN


async def main():
    db = Database()
    await db.initialise()

    bot = NineTwo(db)
    await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
