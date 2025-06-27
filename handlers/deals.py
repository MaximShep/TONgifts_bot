from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from utils.keyboards import create_role_keyboard, create_confirmation_keyboard, create_start_payment_keyboard, create_welcome_keyboard, create_wallets_keyboard, create_back_to_menu_keyboard, create_delete_wallet_keyboard, create_delete_confirmation_keyboard, create_back_to_wallets_keyboard, create_deal_wallet_selection
from utils.validators import validate_ton_address, validate_price, validate_tg_nft_link
from utils.hex_generator import generate_hex_id
from database.repository import save_deal, get_deal_by_hex, update_deal_buyer, save_or_update_user, update_deal_seller, update_ton_address, get_user_wallets, add_user_wallet, set_active_wallet, delete_user_wallet
from config import Config
from aiogram.types import FSInputFile  # Для локальных файлов [[3]]
from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode
from database.models import User  # Для работы с моделью User
from database.repository import session  # Для доступа к сессии

router = Router()


class SellerStates(StatesGroup):
    wait_ton_address = State()
    wait_gift_name = State()
    wait_price = State()
    wait_ton_address_in_wallet = State()
    select_wallet = State()

class DeleteWalletStates(StatesGroup):
    select_wallet = State()  # Выбор кошелька для удаления
    confirm = State()  # Подтверждение удаления


class BuyerStates(StatesGroup):
    wait_hex_code = State()
    wait_payment = State()  # Новое состояние для перехода к оплате
    wait_payment_confirmation = State()  # Ожидание подтверждения



# --- Обработка команды /start с deep-линком ---
@router.message(CommandStart(deep_link=True))
async def handle_deep_link(message: Message, state: FSMContext, command: CommandStart):
    """
    Обрабатывает переход по ссылке вида t.me/bot?start=HEX_ID [[5]][[8]]
    """
    hex_id = command.args  # Используем встроенный парсинг аргументов [[8]]
    await _join_deal(message, state, hex_id)

@router.message(CommandStart(deep_link=False))  # Новый фильтр [[8]]
async def cmd_start(message: Message):
    """
    Приветственное сообщение с кнопкой [[1]]
    """
    await message.answer_photo(
        photo=FSInputFile("assets/startCover.png"),  # Замените на вашу ссылку или file_id [[1]]
        caption="Добро пожаловать в Mivelon Guarantor!\n\n"
                "Этот бот обеспечивает безопасные сделки с NFT.\n"
                "Нажмите кнопку ниже, чтобы создать сделку:",
        reply_markup=create_welcome_keyboard()
    )
# --- Обработка ручного ввода HEX-кода ---
@router.message(BuyerStates.wait_hex_code)
async def process_hex_code(message: Message, state: FSMContext):
    hex_id = message.text.strip()
    await _join_deal(message, state, hex_id)


async def _join_deal(message: Message, state: FSMContext, hex_id: str):
    """
    Общая логика присоединения к сделке [[8]]
    """
    deal = get_deal_by_hex(hex_id)
    if not deal:
        await message.answer("Сделка не найдена. Проверьте HEX-код.")
        return
    
    # Проверяем, не является ли пользователь уже участником сделки
    if deal.seller_id == message.from_user.id or deal.buyer_id == message.from_user.id:
        await message.answer("Вы уже являетесь участником этой сделки.")
        return
    
    save_or_update_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )




    if not deal.seller_id:
        update_deal_seller(deal.id, seller_id=message.from_user.id)
        await state.update_data(id=deal.id)
        await state.update_data(seller_id=message.from_user.id)
        await state.update_data(gift_name=deal.gift_name)
        await state.update_data(comission_price=deal.comission_price)
        await state.update_data(buyer_id=deal.buyer_id)
        await message.answer(
            f"<b>🔗 Вы присоединились к сделке #{deal.id}</b>\n\n"
            f"🛍️ Вы продаете: {deal.gift_name}\n"
            f"💰 Стоимость NFT: {deal.price} TON\n"
            f"<i>(комиссию сервиса 5% оплачивает покупатель)</i>",
            parse_mode=ParseMode.HTML,
        )
        await message.bot.send_message(
            chat_id=deal.buyer_id,
            text=f"Продавец @{message.from_user.username} присоединился к сделке!"
        )
        await message.answer("💳 Введите ваш TON-адрес:")
        await state.set_state(SellerStates.wait_ton_address)
    else:
        update_deal_buyer(deal.id, buyer_id=message.from_user.id)

        # Уведомления
        await message.answer(
            f"<b>🔗 Вы присоединились к сделке #{deal.id}</b>\n\n"
            f"🛍️ Вы покупаете: {deal.gift_name}\n"
            f"💰 Сумма к оплате: <b>{deal.comission_price} TON</b>\n\n"
            f"<i>Комиссия сервисса составляет 5% от стоимости сделки (при сумме сделки менее 0.01 TON, комиссия составляет 0.01 TON)</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=create_start_payment_keyboard(deal.id)
        )
        await message.bot.send_message(
            chat_id=deal.seller_id,
            text=f"Покупатель @{message.from_user.username} присоединился к сделке!"
        )
        await state.clear()  # Сброс состояния после присоединения [[6]]
    # Запуск процесса оплаты

