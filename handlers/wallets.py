from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode

from database.repository import (
    get_user_wallets,
    add_user_wallet,
    set_active_wallet,
    delete_user_wallet,
    session, get_user_language
)
from database.models import User
from utils.validators import validate_ton_address
from utils.keyboards import (
    create_wallets_keyboard,
    create_back_to_wallets_keyboard,
    create_delete_wallet_keyboard,
    create_delete_confirmation_keyboard
)
from config import Config

# Создаем отдельный роутер для кошельков
router = Router()

# Состояния для работы с кошельками
class DeleteWalletStates(StatesGroup):
    select_wallet = State()
    confirm = State()

class SellerStates(StatesGroup):
    wait_ton_address_in_wallet = State()
    select_wallet = State()  # Если используется только здесь

# ВСЕ ВАШИ ФУНКЦИИ С КОШЕЛЬКАМИ ВСТАВЬТЕ СЮДА
# Например:
@router.callback_query(F.data == "wallet")
async def show_wallets(callback: CallbackQuery):
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    if not user:
        user = User(telegram_id=callback.from_user.id, username=callback.from_user.username, wallets=[])
        session.add(user)
        session.commit()
    wallets = user.wallets
    active_wallet = user.active_wallet

    # Формируем текст с HTML-форматированием
    wallets_text = "<b>💼 Ваши КОШЕЛЬКИ:</b>\n\n" + (
        "\n".join([
            f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
            for i, w in enumerate(wallets)
        ]) if wallets else "😭Нет сохраненных кошельков"
    )

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=FSInputFile("assets/wallets.png"),
        caption=wallets_text,
        parse_mode=ParseMode.HTML,
        reply_markup=create_wallets_keyboard(wallets, active_wallet, user_lang)
    )


@router.callback_query(F.data.startswith("select_wallet_"))
async def select_wallet(callback: CallbackQuery):
    wallet_idx = int(callback.data.split("_")[-1]) - 1
    wallets = get_user_wallets(callback.from_user.id)

    if 0 <= wallet_idx < len(wallets):
        selected_wallet = wallets[wallet_idx]
        set_active_wallet(callback.from_user.id, selected_wallet)

        # Обновляем сообщение после выбора
        await show_wallets(callback)  # Перерисовываем интерфейс
        await callback.answer(f"Активный кошелек: {selected_wallet}")

# При нажатии "Добавить кошелек"
@router.callback_query(F.data == "add_wallet")
async def add_wallet(callback: CallbackQuery, state: FSMContext):
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    await callback.message.delete()
    await callback.message.answer(
        "📥 <b>Введите адрес TON-кошелька</b>\n\n"
        "Пример: EQ... или UQ...",
        parse_mode=ParseMode.HTML,
        reply_markup=create_back_to_wallets_keyboard(user_lang)
    )
    await state.set_state(SellerStates.wait_ton_address_in_wallet)

# Обработка ввода адреса
@router.message(SellerStates.wait_ton_address_in_wallet)
async def process_add_wallet(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id)  # Ваша функция получения языка
    if not validate_ton_address(message.text):
        await message.answer_photo(
        photo=FSInputFile("assets/error.png"),
        caption=
            "⚠️ <b>Неверный формат адреса!</b>\n"
            "Адрес должен начинаться с EQ или UQ и содержать 48 символов",
            parse_mode=ParseMode.HTML,
            reply_markup=create_back_to_wallets_keyboard(user_lang)
        )
        return
    add_user_wallet(message.from_user.id, message.text)
    await message.answer(
        "✅ <b>Кошелек добавлен!</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=create_back_to_wallets_keyboard(user_lang)
    )
    await state.clear()


# Заменить существующий обработчик удаления:
@router.callback_query(F.data == "delete_wallet")
async def delete_wallet(callback: CallbackQuery, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    wallets = user.wallets if user else []

    if not wallets:
        await callback.answer_photo(
        photo=FSInputFile("assets/error.png"),
        caption="У вас нет сохраненных кошельков", show_alert=True)
        return
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    await callback.message.delete()
    await callback.message.answer(
        "Выберите кошелек для удаления:\n" +
        "\n".join([f"{i + 1}.{wallet}" for i, wallet in enumerate(wallets)]),
        reply_markup=create_delete_wallet_keyboard(wallets, user_lang)
    )
    await state.set_state(DeleteWalletStates.select_wallet)


# Добавить обработчик выбора кошелька:
@router.callback_query(DeleteWalletStates.select_wallet, F.data.startswith("delete_select_"))
async def confirm_deletion(callback: CallbackQuery, state: FSMContext):
    wallet_idx = int(callback.data.split("_")[-1])
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()

    if not user or wallet_idx >= len(user.wallets):
        await callback.answer_photo(
        photo=FSInputFile("assets/error.png"),
        caption="Ошибка выбора кошелька", show_alert=True)
        return

    selected_wallet = user.wallets[wallet_idx]
    await state.update_data(selected_wallet=selected_wallet)
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    await callback.message.delete()
    await callback.message.answer(
        f"Удалить кошелек?\n\n{selected_wallet}",
        reply_markup=create_delete_confirmation_keyboard(user_lang)
    )
    await state.set_state(DeleteWalletStates.confirm)


# Подтверждение удаления
@router.callback_query(DeleteWalletStates.confirm)
async def process_deletion(callback: CallbackQuery, state: FSMContext):
    if callback.data == "cancel_delete":
        await show_wallets(callback)
        await state.clear()
        return

    data = await state.get_data()
    wallet = data.get("selected_wallet")
    delete_user_wallet(callback.from_user.id, wallet)

    await callback.answer("✅ Кошелек удален", show_alert=True)
    await show_wallets(callback)
    await state.clear()