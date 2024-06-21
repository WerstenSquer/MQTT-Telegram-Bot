import asyncio
from aiogram import Bot, Dispatcher, types
import json

from cmds_list import private
from handlers import user_router
import mqtt_sub
from mqtt_sub import msg_user

TOKEN = '6759032280:AAETYeIQshz0ma72NbM4tS-hnhbbTST86PI'
ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(user_router)

async def main():
    mqtt_sub.mqtt_run()
    while True:
        if mqtt_sub.state_msg.state:
            json_msg = json.loads(msg_user.text)
            topic = msg_user.topic
            status = json_msg['status']
            text_for_user = "topic: " + topic + "\nstatus: " + status
            await bot.send_message(1487552706, text_for_user)
            mqtt_sub.state_msg.state = False
    mqtt_sub.mqtt_stop()

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) # удаление команд для их переназначения
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())
