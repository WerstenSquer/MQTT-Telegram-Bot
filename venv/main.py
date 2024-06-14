import asyncio
from aiogram import Bot, Dispatcher, types

from cmds_list import private
from handlers import user_router

TOKEN = '6759032280:AAETYeIQshz0ma72NbM4tS-hnhbbTST86PI'
ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(user_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) # удаление команд для их переназначения
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())