# --- Команда меню ---

@router.message(F.text.in_({"/menu", "Меню"}))
async def go_menu(message: Message, state: FSMContext):
    await message.answer_photo(
        photo=FSInputFile("assets/menu.png"),  # Замените на вашу ссылку или file_id [[1]]
        caption="И вы до сих пор в Mivelon Guarantor!\n\n"
                "Этот бот обеспечивает безопасные сделки с NFT.\n"
                "Нажмите кнопку ниже, чтобы создать сделку:",
        reply_markup=create_welcome_keyboard()
    )


@router.callback_query(F.data == "wallet")
async def show_wallets(callback: CallbackQuery):
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
        reply_markup=create_wallets_keyboard(wallets, active_wallet)
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
    await callback.message.delete()
    await callback.message.answer(
        "📥 <b>Введите адрес TON-кошелька</b>\n\n"
        "Пример: EQ... или UQ...",
        parse_mode=ParseMode.HTML,
        reply_markup=create_back_to_wallets_keyboard()
    )
    await state.set_state(SellerStates.wait_ton_address_in_wallet)

# Обработка ввода адреса
@router.message(SellerStates.wait_ton_address_in_wallet)
async def process_add_wallet(message: Message, state: FSMContext):
    if not validate_ton_address(message.text):
        await message.answer(
            "⚠️ <b>Неверный формат адреса!</b>\n"
            "Адрес должен начинаться с EQ или UQ и содержать 48 символов",
            parse_mode=ParseMode.HTML,
            reply_markup=create_back_to_wallets_keyboard()
        )
        return

    add_user_wallet(message.from_user.id, message.text)
    await message.answer(
        "✅ <b>Кошелек добавлен!</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=create_back_to_wallets_keyboard()
    )
    await state.clear()


