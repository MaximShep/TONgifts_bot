import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from docs.conf import language

from handlers import deals, payments, wallets, language
from state_middleware import StateMiddleware
from config import Config  # Импорт класса Config из config.py [[10]]
from ton_service import TonService
from utils.scheduler import DealScheduler



# Настройка логирования
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Инициализация бота и диспетчера
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()
scheduler = DealScheduler(bot)


# Подключение middleware
dp.update.middleware(StateMiddleware())

# Регистрация обработчиков
dp.include_router(wallets.router)
dp.include_router(deals.router)
dp.include_router(payments.router)
dp.include_router(language.router)

# Настройка планировщика ПОСЛЕ инициализации бота

async def main():
    # Инициализация TON-сервиса
    ton_service = TonService()
    await ton_service.initialize()  # Запуск LiteBalancer [[
    await scheduler.start()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
