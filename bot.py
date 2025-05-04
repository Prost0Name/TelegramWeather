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
from weather import get_weather, get_weather_by_coords
from database.users import add_user, add_notification, get_notifications, delete_notification
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
    await message.answer("Давайте добавим новую рассылку. Введите город:")
    await state.set_state(NotificationSetup.waiting_for_city)

@dp.message(StateFilter(NotificationSetup.waiting_for_city))
async def process_city(message: Message, state: FSMContext):
    city = message.text
    try:
        await get_weather(city)
        await state.update_data(city=city)
        await message.answer(
            f"Город {city} принят. Теперь укажите время для уведомлений в формате ЧЧ:ММ (например, 08:00)")
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
    await add_notification(message.from_user.id, city, time_text)
    await message.answer(
        f"Рассылка добавлена! Вы будете получать прогноз погоды для города {city} каждый день в {time_text}.\n\n"
        f"Посмотреть все свои рассылки: /my_notifications\nУдалить рассылку: /delete_notification")
    await state.clear()

@dp.message(Command("my_notifications"))
async def cmd_my_notifications(message: Message):
    notifs = await get_notifications(message.from_user.id)
    if not notifs:
        await message.answer("У вас нет активных рассылок. Добавьте через /setup.")
        return
    text = "Ваши рассылки:\n"
    for n in notifs:
        text += f"ID: {n.id} | Город: {n.city} | Время: {n.notification_time}\n"
    await message.answer(text)

@dp.message(Command("delete_notification"))
async def cmd_delete_notification(message: Message, state: FSMContext):
    notifs = await get_notifications(message.from_user.id)
    if not notifs:
        await message.answer("У вас нет рассылок для удаления.")
        return
    text = "Введите ID рассылки, которую хотите удалить.\n"
    for n in notifs:
        text += f"ID: {n.id} | Город: {n.city} | Время: {n.notification_time}\n"
    await message.answer(text)
    await state.set_state("waiting_for_delete_id")

@dp.message(StateFilter("waiting_for_delete_id"))
async def process_delete_id(message: Message, state: FSMContext):
    try:
        notif_id = int(message.text.strip())
        await delete_notification(message.from_user.id, notif_id)
        await message.answer("Рассылка удалена!")
    except Exception:
        await message.answer("Ошибка! Проверьте ID и попробуйте снова.")
    await state.clear()

@dp.message(Command("weather"))
async def cmd_weather(message: Message):
    await message.answer("Напишите название города для получения текущей погоды")

@dp.message(F.location)
async def get_weather_for_location(message: Message):
    location = message.location
    if location is None:
        await message.answer("Не удалось получить координаты. Попробуйте снова.")
        return
    try:
        weather_data = await get_weather_by_coords(location.latitude, location.longitude)
        await message.answer(weather_data)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
        await message.answer("Не удалось получить погоду по координатам. Попробуйте позже.")


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