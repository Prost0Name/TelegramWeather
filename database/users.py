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
    print(user_id, username, first_name, last_name)
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