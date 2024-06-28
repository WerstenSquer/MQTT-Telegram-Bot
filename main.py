import asyncio

import tg_bot
from tg_bot import get_topic_list

async def main():
    await tg_bot.tg_bot_start()

asyncio.run(main())