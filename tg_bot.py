from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import redis

import kbds
import mqtt_sub
from mqtt_sub import dict_msg_info, client
from cmds_list import private

TOKEN = '6759032280:AAETYeIQshz0ma72NbM4tS-hnhbbTST86PI'
ALLOWED_UPDATES = ['message', 'edited_message']
MSG_SEND_INTERVAL = 10

bot = Bot(token=TOKEN)
dp = Dispatcher()
user_router = Router()
dp.include_router(user_router)
chat_id = 0

r = redis.Redis(host='localhost', port=6379, db=0)

async def send_info():
    if dict_msg_info and chat_id != 0:
        main_message = ''
        for key, value in dict_msg_info.items():
            main_message += 'topic: ' + key + '\n'
            for param in value:
                main_message += param + '\n'
            main_message += '\n'

        await bot.send_message(chat_id, main_message)

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(send_info, trigger='interval', seconds=MSG_SEND_INTERVAL)

async def tg_bot_start():
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) # удаление команд для их переназначения
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

def get_topic_list():
    topic_list = []
    global chat_id
    for mac in r.smembers(chat_id):
        topic = 'DEVICES/' + str(mac)[2:19] + '/INFO/'
        topic_list.append(topic)
    return topic_list

class Start(StatesGroup):
    start = State()

class AddMAC(StatesGroup):
    address = State()

class DelMAC(StatesGroup):
    address = State()

@user_router.message(StateFilter(None), Command('start'))
async def start_cmd(message: types.Message, state: FSMContext):
    global chat_id
    chat_id = message.chat.id
    mqtt_sub.mqtt_run(get_topic_list())
    await message.answer(
        'Пользователь с ID:' + (str)(message.from_user.id), reply_markup=kbds.start_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Выберите действие')
    )
    await state.set_state(Start.start)

@user_router.message(StateFilter(Start.start), Command('add'))
@user_router.message(StateFilter(Start.start), F.text == 'Добавить MAC-адрес')
async def add_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите MAC-адрес устройства для добавления', reply_markup=kbds.cancel_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Введите MAC-адрес устройства')
    )
    await state.set_state(AddMAC.address)

@user_router.message(StateFilter(Start.start), Command('delete'))
@user_router.message(StateFilter(Start.start), F.text == 'Удалить MAC-адрес')
async def add_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите MAC-адрес устройства для удаления', reply_markup=kbds.cancel_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Введите MAC-адрес устройства')
    )
    await state.set_state(DelMAC.address)

@user_router.message(StateFilter(AddMAC.address), Command('cancel'))
@user_router.message(StateFilter(AddMAC.address), F.text == 'Отмена')
async def cancel_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        'Добавление MAC-адреса устройства отменено', reply_markup=kbds.start_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Выберите действие')
    )
    await state.clear()
    await state.set_state(Start.start)

@user_router.message(StateFilter(DelMAC.address), Command('cancel'))
@user_router.message(StateFilter(DelMAC.address), F.text == 'Отмена')
async def cancel_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        'Удаление MAC-адреса устройства отменено', reply_markup=kbds.start_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Выберите действие')
    )
    await state.clear()
    await state.set_state(Start.start)

@user_router.message(StateFilter(AddMAC.address), AddMAC.address, F.text)
async def add_cmd(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    try:
        await r.sadd((str)(message.from_user.id), message.text)
    except:
        pass
    await message.answer(
        'MAC-адрес добавлен', reply_markup=kbds.start_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Выберите действие')
    )
    await state.clear()
    await state.set_state(Start.start)
    mqtt_sub.update(get_topic_list())

@user_router.message(StateFilter(DelMAC.address), DelMAC.address, F.text)
async def delete_cmd(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    try:
        await r.srem((str)(message.from_user.id), message.text)
    except:
        pass
    await message.answer(
        'MAC-адрес удален', reply_markup=kbds.start_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Выберите действие')
    )
    await state.clear()
    await state.set_state(Start.start)
    del_topic = 'DEVICES/' + message.text + '/INFO/'
    mqtt_sub.unsubscribe(del_topic)

@user_router.message(StateFilter(Start.start), Command('see_mac'))
@user_router.message(StateFilter(Start.start), F.text == 'Просмотреть MAC-адреса')
async def see_mac_cmd(message: types.Message):
    text = r.smembers((str)(message.from_user.id))
    for mac in text:
        await message.answer(mac)

@user_router.message(StateFilter(Start.start), F.text)
async def add_cmd(message: types.Message):
    await message.answer(
        'Выберите действие', reply_markup=kbds.start_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Выберите действие')
    )

