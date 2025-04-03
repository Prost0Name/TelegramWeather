import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from weather import get_weather
from database.users import add_user, update_user_city, update_user_notification_time
from notifications import send_weather_notifications

logging.basicConfig(level=logging.INFO)

class NotificationSetup(StatesGroup):
    waiting_for_city = State()
    waiting_for_time = State()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    await message.answer(
        "Привет! Я бот погоды. Напиши название города, чтобы узнать текущую погоду, "
        "или используй /setup для настройки ежедневных уведомлений о погоде."
    )

@dp.message(Command("setup"))
async def cmd_setup(message: Message, state: FSMContext):
    await message.answer("Давайте настроим ежедневные уведомления о погоде. В каком городе вы хотите получать прогноз?")
    await state.set_state(NotificationSetup.waiting_for_city)

@dp.message(StateFilter(NotificationSetup.waiting_for_city))
async def process_city(message: Message, state: FSMContext):
    city = message.text
    try:
        await get_weather(city)
        # Сохраняем город в состоянии
        await state.update_data(city=city)
        await update_user_city(message.from_user.id, city)
        
        await message.answer(
            f"Отлично! Город {city} установлен. Теперь укажите время для ежедневных уведомлений в формате ЧЧ:ММ (например, 08:00)"
        )
        await state.set_state(NotificationSetup.waiting_for_time)
    except Exception as e:
        await message.answer(f"Не удалось найти город {city}. Пожалуйста, проверьте название и попробуйте снова.")

@dp.message(StateFilter(NotificationSetup.waiting_for_time))
async def process_time(message: Message, state: FSMContext):
    time_text = message.text
    
    if not re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', time_text):
        await message.answer("Пожалуйста, укажите время в формате ЧЧ:ММ (например, 08:00)")
        return
    
    data = await state.get_data()
    city = data.get('city')
    
    await update_user_notification_time(message.from_user.id, time_text)
    
    await message.answer(
        f"Настройка завершена! Вы будете получать прогноз погоды для города {city} каждый день в {time_text}.\n\n"
        f"Вы можете изменить настройки в любое время с помощью команды /setup."
    )
    
    await state.clear()

@dp.message(Command("weather"))
async def cmd_weather(message: Message):
    await message.answer("Напишите название города для получения текущей погоды")

@dp.message(~F.text.startswith('/'))
async def get_weather_for_city(message: Message):
    city = message.text
    try:
        weather_data = await get_weather(city)
        await message.answer(weather_data)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
        await message.answer("Пожалуйста, проверьте название города и попробуйте снова.")

async def setup():
    asyncio.create_task(send_weather_notifications(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(setup()) 