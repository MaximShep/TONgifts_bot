from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest

from handlers.deals import BuyerStates
from locales import get_text
from ton_service import TonService
from database.repository import update_deal_status, get_deal_by_id, get_user_language, get_username, \
    add_referral_revenue, revenue_update, update_last_activity, get_deal_by_hex
from utils.keyboards import create_payment_keyboard, close_keyboard, \
    transfer_nft, create_back_to_menu_keyboard, support_button  # Если нужна клавиатура для других действий
from config import Config
from utils.nft_checker import check_nft_owner
import asyncio
from database.repository import session  # Для доступа к сессии
from database.models import User  # Для работы с моделью User


router = Router()
ton_service = TonService()


@router.callback_query(F.data.startswith("start_payment_"))
async def start_payment(callback: CallbackQuery, state: FSMContext):
    deal_id = callback.data.split("_")[2]
    deal = get_deal_by_id(deal_id)
    user_lang = get_user_language(callback.from_user.id)
    if not deal:
        await callback.answer(get_text('deal_not_found', user_lang))
        return

    if deal.status == 'canceled' or deal.status == 'time_out':
        user_lang = get_user_language(callback.message.from_user.id)
        await callback.message.answer(
            caption=get_text('canceled', user_lang)
        )
        return

    telegram_id = callback.from_user.id
    user_lang = get_user_language(telegram_id)
    await update_last_activity(telegram_id)

    amount = deal.comission_price
    comment = f"DEAL_{deal.id}"
    update_deal_status(deal.id, "start_payment")

    await callback.message.answer(
        get_text('send_ton_payment', user_lang).format(
            amount=amount,
            ton_address=Config.ADMIN_TON_ADDRESS,
            comment=comment,
            deal_id=deal.id,
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=create_payment_keyboard(int(amount * 10 ** 9), comment, user_lang)
    )

    # Запуск автоматической проверки платежа
    asyncio.create_task(automatic_payment_monitor(callback, deal))

    seller_lang = get_user_language(deal.seller_id)

    # Уведомление продавца
    await callback.message.bot.send_message(
        chat_id=deal.seller_id,
        text=get_text('payment_started_notification', seller_lang),
        reply_markup=close_keyboard(seller_lang)
    )


async def automatic_payment_monitor(callback: CallbackQuery, deal):
    """Автоматически проверяет оплату каждые 3 секунды"""
    max_time = 900  # 15 минут
    interval = 5  # Интервал проверки
    deal_id = callback.data.split("_")[2]  # Извлекаем ID сделки [[8]]
    deal = get_deal_by_id(deal_id)
    print(deal_id)

    for _ in range(max_time // interval):
        if await ton_service.check_payment(deal.id, deal.comission_price):
            await process_payment(callback, deal)
            return
        await asyncio.sleep(interval)
    buyer_lang = get_user_language(deal.buyer_id)  # Ваша функция получения языка
    seller_lang = get_user_language(deal.seller_id)  # Ваша функция получения языка

    # Если время истекло
    await callback.message.bot.send_message(
        chat_id=deal.buyer_id,
        text=get_text('payment_timeout', buyer_lang),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=close_keyboard(buyer_lang)
    )
    await callback.message.bot.send_message(
        chat_id=deal.seller_id,
        text=get_text('payment_timeout', seller_lang),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=close_keyboard(seller_lang)
    )
    update_deal_status(deal.id, "canceled")


async def process_payment(callback: CallbackQuery, deal):
    """Обрабатывает успешную оплату"""
    user_lang = get_user_language(callback.from_user.id)
    update_deal_status(deal.id, "payment_received")

    username = get_username(deal.buyer_id)

    await callback.message.answer(
        get_text('payment_confirmed', user_lang),
        parse_mode = ParseMode.HTML,

    )
    await callback.message.bot.send_message(
        chat_id=deal.seller_id,
        text=get_text('payment_received_notification', user_lang).format(username=username),
        parse_mode=ParseMode.HTML,
        reply_markup=transfer_nft(username, user_lang)  # Предполагается, что transfer_nft принимает user_lang
    )

    # Запуск проверки передачи NFT
    asyncio.create_task(monitor_nft_transfer(callback, deal))


async def monitor_nft_transfer(callback: CallbackQuery, deal):
    """Проверяет передачу NFT после оплаты"""
    user_lang = get_user_language(callback.from_user.id)
    max_time = 900  # 15 минут
    interval = 3

    for _ in range(max_time // interval):
        nft_owner = check_nft_owner(deal.gift_name[0])
        buyer_username = callback.from_user.username

        if nft_owner == buyer_username:
            await finalize_deal(callback, deal)
            return

        await asyncio.sleep(interval)

    # Возврат средств при истечении времени
    await callback.message.answer(get_text('payment_timeout_refund', user_lang))
    await ton_service.refund_payment(deal.buyer_address, deal.comission_price)
    update_deal_status(deal.id, "refunded")

async def finalize_deal(callback: CallbackQuery, deal):
    """Завершает сделку и переводит средства"""
    buyer_lang = get_user_language(deal.buyer_id)  # Ваша функция получения языка
    seller_lang = get_user_language(deal.seller_id)  # Ваша функция получения языка
    # После успешной передачи NFT
    await callback.message.bot.send_message(
        chat_id=deal.buyer_id,
        text=get_text('deal_completed_buyer', buyer_lang).format(link="https://t.me/mivelon_info"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_back_to_menu_keyboard(buyer_lang)
    )
    success = await ton_service.transfer_funds(deal.ton_address, deal.price, deal.id)
    # Ожидаем получения комиссии

    if success:
        update_deal_status(deal.id, "completed")
        fee = None
        while fee is None:
            fee = await ton_service.find_transaction(deal.id)
            if fee is None:
                await asyncio.sleep(5)  # Пауза перед повторной проверкой
            else:
                fee = fee / (10 ** 9)
        buyer = session.query(User).filter_by(telegram_id=deal.buyer_id).first()
        seller = session.query(User).filter_by(telegram_id=deal.seller_id).first()
        print(fee)
        if buyer.invited_by is not None and seller.invited_by is not None:
            referal_sum = ((deal.comission_price - fee)*Config.REFERAL_COMMISSION)/2
            our_revenue = deal.comission_price -fee- (referal_sum*2)
            add_referral_revenue(deal.buyer_id, referal_sum)
            add_referral_revenue(deal.seller_id, referal_sum)
        elif buyer.invited_by is not None:
            referal_sum = (deal.comission_price - fee)*Config.REFERAL_COMMISSION
            our_revenue = deal.comission_price - fee - referal_sum
            add_referral_revenue(deal.buyer_id, referal_sum)
        elif seller.invited_by is not None:
            referal_sum = (deal.comission_price - fee)*Config.REFERAL_COMMISSION
            our_revenue = deal.comission_price - fee - referal_sum
            add_referral_revenue(deal.seller_id, referal_sum)
        else:
            our_revenue = deal.comission_price - fee
        revenue_update(deal.id, our_revenue)
        await callback.message.bot.send_message(
            chat_id=deal.seller_id,
            text=get_text('deal_completed_seller', seller_lang).format(price=deal.price,link="https://t.me/mivelon_info"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=create_back_to_menu_keyboard(seller_lang)
        )
        await callback.message.bot.send_message(
            chat_id=-1002751170506,
            text=f"<b>Сделка #{deal.id} завершена!</b>\n\n"
                 f"🛍️ NFT: {deal.gift_name[0]}\n"
                 f"💰 Цена (без комиссии): {deal.price} TON\n\n"
                 f"Продавец: @{get_username(deal.seller_id)} [{deal.seller_id}]\n"
                 f"Покупатель: @{get_username(deal.buyer_id)} [{deal.buyer_id}]\n\n"
                 f"<b>💰 Сумма сделки (c скомиссией): {deal.comission_price} TON</b>",
            message_thread_id=4,
            parse_mode=ParseMode.HTML
        )

    else:
        await callback.message.bot.send_message(
            chat_id=deal.seller_id,
            text=get_text("transfer_money_error", seller_lang),
            reply_markup = support_button(seller_lang)
        )

        keyboard_transfererror = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Завершить сделку", callback_data=f"refresh_transfererror_{deal.id}")]
        ])
        await callback.message.bot.send_message(
            chat_id=-1002751170506,
            text=f"<b>Сделка #{deal.id} ошибка перевода!</b>\n\n"
                 f"🛍️ NFT: {deal.gift_name[0]}\n"
                 f"💰 Цена (без комиссии): {deal.price} TON\n\n"
                 f"Продавец: @{get_username(deal.seller_id)} [{deal.seller_id}]\n"
                 f"Покупатель: @{get_username(deal.buyer_id)} [{deal.buyer_id}]\n\n"
                 f"<b>💰 Сумма сделки (c скомиссией): {deal.comission_price} TON</b>",
            message_thread_id=186,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard_transfererror
        )

        @router.callback_query(F.data.startswith("refresh_transfererror_"))
        async def refresh_transfererror_handler(callback: CallbackQuery):
            deal_id = callback.data.split("_")[-1]

            # Получаем актуальные данные сделки
            deal = get_deal_by_hex(deal_id)
            update_deal_status(deal_id, 'completed')
            updated_text = (
                f"<b>Сделка #{deal.id} завершена!</b>\n\n"
                f"🛍️ NFT: {deal.gift_name[0]}\n"
                f"💰 Цена (без комиссии): {deal.price} TON\n\n"
                f"Продавец: @{get_username(deal.seller_id) if deal.seller_id is not None else '—'} [{deal.seller_id if deal.seller_id is not None else '—'}]\n"
                f"Покупатель: @{get_username(deal.buyer_id) if deal.buyer_id is not None else '—'} [{deal.buyer_id if deal.buyer_id is not None else '—'}]\n\n"
                f"<b>💰 Сумма сделки (c комиссией): {deal.comission_price} TON</b>"
            )
            try:
                if callback.message.text != updated_text or callback.message.reply_markup != callback.message.reply_markup:
                    await callback.message.edit_text(
                        text=updated_text,
                        parse_mode=ParseMode.HTML
                    )
            except TelegramBadRequest as e:
                if "message is not modified" in e.message:
                    pass
                else:
                    raise
            await callback.answer()

# from aiogram import Router, F
# import asyncio
# from aiogram.types import CallbackQuery, Message
# from aiogram.fsm.context import FSMContext
#
# from handlers.deals import BuyerStates
# from ton_service import TonService
# from database.repository import update_deal_status, get_deal_by_id
# from utils.keyboards import create_payment_keyboard
# from config import Config
# from utils.nft_checker import check_nft_owner
# from dotenv import load_dotenv
# import os
# from aiogram.enums import ParseMode
#
#
# router = Router()
# ton_service = TonService()
#
#
# @router.callback_query(F.data.startswith("start_payment_"))
# async def start_payment(callback: CallbackQuery, state: FSMContext):
#     deal_id = callback.data.split("_")[2]
#     deal = get_deal_by_id(deal_id)
#     load_dotenv(".env")
#     amount = deal.comission_price  # Комиссия 5%
#     comment = f"DEAL_{deal.id}"
#
#     await callback.message.answer(
#         f"💰 Переведите *{amount}* TON на адрес:\n"
#         f"`{Config.ADMIN_TON_ADDRESS}`\n\n"
#         f"⚠️ Обязательно введите комментарий (мемо): `{comment}`",
#         parse_mode=ParseMode.MARKDOWN,
#         reply_markup=create_payment_keyboard(deal.id)
#     )
#
#     # Уведомление продавца через callback.message.bot (без прямого импорта bot) [[8]]
#     await callback.message.bot.send_message(
#         chat_id=deal.seller_id,
#         text="Покупатель начал оплату. Ожидайте подтверждения."
#     )
#     await state.set_state(BuyerStates.wait_payment_confirmation)  # Состояние ожидания подтверждения [[6]]
#
#
# @router.callback_query(F.data.startswith("confirm_payment_"))
# async def confirm_payment(callback: CallbackQuery):
#     deal_id = callback.data.split("_")[2]  # Извлекаем ID сделки [[8]]
#     deal = get_deal_by_id(deal_id)
#
#     if not deal:
#         await callback.answer("Сделка не найдена!")
#         print(f"Сделка {deal_id} не найдена в БД")  # Для отладки [[3]]
#         return
#
#     if ton_service.check_payment(deal.id, deal.comission_price):
#         await callback.message.answer("☑️ Оплата подтверждена! Ожидайте передачи NFT... \nЕсли подарок не передадут в течение 10 минут, средства вернутся к вам на счет")
#         await callback.message.bot.send_message(chat_id=deal.seller_id, text="🎁 Оплата получена. Передайте NFT покупателю.")
#         asyncio.create_task(monitor_nft_transfer(deal, callback))
#     else:
#         await callback.message.answer("Платеж не обнаружен. Проверьте комментарий и сумму.")
#
#
#
# async def monitor_nft_transfer(deal, callback: CallbackQuery):
#     """
#     Проверяет каждые 3 секунды, был ли передан NFT покупателю.
#     Если NFT не передан в течение 10 минут, отменяет сделку.
#     """
#     max_time = 600  # 10 минут (в секундах)
#     interval = 3  # Интервал проверки (в секундах)
#     elapsed_time = 0
#
#     while elapsed_time < max_time:
#         # Проверяем владельца NFT
#         nft_owner = check_nft_owner(deal.gift_name)  # Получаем текущего владельца NFT
#         buyer_username = callback.from_user.username
#
#         if nft_owner == buyer_username: #buyer_username:
#             # NFT успешно передан покупателю
#             await confirm_gift(deal, callback)
#             return
#
#         await asyncio.sleep(interval)
#         elapsed_time += interval
#
#     # Если прошло 10 минут, а NFT не передан
#     update_deal_status(deal.id, "canceled")
#     await callback.message.answer("Время истекло. NFT не был передан. Деньги возвращены.")
#     await ton_service.refund_payment(deal.buyer_address, deal.comission_price)  # Возврат средств
# async def confirm_gift(deal, callback: CallbackQuery):
#     """
#     Подтверждает получение NFT и переводит средства продавцу.
#     """
#     await callback.message.bot.send_message(
#             chat_id=deal.buyer_id,
#             text=f"✅ NFT получен! Сделка завершена\n\nНовости об обновлениях Mivelon Garant в [официальном канале](https://t.me/mivelon) 🚀",
#             parse_mode=ParseMode.MARKDOWN
#         )
#
#     success = await ton_service.transfer_funds(deal.ton_address, deal.price, deal.id)
#     if success:
#         update_deal_status(deal.id, "completed")
#         await callback.message.bot.send_message(
#             chat_id=deal.seller_id,
#             text=f"✅ Сделка завершена! Вам переведено {deal.price} TON\n\nНовости об обновлениях Mivelon Garant в [официальном канале](https://t.me/mivelon) 🚀",
#             parse_mode=ParseMode.MARKDOWN
#         )
#     else:
#         await callback.message.bot.send_message(
#             chat_id=deal.seller_id,
#             text="Ошибка перевода средств. Свяжитесь с поддержкой."
#         )
#
