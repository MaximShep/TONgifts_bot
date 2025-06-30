# scheduler.py
from datetime import datetime, timedelta
import asyncio
from aiogram import Bot
from database.repository import get_active_deals, update_deal_status, get_user_language
from locales import get_text
from utils.keyboards import close_keyboard


class DealScheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.is_running = False

    async def check_timeouts(self):
        while True:
            active_deals = get_active_deals()

            for deal in active_deals:
                try:
                    seller_lang=get_user_language(deal.seller_id)
                    await self.bot.send_message(
                        chat_id=deal.seller_id,
                        text=get_text('deal_time_out', seller_lang).format(deal_id=deal.id),
                        reply_markup = close_keyboard(seller_lang))
                    buyer_lang = get_user_language(deal.seller_id)
                    await self.bot.send_message(
                        chat_id=deal.buyer_id,
                        text=get_text('deal_time_out', buyer_lang).format(deal_id=deal.id),
                        reply_markup=close_keyboard(buyer_lang))
                    update_deal_status(deal.id, 'time_out')
                except Exception as e:
                    print(f"Ошибка уведомления: {e}")

            await asyncio.sleep(600)  # Проверка каждую минуту

    async def start(self):
        if not self.is_running:
            self.is_running = True
            asyncio.create_task(self.check_timeouts())