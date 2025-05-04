import asyncio
import logging
import datetime
from aiogram import Bot
from database.users import get_notifications_for_time, get_user_by_telegram_id
from weather import get_weather

logger = logging.getLogger(__name__)

async def send_weather_notifications(bot: Bot):
    while True:
        try:
            current_time = datetime.datetime.now().strftime("%H:%M")
            notifications = await get_notifications_for_time(current_time)
            for notif in notifications:
                try:
                    user = await get_user_by_telegram_id(notif.user_id)
                    if user:
                        weather_data = await get_weather(notif.city)
                        await bot.send_message(user.telegram_id,
                                              f"Ваш ежедневный прогноз погоды для {notif.city} в {notif.notification_time}:\n\n{weather_data}")
                        logger.info(f"Отправлено уведомление о погоде пользователю {user.telegram_id} для {notif.city}")
                except Exception as e:
                    logger.error(f"Ошибка при отправке уведомления пользователю {notif.user_id}: {e}")
            await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"Ошибка в процессе отправки уведомлений: {e}")
            await asyncio.sleep(60) 