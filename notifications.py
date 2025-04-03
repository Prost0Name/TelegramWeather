import asyncio
import logging
import datetime
from aiogram import Bot
from database.users import get_users_for_notifications
from weather import get_weather

logger = logging.getLogger(__name__)

async def send_weather_notifications(bot: Bot):
    while True:
        try:
            current_time = datetime.datetime.now().strftime("%H:%M")
            
            users = await get_users_for_notifications(current_time)
            
            for user in users:
                if user.city:
                    try:
                        weather_data = await get_weather(user.city)
                        await bot.send_message(user.telegram_id, 
                                              f"Ваш ежедневный прогноз погоды:\n\n{weather_data}")
                        logger.info(f"Отправлено уведомление о погоде пользователю {user.telegram_id}")
                    except Exception as e:
                        logger.error(f"Ошибка при отправке уведомления пользователю {user.telegram_id}: {e}")
            
            await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"Ошибка в процессе отправки уведомлений: {e}")
            await asyncio.sleep(60) 