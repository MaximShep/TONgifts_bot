import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from database.repository import session, get_referral_count, get_referral_revenue, \
    reset_referral_revenue  # Для доступа к сессии
from database.models import User  # Для работы с моделью User
from config import Config
from aiogram.enums import ParseMode

from database.repository import get_user_language
from handlers.deals import go_menu
from locales import get_text
from ton_service import TonService
from utils.keyboards import back_to_menu_from_ref_keyboard
from utils.reflinks import encode_telegram_id

router = Router()
ton_service = TonService()


# --- Обработчик реферальной программы ---
@router.callback_query(F.data == "referral")
async def process_referral(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id)
    user = session.query(User).filter_by(telegram_id=user_id).first()

    if not user:
        return

    link = f"https://t.me/{Config.BOT_USERNAME}?start=ref_{encode_telegram_id(user_id)}"
    wallets = user.wallets
    count_of_referrals = get_referral_count(user_id)
    revenue = get_referral_revenue(user_id)

    if user_id in Config.VIP_IDS:
        text = get_text('referral_program', user_lang).format(
            link=link,
            count=count_of_referrals,
            revenue=revenue,
            commission=Config.REFERAL_COMMISSION_VIP * 100,
            active_wallet=user.active_wallet if wallets else get_text('no_wallets', user_lang)
        )
    else:
        text = get_text('referral_program', user_lang).format(
            link=link,
            count=count_of_referrals,
            revenue=revenue,
            commission=Config.REFERAL_COMMISSION * 100,
            active_wallet=user.active_wallet if wallets else get_text('no_wallets', user_lang)
        )

    await callback.message.answer_photo(
        photo=FSInputFile("assets/referal.png"),
        caption=text,
        parse_mode=ParseMode.HTML,
        reply_markup=back_to_menu_from_ref_keyboard(user_lang)
    )


# --- Обработчик вывода средств ---
@router.callback_query(F.data == "money_ref")
async def give_me_my_refs(callback: CallbackQuery):
    user_lang = get_user_language(callback.from_user.id)
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()

    if not user:
        return

    if user.ref_revenue >= 1 and user.wallets:
        await ton_service.refund_payment(user.active_wallet, user.ref_revenue)
        reset_referral_revenue(callback.from_user.id)
        await callback.answer(get_text('payout_success', user_lang).format(wallet=user.active_wallet), show_alert=True)
    elif user.ref_revenue < 1:
        await callback.answer(get_text('insufficient_funds', user_lang), show_alert=True)
    elif not user.wallets:
        await callback.answer(get_text('add_wallet_first', user_lang), show_alert=True)


    await go_menu(callback.message, callback.message.state)