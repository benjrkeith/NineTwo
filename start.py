import asyncio

from ninetwo import NineTwo
from config import TOKEN


async def main():
    bot = NineTwo()
    await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
