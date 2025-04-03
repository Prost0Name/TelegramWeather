import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN
from weather import get_weather
from database.users import add_user

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    await message.answer(
        "Напиши название города для получения погоды"
    )


@dp.message()
async def get_weather_for_city(message: Message):
    city = message.text
    try:
        weather_data = await get_weather(city)
        await message.answer(weather_data)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
        await message.answer("Пожалуйста, проверьте название города и попробуйте снова.")

async def setup():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(setup()) 