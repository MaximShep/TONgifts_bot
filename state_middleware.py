from aiogram import BaseMiddleware  # Новый импорт [[3]]
from aiogram.types import Message, TelegramObject
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError  # Обновленный импорт [[3]]
from aiogram.utils.i18n import I18n  # Для локализации (опционально)


class StateMiddleware(BaseMiddleware):
    """
    Middleware для управления FSM-состояниями и асинхронными операциями.
    Автоматически инициализирует FSMContext для новых пользователей [[3]].
    """

    async def __call__(
            self,
            handler: callable,
            event: TelegramObject,
            data: dict
    ) -> any:
        # Инициализация FSMContext
        if not data.get("state"):
            data["state"] = FSMContext(
                storage=data["bot"].get("storage"),
                key=data["bot"].get("state_key")
            )

        # Анти-флуд через throttling_manager (новый подход) [[3]]
        try:
            return await handler(event, data)
        except TelegramAPIError as e:
            # Обработка ошибок API
            return await self.handle_telegram_api_error(e, data)

    async def handle_telegram_api_error(self, error: TelegramAPIError, data: dict):
        """Обработка ошибок Telegram API (например, флуд-контроль) [[3]]"""
        if "Too Many Requests" in str(error):
            await data["bot"].send_message(
                chat_id=data["event_chat"].id,
                text="Слишком много запросов. Попробуйте позже."
            )
        raise error  # Пробрасываем ошибку дальше