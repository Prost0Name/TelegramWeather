import logging
from typing import List, Optional, Tuple, Dict, Any
from database.models import Users

logger = logging.getLogger(__name__)

async def get_user_by_telegram_id(telegram_id: int) -> Optional[Users]:
    try:
        user = await Users.filter(telegram_id=telegram_id).first()
        return user
    except Exception as e:
        logger.error(f"Ошибка при поиске пользователя {telegram_id}: {e}")
        return None

async def add_user(user_id: int, username: Optional[str], first_name: Optional[str], last_name: Optional[str]) -> None:
    try:
        existing_user = await get_user_by_telegram_id(user_id)
        
        if existing_user:
            logger.info(f"Пользователь {user_id} уже существует в базе данных")
            return
            
        new_users = Users(
            telegram_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        await new_users.save()
        
        logger.info(f"Создан новый пользователь: {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при добавлении {user_id}: {e}")
        raise

async def update_user_city(user_id: int, city: str) -> None:
    try:
        user = await get_user_by_telegram_id(user_id)
        if user:
            user.city = city
            await user.save()
            logger.info(f"Обновлен город для пользователя {user_id}: {city}")
        else:
            logger.error(f"Пользователь {user_id} не найден")
    except Exception as e:
        logger.error(f"Ошибка при обновлении города для {user_id}: {e}")
        raise

async def update_user_notification_time(user_id: int, time: str) -> None:
    try:
        user = await get_user_by_telegram_id(user_id)
        if user:
            user.notification_time = time
            user.notifications_enabled = True
            await user.save()
            logger.info(f"Обновлено время уведомлений для пользователя {user_id}: {time}")
        else:
            logger.error(f"Пользователь {user_id} не найден")
    except Exception as e:
        logger.error(f"Ошибка при обновлении времени уведомлений для {user_id}: {e}")
        raise

async def get_users_for_notifications(current_time: str) -> List[Users]:
    try:
        users = await Users.filter(notification_time=current_time, notifications_enabled=True)
        return users
    except Exception as e:
        logger.error(f"Ошибка при получении пользователей для уведомлений: {e}")
        return []