from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from database.repository import session, get_referral_count, get_referral_revenue, \
    reset_referral_revenue  # Для доступа к сессии
from database.models import User  # Для работы с моделью User
from config import Config
from aiogram.enums import ParseMode

from database.repository import get_user_language
from handlers.deals import go_menu
from ton_service import TonService
from utils.keyboards import back_to_menu_from_ref_keyboard
from utils.reflinks import encode_telegram_id

router = Router()
ton_service = TonService()


#РАЗДЕЛ С РЕФЕРАЛАМИ
@router.callback_query(F.data == "referral")
async def process_referral(callback: CallbackQuery):
    await callback.message.delete()  # Удаляем сообщение
    user_id = callback.from_user.id  # Получаем ID из callback
    user_lang = get_user_language(user_id)
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    link=f"https://t.me/{Config.BOT_USERNAME}?start=ref_{encode_telegram_id(user_id)}"
    wallets = user.wallets if user else []
    count_of_referrals = get_referral_count(user_id)
    revenue = get_referral_revenue(user_id)
    text=f"РЕФЕРАЛЬНАЯ программа, ваша ссылка:\n\n<code>{link}</code>\n\nКоличество приведенных пользователей: <u><b>{count_of_referrals}</b></u>\nЗаработано: <u><b>{revenue}</b></u>\n<blockquote>20% с комиссии бота</u></blockquote>\n\nАктивный кошелек:<i>{"Добавьте кошелек" if not wallets else user.active_wallet}</i>\n<blockquote>Вывести средства на активный адрес можно только от <u>1 TON</u></blockquote>"
    await callback.message.answer_photo(
        photo=FSInputFile("assets/menu.png"),
        caption=text,
        parse_mode=ParseMode.HTML,
        reply_markup=back_to_menu_from_ref_keyboard(user_lang)
    )


#Вывод средств
@router.callback_query(F.data == "money_ref")
async def give_me_my_refs(callback: CallbackQuery):
    user_lang = get_user_language(callback.from_user.id)
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    wallets = user.wallets if user else []
    if user.ref_revenue >=1 and wallets !=[]:
        # await TonService.refund_payment(user.active_wallet, user.ref_revenue)
        reset_referral_revenue(callback.from_user.id)
        await callback.answer(f"Средства выведены на {user.active_wallet}", show_alert=True)
    elif user.ref_revenue <1:
        await callback.answer(f"Недостаточно TON для вывода", show_alert=True)
    elif wallets ==[]:
        await callback.answer(f"Добавьте кошелек", show_alert=True)
    await go_menu(callback)