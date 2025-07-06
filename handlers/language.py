from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode

from database.repository import (
    session, get_user_language, update_user_language
)
from database.models import User
from locales import get_text
from utils.keyboards import (
    create_language_keyboard, create_welcome_keyboard, seller_join_language_keyboard, buyer_join_language_keyboard
)
from config import Config

# Создаем отдельный роутер для кошельков
router = Router()


#РАЗДЕЛ С ЯЗЫКАМИ
@router.callback_query(F.data == "language")
async def process_language(callback: CallbackQuery):
    user_lang = get_user_language(callback.from_user.id)

    # Создаем медиа-объект с новым изображением и подписью
    media = InputMediaPhoto(
        media=FSInputFile("assets/language.png"),
        caption=get_text('language_selection', user_lang)
    )

    # Изменяем медиа и подпись одним запросом
    await callback.message.edit_media(
        media=media,
        reply_markup=create_language_keyboard(user_lang)
    )
@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1].lower()  # Приводим к нижнему регистру
    user_lang = get_user_language(callback.from_user.id)
    if lang not in ['ru', 'en', 'ar', 'zh']:
        await callback.answer(get_text('unknown_language', user_lang), show_alert=True)
        return

    update_user_language(callback.from_user.id, lang)

    # Перезагружаем пользователя из БД
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    user_lang = user.language if user else 'en'  # Язык по умолчанию
    media = InputMediaPhoto(
        media=FSInputFile("assets/menu.png"),
        parse_mode=ParseMode.HTML,
        caption=get_text('menu_message', user_lang)
    )
    # Изменяем медиа и подпись одним запросом
    await callback.message.edit_media(
        media=media,
        parse_mode=ParseMode.HTML,
        reply_markup=create_welcome_keyboard(user_lang)
    )

# # поменять язык при присоединении
# @router.callback_query(F.data == "join_and_change_language")
# async def process_referral(callback: CallbackQuery):
#     await callback.answer("Учи английский", show_alert=True)

#присоединился ПРОДАВЕЦ
@router.callback_query(F.data == "join_and_change_language")
async def process_language(callback: CallbackQuery):
    user_lang = get_user_language(callback.from_user.id)

    # Создаем медиа-объект с новым изображением и подписью
    media = InputMediaPhoto(
        media=FSInputFile("assets/join_language.png"),
        caption=get_text('language_selection', user_lang)
    )

    # Изменяем медиа и подпись одним запросом
    await callback.message.edit_media(
        media=media,
        reply_markup=seller_join_language_keyboard(user_lang)
    )

#присоединился ПОКУПАТЕЛЬ
@router.callback_query(F.data.startswith("buyer_join_and_change_language_"))
async def process_language(callback: CallbackQuery):
    deal_id = callback.data.split("_")[-1]
    user_lang = get_user_language(callback.from_user.id)

    # Создаем медиа-объект с новым изображением и подписью
    media = InputMediaPhoto(
        media=FSInputFile("assets/join_language.png"),
        caption=get_text('language_selection', user_lang)
    )

    # Изменяем медиа и подпись одним запросом
    await callback.message.edit_media(
        media=media,
        reply_markup=buyer_join_language_keyboard(deal_id, user_lang)
    )