# Заменить существующий обработчик удаления:
@router.callback_query(F.data == "delete_wallet")
async def delete_wallet(callback: CallbackQuery, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    wallets = user.wallets if user else []

    if not wallets:
        await callback.answer("У вас нет сохраненных кошельков", show_alert=True)
        return

    await callback.message.delete()
    await callback.message.answer(
        "Выберите кошелек для удаления:\n" +
        "\n".join([f"{i + 1}.{wallet}" for i, wallet in enumerate(wallets)]),
        reply_markup=create_delete_wallet_keyboard(wallets)
    )
    await state.set_state(DeleteWalletStates.select_wallet)


# Добавить обработчик выбора кошелька:
@router.callback_query(DeleteWalletStates.select_wallet, F.data.startswith("delete_select_"))
async def confirm_deletion(callback: CallbackQuery, state: FSMContext):
    wallet_idx = int(callback.data.split("_")[-1])
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()

    if not user or wallet_idx >= len(user.wallets):
        await callback.answer("Ошибка выбора кошелька", show_alert=True)
        return

    selected_wallet = user.wallets[wallet_idx]
    await state.update_data(selected_wallet=selected_wallet)

    await callback.message.delete()
    await callback.message.answer(
        f"Удалить кошелек?\n\n{selected_wallet}",
        reply_markup=create_delete_confirmation_keyboard()
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

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await callback.message.delete()  # Удаляем текущее сообщение
    await go_menu(callback.message, state)

@router.callback_query(F.data == "referral")
async def process_referral(callback: CallbackQuery):
    await callback.answer("Реферальная программа в разработке", show_alert=True)

@router.callback_query(F.data == "language")
async def process_language(callback: CallbackQuery):
    await callback.answer("Выбор языка в разработке", show_alert=True)

# --- Остальная логика создания сделки (продавец) ---

@router.message(F.text.in_({"/create_deal", "Сделка"}))
async def start_deal_creation(message: Message, state: FSMContext):
    await message.answer_photo(
        photo=FSInputFile("assets/choose.png"),
        caption="🙍‍♂️ Выберите роль:",
        reply_markup=create_role_keyboard())
    await state.set_state(SellerStates.wait_ton_address)

@router.callback_query(F.data == "create_deal")
async def process_create_deal_callback(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие кнопки "Создать сделку" и вызывает логику команды /create_deal.
    """
    await callback.answer()  # Подтверждаем получение запроса
    await callback.message.delete()  # Удаляем сообщение с кнопкой (опционально)

    # Вызываем логику создания сделки
    await start_deal_creation(callback.message, state)


@router.callback_query(F.data == "role_seller")
async def process_seller_role(callback: CallbackQuery, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    wallets = user.wallets if user else []
    active_wallet = user.active_wallet if user else None

    text = (
            "💼 <b>Выберите кошелек для сделки:</b>\n\n" +
            ("\n".join([
                f"{i + 1}. <code>{w}</code> {'✅' if w == active_wallet else ''}"
                for i, w in enumerate(wallets)
            ]) if wallets else "Нет сохраненных кошельков\n\n") +
            "Можно ввести новый адрес или выбрать существующий"
    )

    await callback.message.answer(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=create_deal_wallet_selection(wallets, active_wallet)
    )
    await state.set_state(SellerStates.wait_ton_address)


# Выбор существующего кошелька
@router.callback_query(SellerStates.wait_ton_address, F.data.startswith("deal_wallet_"))
async def select_deal_wallet(callback: CallbackQuery, state: FSMContext):
    wallet_idx = int(callback.data.split("_")[-1])
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()

    if wallet_idx < len(user.wallets):
        selected_wallet = user.wallets[wallet_idx]
        set_active_wallet(callback.from_user.id, selected_wallet)
        await callback.answer(f"Выбран кошелек: {selected_wallet}")
        await process_seller_role(callback, state)  # Обновляем интерфейс


# Кнопка "Далее"
@router.callback_query(SellerStates.wait_ton_address, F.data == "deal_wallet_next")
async def proceed_deal_wallet(callback: CallbackQuery, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()

    if not user or not user.active_wallet:
        await callback.answer("Сначала выберите кошелек", show_alert=True)
        return

    await state.update_data(ton_address=user.active_wallet)
    await callback.message.answer_photo(
        photo=FSInputFile("assets/link.png"),
        caption="🔗 Отправьте ссылку на подарок:"
    )
    await state.set_state(SellerStates.wait_gift_name)


# Обработка ввода нового адреса
@router.message(SellerStates.wait_ton_address)
async def process_new_deal_wallet(message: Message, state: FSMContext):
    if not validate_ton_address(message.text):
        await message.answer("⚠️ Неверный формат адреса. Попробуйте снова:")
        return

    add_user_wallet(message.from_user.id, message.text)
    set_active_wallet(message.from_user.id, message.text)
    await state.update_data(ton_address=message.text)
    await message.answer_photo(
        photo=FSInputFile("assets/link.png"),
        caption="🔗 Отправьте ссылку на подарок:"
    )
    await state.set_state(SellerStates.wait_gift_name)

@router.callback_query(F.data == "cancel_deal")
async def cancel_deal(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Сделка отменена", reply_markup=create_welcome_keyboard())

@router.callback_query(F.data == "role_buyer")
async def process_seller_role(callback: CallbackQuery, state: FSMContext):
    await state.update_data(ton_address="")
    await state.update_data(id="")
    await callback.message.answer_photo(
        photo=FSInputFile("assets/link.png"),
        caption="🔗 Отправьте ссылку на подарок:")
    await state.set_state(SellerStates.wait_gift_name)


@router.message(SellerStates.wait_ton_address)
async def process_ton_address(message: Message, state: FSMContext):
    if not validate_ton_address(message.text):
        await message.answer("Неверный формат TON-адреса. Попробуйте снова:")
        return

    # Добавляем кошелек и устанавливаем активным
    add_user_wallet(message.from_user.id, message.text)
    set_active_wallet(message.from_user.id, message.text)  # Новая строка

    await state.update_data(ton_address=message.text)
    data = await state.get_data()

    if data["id"] != "":
        update_ton_address(data["id"], data["ton_address"])
        await message.bot.send_message(
            chat_id=data["seller_id"],
            text=f"TON адрес принят! Ожидайте начала оплаты покупателем"
        )
        await message.bot.send_message(
            chat_id=data["buyer_id"],
            text=f"<b>🔗 Оплата по сделке #{data['id']}</b>\n"
                 f"🛍️ Вы покупаете: {data['gift_name']}\n"
                 f"💰 Сумма к оплате: <b>{data['comission_price']} TON</b>\n"
                 f"<i>Комиссия сервиса составляет 5% от стоимости сделки</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=create_start_payment_keyboard(data["id"])
        )
        await state.clear()
    else:
        await message.answer_photo(
            photo=FSInputFile("assets/link.png"),
            caption="🔗 Отправьте ссылку на подарок:"
        )
        await state.set_state(SellerStates.wait_gift_name)

@router.message(SellerStates.wait_gift_name)
async def process_gift_name(message: Message, state: FSMContext):
    if not validate_tg_nft_link(message.text):
        await message.answer("Неверный формат ссылки. Попробуйте снова:", ParseMode.MARKDOWN)
        return
    await state.update_data(gift_name=message.text)
    await message.answer_photo(
        photo=FSInputFile("assets/howMuch.png"),
        caption="💵 Введите цену подарка в TON (в формате 0.01):")
    await state.set_state(SellerStates.wait_price)


@router.message(SellerStates.wait_price)
async def process_price(message: Message, state: FSMContext):
    if not validate_price(message.text):
        await message.answer_photo(
        photo=FSInputFile("assets/howMuch.png"),
        caption="Цена должна быть числом больше 0. Для десятичного значения используйте '.'\nПопробуйте снова:")
        return

    data = await state.get_data()
    hex_id = generate_hex_id()
    await state.update_data(id=hex_id)
    await state.update_data(id=hex_id)
    if data["ton_address"]=="":
        await state.update_data(buyer_id=message.from_user.id)
        if float(message.text) <= 0.01:
            deal_id = save_deal(
                sdelka_id=hex_id,
                seller_id=None,
                buyer_id=message.from_user.id,
                ton_address=data["ton_address"],
                gift_name=data["gift_name"],
                price=float(message.text),
                comission_price = round(float(message.text) + 0.01, 6)
            )
        else:
            deal_id = save_deal(
                sdelka_id=hex_id,
                seller_id=None,
                buyer_id=message.from_user.id,
                ton_address=data["ton_address"],
                gift_name=data["gift_name"],
                price=float(message.text),
                comission_price = round(float(message.text) * (1 + float(os.getenv("COMMISSION_PERCENT"))), 6)
            )
    else:
        await state.update_data(seller_id=message.from_user.id)
        if float(message.text) <= 0.01:
            deal_id = save_deal(
                sdelka_id=hex_id,
                seller_id=message.from_user.id,
                buyer_id=None,
                ton_address=data["ton_address"],
                gift_name=data["gift_name"],
                price=float(message.text),
                comission_price = round(float(message.text) + 0.01, 6)
            )
        else:
            deal_id = save_deal(
                sdelka_id=hex_id,
                seller_id=message.from_user.id,
                buyer_id=None,
                ton_address=data["ton_address"],
                gift_name=data["gift_name"],
                price=float(message.text),
                comission_price = round(float(message.text) * (1 + float(os.getenv("COMMISSION_PERCENT"))), 6)
            )
    await state.clear()  # Сброс состояния после присоединения [[6]]
    link = f"https://t.me/{Config.BOT_USERNAME}?start={hex_id}"
    deal = get_deal_by_hex(hex_id)
    await message.answer(
        f"<b>Сделка создана! #{hex_id}</b>\n\n"
        f"🛍️ NFT для продажи: {deal.gift_name}\n\n"
        f"💰 Стоимость NFT: {deal.price} TON\n"
        f"<i>(комиссию сервиса 5% оплачивает покупатель)</i>\n\n"
        f"Поделитесь ссылкой со вторым участником сделки:\n{link}",
        parse_mode=ParseMode.HTML
    )
