from aiogram import F, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import redis

import kbds
import mqtt_sub

user_router = Router()
r = redis.Redis(host='localhost', port=6379, db=0)

@user_router.message(StateFilter(None), Command('start'))
async def start_cmd(message: types.Message):
    await message.answer(
        'Пользователь с ID:' + (str)(message.from_user.id), reply_markup=kbds.start_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Выберите действие')
    )

class AddMAC(StatesGroup):
    address = State()

class DelMAC(StatesGroup):
    address = State()

@user_router.message(StateFilter(None), Command('add'))
@user_router.message(StateFilter(None), F.text == 'Добавить MAC-адрес')
async def add_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите MAC-адрес устройства для добавления', reply_markup=kbds.cancel_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Введите MAC-адрес устройства')
    )
    await state.set_state(AddMAC.address)

@user_router.message(StateFilter(None), Command('delete'))
@user_router.message(StateFilter(None), F.text == 'Удалить MAC-адрес')
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

@user_router.message(StateFilter(DelMAC.address), Command('cancel'))
@user_router.message(StateFilter(DelMAC.address), F.text == 'Отмена')
async def cancel_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        'Удаление MAC-адреса устройства отменено', reply_markup=kbds.start_kbd.as_markup(resize_keyboard=True, input_field_placeholder='Выберите действие')
    )
    await state.clear()

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

@user_router.message(StateFilter(None), Command('see_mac'))
@user_router.message(StateFilter(None), F.text == 'Просмотреть MAC-адреса')
async def see_mac_cmd(message: types.Message):
    text = r.smembers((str)(message.from_user.id))
    for mac in text:
        await message.answer(mac)


