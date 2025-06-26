from aiogram import Router, F
import asyncio
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from handlers.deals import BuyerStates
from ton_service import TonService
from database.repository import update_deal_status, get_deal_by_id
from utils.keyboards import create_payment_keyboard
from config import Config
from utils.nft_checker import check_nft_owner
from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode


router = Router()
ton_service = TonService()


@router.callback_query(F.data.startswith("start_payment_"))
async def start_payment(callback: CallbackQuery, state: FSMContext):
    deal_id = callback.data.split("_")[2]
    deal = get_deal_by_id(deal_id)
    load_dotenv(".env")
    amount = deal.comission_price  # Комиссия 5%
    comment = f"DEAL_{deal.id}"

    await callback.message.answer(
        f"💰 Переведите *{amount}* TON на адрес:\n"
        f"`{Config.ADMIN_TON_ADDRESS}`\n\n"    
        f"⚠️ Обязательно введите комментарий (мемо): `{comment}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_payment_keyboard(deal.id)
    )

    # Уведомление продавца через callback.message.bot (без прямого импорта bot) [[8]]
    await callback.message.bot.send_message(
        chat_id=deal.seller_id,
        text="Покупатель начал оплату. Ожидайте подтверждения."
    )
    await state.set_state(BuyerStates.wait_payment_confirmation)  # Состояние ожидания подтверждения [[6]]


@router.callback_query(F.data.startswith("confirm_payment_"))
async def confirm_payment(callback: CallbackQuery):
    deal_id = callback.data.split("_")[2]  # Извлекаем ID сделки [[8]]
    deal = get_deal_by_id(deal_id)

    if not deal:
        await callback.answer("Сделка не найдена!")
        print(f"Сделка {deal_id} не найдена в БД")  # Для отладки [[3]]
        return

    if ton_service.check_payment(deal.id, deal.comission_price):
        await callback.message.answer("☑️ Оплата подтверждена! Ожидайте передачи NFT... \nЕсли подарок не передадут в течение 10 минут, средства вернутся к вам на счет")
        await callback.message.bot.send_message(chat_id=deal.seller_id, text="🎁 Оплата получена. Передайте NFT покупателю.")
        asyncio.create_task(monitor_nft_transfer(deal, callback))
    else:
        await callback.message.answer("Платеж не обнаружен. Проверьте комментарий и сумму.")



async def monitor_nft_transfer(deal, callback: CallbackQuery):
    """
    Проверяет каждые 3 секунды, был ли передан NFT покупателю.
    Если NFT не передан в течение 10 минут, отменяет сделку.
    """
    max_time = 600  # 10 минут (в секундах)
    interval = 3  # Интервал проверки (в секундах)
    elapsed_time = 0

    while elapsed_time < max_time:
        # Проверяем владельца NFT
        nft_owner = check_nft_owner(deal.gift_name)  # Получаем текущего владельца NFT
        buyer_username = callback.from_user.username
        
        if nft_owner == buyer_username: #buyer_username:
            # NFT успешно передан покупателю
            await confirm_gift(deal, callback)
            return
        
        await asyncio.sleep(interval)
        elapsed_time += interval

    # Если прошло 10 минут, а NFT не передан
    update_deal_status(deal.id, "canceled")
    await callback.message.answer("Время истекло. NFT не был передан. Деньги возвращены.")
    await ton_service.refund_payment(deal.buyer_address, deal.comission_price)  # Возврат средств
async def confirm_gift(deal, callback: CallbackQuery):
    """
    Подтверждает получение NFT и переводит средства продавцу.
    """
    await callback.message.bot.send_message(
            chat_id=deal.buyer_id,
            text=f"✅ NFT получен! Сделка завершена\n\nНовости об обновлениях Mivelon Garant в [официальном канале](https://t.me/mivelon) 🚀",
            parse_mode=ParseMode.MARKDOWN   
        )

    success = await ton_service.transfer_funds(deal.ton_address, deal.price, deal.id)
    if success:
        update_deal_status(deal.id, "completed")
        await callback.message.bot.send_message(
            chat_id=deal.seller_id,
            text=f"✅ Сделка завершена! Вам переведено {deal.price} TON\n\nНовости об обновлениях Mivelon Garant в [официальном канале](https://t.me/mivelon) 🚀",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await callback.message.bot.send_message(
            chat_id=deal.seller_id,
            text="Ошибка перевода средств. Свяжитесь с поддержкой."
        )