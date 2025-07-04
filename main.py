import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from docs.conf import language
from datetime import datetime, timedelta, timezone
from database.repository import session
from aiogram.enums import ParseMode

from handlers import deals, payments, wallets, language, referal
from state_middleware import StateMiddleware
from config import Config  # Импорт класса Config из config.py [[10]]
from ton_service import TonService
from utils.scheduler import DealScheduler
from database.reporting import generate_daily_report, format_report

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
dp.include_router(referal.router)

async def daily_report_task():
    while True:
        # Текущее время в UTC
        now_utc = datetime.now(timezone.utc)

        # Московское время (UTC+3)
        tz_msk = timezone(timedelta(hours=3))
        now_msk = now_utc.astimezone(tz_msk)

        # Устанавливаем целевое время: сегодня в 23:59 MSK
        next_run_msk = now_msk.replace(hour=23, minute=59, second=0, microsecond=0)
        # next_run_msk = now_msk.replace(hour=now_msk.hour, minute=now_msk.minute + 1, second=0, microsecond=0)
        # Если время уже прошло — переносим на завтра
        if now_msk >= next_run_msk:
            next_run_msk += timedelta(days=1)

        # Переводим целевое время в UTC
        next_run_utc = next_run_msk.astimezone(timezone.utc)

        # Считаем задержку до следующего запуска
        delay = (next_run_utc - now_utc).total_seconds()
        print(f"[INFO] Отчет будет отправлен {next_run_msk.strftime('%Y-%m-%d %H:%M')} (MSK)")

        await asyncio.sleep(delay)

        try:
            report_data = generate_daily_report(session)
            report_text = format_report(report_data)

            # Отправляем отчет в указанный чат
            await bot.send_message(
                chat_id=-1002751170506,
                text=report_text,
                message_thread_id=184,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            print(f"[ERROR] Не удалось отправить отчет: {e}")


# Настройка планировщика ПОСЛЕ инициализации бота

async def main():
    # Инициализация TON-сервиса
    ton_service = TonService()
    await ton_service.initialize()  # Запуск LiteBalancer [[
    await scheduler.start()
    asyncio.create_task(daily_report_task())
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
