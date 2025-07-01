from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from utils.keyboards import create_role_keyboard, create_confirmation_keyboard, create_start_payment_keyboard, \
    create_welcome_keyboard, create_deal_wallet_selection, deal_address_keyboard_seller, deal_link_keyboard_seller, \
    create_language_keyboard, join_deal_wallet_selection, deal_address_keyboard_buyer, close_keyboard, \
    not_join_start_payment_keyboard
from utils.validators import validate_ton_address, validate_price, validate_tg_nft_link
from utils.hex_generator import generate_hex_id
from database.repository import save_deal, get_deal_by_hex, update_deal_buyer, save_or_update_user, update_deal_seller, \
    update_ton_address, add_user_wallet, set_active_wallet, get_user_language, update_user_language, check_status, \
    exit_deal, get_username, is_new_user, get_user_by_id, get_userbuyer_deals, get_userseller_deals
from config import Config
from aiogram.types import FSInputFile  # Для локальных файлов [[3]]
from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode
from database.models import User  # Для работы с моделью User
from database.repository import session  # Для доступа к сессии
from locales import get_text


router = Router()


class SellerStates(StatesGroup):
    wait_ton_address = State()
    wait_gift_name = State()
    wait_price = State()
    select_wallet_deal = State()



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

# --- Обработка ручного ввода HEX-кода ---
@router.message(BuyerStates.wait_hex_code)
async def process_hex_code(message: Message, state: FSMContext):
    hex_id = message.text.strip()
    await _join_deal(message, state, hex_id)

#### команда СТАРТ
@router.message(CommandStart(deep_link=False))  # Новый фильтр [[8]]
async def cmd_start(message: Message):
    """
    Приветственное сообщение с кнопкой [[1]]
    """
    user_lang = get_user_language(message.from_user.id)  # Ваша функция получения языка

    if is_new_user(telegram_id=message.from_user.id):
        save_or_update_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username)

        keyboard_admin_users = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh_user_{message.from_user.id}")]
        ])
        await message.bot.send_message(
            chat_id=-1002751170506,
            text=f"<b>Новый пользователь @{get_username(message.from_user.id)} [{message.from_user.id}]</b>",
            message_thread_id = 25,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard_admin_users
        )
    else:
        save_or_update_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )

    await message.answer_photo(
        photo=FSInputFile("assets/startCover.png"),  # Замените на вашу ссылку или file_id [[1]]
        caption=get_text('welcome_message', user_lang),
        parse_mode=ParseMode.HTML,
        reply_markup=create_welcome_keyboard(user_lang)
    )


# --- Команда меню ---

# Обработчик для текстового сообщения "/menu" или "Меню"
@router.message(F.text.in_({"/menu", "Меню"}))
async def menu_text(message: Message):
    user_id = message.from_user.id  # Получаем ID из callback
    user_lang = get_user_language(user_id)

    if is_new_user(telegram_id=message.from_user.id):
        save_or_update_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username)

        keyboard_admin_users = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh_user_{message.from_user.id}")]
        ])
        await message.bot.send_message(
            chat_id=-1002751170506,
            text=f"<b>Новый пользователь @{get_username(message.from_user.id)} [{message.from_user.id}]</b>",
            message_thread_id = 25,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard_admin_users
        )
    else:
        save_or_update_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )

    await message.answer_photo(
        photo=FSInputFile("assets/menu.png"),
        caption=get_text('menu_message', user_lang),
        parse_mode=ParseMode.HTML,
        reply_markup=create_welcome_keyboard(user_lang)
    )

# Обработчик для callback-кнопки "Назад в меню"
@router.callback_query(F.data == "back_to_menu")
async def go_menu(callback: CallbackQuery):
    """
    Корректный возврат в меню через callback
    """
    await callback.message.delete()  # Удаляем текущее сообщение
    user_id = callback.from_user.id  # Получаем ID из callback
    user_lang = get_user_language(user_id)
    await callback.message.answer_photo(
        photo=FSInputFile("assets/menu.png"),
        caption=get_text('menu_message', user_lang),
        parse_mode=ParseMode.HTML,
        reply_markup=create_welcome_keyboard(user_lang)
    )

# Обработчик для callback-кнопки "Закрыть"
@router.callback_query(F.data == "close")
async def close_action(callback: CallbackQuery):
    await callback.message.delete()  # Удаляем текущее сообщение

#РАЗДЕЛ С РЕФЕРАЛАМИ
@router.callback_query(F.data == "referral")
async def process_referral(callback: CallbackQuery):
    user_id = callback.from_user.id  # Получаем ID из callback
    user_lang = get_user_language(user_id)
    await callback.answer(get_text('referral_program', user_lang), show_alert=True)



# СОЗДАНИЕ СДЕЛКИ

### создание сделки ПО КОМАНДЕ
@router.message(F.text.in_({"/create_deal", "Сделка"}))
async def start_deal_creation(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    user_lang = get_user_language(telegram_id)  # # Ваша функция получения языка

    if is_new_user(telegram_id=message.from_user.id):
        save_or_update_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username)

        keyboard_admin_users = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh_user_{message.from_user.id}")]
        ])
        await message.bot.send_message(
            chat_id=-1002751170506,
            text=f"<b>Новый пользователь @{get_username(message.from_user.id)} [{message.from_user.id}]</b>",
            message_thread_id = 25,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard_admin_users
        )
    else:
        save_or_update_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )

    await message.answer_photo(
        photo=FSInputFile("assets/choose.png"),
        caption=get_text('role_selection', user_lang),
        parse_mode=ParseMode.HTML,
        reply_markup=create_role_keyboard(user_lang))
    # await state.set_state(SellerStates.wait_ton_address)

### создание сделки ПО КНОПКЕ
@router.callback_query(F.data == "create_deal")
async def process_create_deal_callback(callback: CallbackQuery):
    """
    Обрабатывает нажатие кнопки "Создать сделку" и вызывает логику команды /create_deal.
    """
    await callback.answer()  # Подтверждаем получение запроса
    await callback.message.delete()  # Удаляем сообщение с кнопкой (опционально)
    user_id = callback.from_user.id  # Получаем ID из callback
    user_lang = get_user_language(user_id)  # # Ваша функция получения языка
    await callback.message.answer_photo(
        photo=FSInputFile("assets/choose.png"),
        caption=get_text('role_selection', user_lang),
        parse_mode=ParseMode.HTML,
        reply_markup=create_role_keyboard(user_lang))

###  РОЛЬ ПОКУПАТЕЛЬ
@router.callback_query(F.data == "role_buyer")
async def process_buyer_role(callback: CallbackQuery, state: FSMContext):
    await state.update_data(ton_address="")
    await state.update_data(id="")
    telegram_id = callback.from_user.id
    user_lang = get_user_language(telegram_id)
    await callback.message.delete()  # Удаляем сообщение
    await callback.message.answer_photo(
        photo=FSInputFile("assets/link.png"),
        caption=get_text('buyer_enter_gift_link', user_lang),
        reply_markup=deal_address_keyboard_buyer(user_lang)
    )
    await state.set_state(SellerStates.wait_gift_name)

#### РОЛЬ ПРОДАВЕЦ --- выбор КОШЕЛЬКА
@router.callback_query(F.data == "role_seller")
async def process_seller_role(callback: CallbackQuery, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    await callback.message.delete()  # Удаляем сообщение
    wallets = user.wallets if user else []
    active_wallet = user.active_wallet if user else None
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка

    text = (
        get_text('select_wallet', user_lang).format(
            wallet_list="\n".join([
                f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                for i, w in enumerate(wallets)
            ]),
            no_wallets=get_text('no_saved_wallets', user_lang) if not wallets else ""
        )
    )

    await callback.message.answer_photo(
        photo=FSInputFile("assets/selectWallet.png"),  # Замените на вашу ссылку или file_id [[1]]
        caption=text,
        parse_mode=ParseMode.HTML,
        reply_markup=create_deal_wallet_selection(wallets, active_wallet, user_lang)
    )
    await state.set_state(SellerStates.select_wallet_deal)  # Установите новое состояние

# --- Выбор активного кошелька по кнопке [1][2][3]---
@router.callback_query(SellerStates.select_wallet_deal, F.data.startswith("choose_wallet_"))
async def select_deal_wallet(callback: CallbackQuery, state: FSMContext):
    wallet_idx = int(callback.data.split("_")[-1])
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    if wallet_idx < len(user.wallets):
        selected_wallet = user.wallets[wallet_idx]
        set_active_wallet(callback.from_user.id, selected_wallet)
        await callback.answer(get_text('wallet_selected', user_lang).format(wallet=selected_wallet))
        await process_seller_role(callback, state)  # Обновляем интерфейс

# --- Кнопка "Далее" ---
@router.callback_query(SellerStates.select_wallet_deal, F.data == "proceed_wallet")
async def proceed_deal_wallet(callback: CallbackQuery, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    if not user or not user.active_wallet:
        await callback.answer(get_text('select_wallet_first', user_lang), show_alert=True)
        return

    await state.update_data(ton_address=user.active_wallet)
    data = await state.get_data()
    await callback.message.delete()  # Удаляем сообщение
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    await callback.message.answer_photo(
        photo=FSInputFile("assets/link.png"),
        caption=get_text('selected_ton_address', user_lang).format(ton_address=data['ton_address']),
        parse_mode=ParseMode.HTML,
        reply_markup=deal_address_keyboard_seller(user_lang)
    )
    await state.set_state(SellerStates.wait_gift_name)

# --- Ввод нового адреса РУЧНОЙ ---
@router.message(SellerStates.select_wallet_deal)
async def process_new_deal_wallet(message: Message, state: FSMContext):
    if not validate_ton_address(message.text):
        telegram_id = message.from_user.id
        user_lang = get_user_language(telegram_id)  # Ваша функция получения языка
        user = session.query(User).filter_by(telegram_id=message.from_user.id, ).first()
        wallets = user.wallets if user else []
        active_wallet = user.active_wallet if user else None
        text = (
            get_text('invalid_ton_address', user_lang).format(
                wallet_list="\n".join([
                    f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                    for i, w in enumerate(wallets)
                ]),
                no_wallets=get_text('no_saved_wallets', user_lang) if not wallets else "",
                enter_new=get_text('enter_new_or_select', user_lang)
            )
        )
        await message.answer_photo(
            photo=FSInputFile("assets/error.png"),  # Замените на вашу ссылку или file_id [[1]]
            caption=text,
            parse_mode=ParseMode.HTML,
            reply_markup=create_deal_wallet_selection(wallets, active_wallet, user_lang)
        )
        return
    telegram_id = message.from_user.id
    user_lang = get_user_language(telegram_id)  # Ваша функция получения языка
    add_user_wallet(message.from_user.id, message.text)
    set_active_wallet(message.from_user.id, message.text)
    await state.update_data(ton_address=message.text)
    data = await state.get_data()
    await message.answer_photo(
        photo=FSInputFile("assets/link.png"),
        caption=get_text('selected_ton_address', user_lang).format(ton_address=data['ton_address']),
        parse_mode=ParseMode.HTML,
        reply_markup=deal_address_keyboard_seller(user_lang)
    )
    await state.set_state(SellerStates.wait_gift_name)





######   Обработка ввода ССЫЛКИ на подарок и начало ввода ЦЕНЫ (процесс ОДИНАКОВЫЙ для ОБЕИХ ролей)
@router.message(SellerStates.wait_gift_name)
async def process_gift_name(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id)

    if not validate_tg_nft_link(message.text):
        await message.answer_photo(
            photo=FSInputFile("assets/error.png"),
            caption=get_text('invalid_gift_link', user_lang),
            parse_mode=ParseMode.HTML,
            reply_markup=deal_address_keyboard_seller(user_lang)
        )
        return

    await state.update_data(gift_name=message.text)

    await message.answer_photo(
        photo=FSInputFile("assets/howMuch.png"),
        caption=get_text('enter_price', user_lang),
        parse_mode=ParseMode.HTML,
        reply_markup=deal_link_keyboard_seller(user_lang)
    )
    await state.set_state(SellerStates.wait_price)


### ОТМЕНА создания сделки
@router.callback_query(F.data == "cancel_deal")
async def cancel_deal(callback: CallbackQuery, state: FSMContext):
    user_lang = get_user_language(callback.from_user.id)
    await state.clear()
    await callback.answer(get_text('deal_canceled', user_lang))
    await go_menu(callback)





###СОЗДАНИЕ СДЕЛКИ В БАЗЕ ДАННЫХ
@router.message(SellerStates.wait_price)
async def process_price(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id)  # Ваша функция получения языка
    if not validate_price(message.text):
        await message.answer_photo(
        photo=FSInputFile("assets/howMuch.png"),
        caption=get_text('price_must_be_number', user_lang),
        reply_markup=deal_link_keyboard_seller(user_lang))
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
    text = get_text("deal_created", user_lang).format(
        hex_id=hex_id,
        gift_name=deal.gift_name,
        price=deal.price,
        percent=Config.COMMISSION_PERCENT*100,
        link=link,
    )
    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML
    )
    keyboard_admin_deals = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh_deal_{deal.id}")]
    ])
    await message.bot.send_message(
        chat_id=-1002751170506,
        text=f"<b>Сделка #{deal.id}</b>\n\n"
            f"Статус: {deal.status}\n\n"
            f"🛍️ NFT: {deal.gift_name}\n"
            f"💰 Цена (без комиссии): {deal.price} TON\n\n"
            f"Продавец: @{get_username(deal.seller_id) if deal.seller_id is not None else '—'} [{deal.seller_id if deal.seller_id is not None else '—'}]\n"
            f"Покупатель: @{get_username(deal.buyer_id) if deal.buyer_id is not None else '—'} [{deal.buyer_id if deal.buyer_id is not None else '—'}]\n\n"
            f"<b>💰 Сумма сделки (c комиссией): {deal.comission_price} TON</b>",
        message_thread_id=35,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard_admin_deals
    )
    @router.callback_query(F.data.startswith("refresh_deal_"))
    async def refresh_deal_handler(callback: CallbackQuery):
        deal_id = callback.data.split("_")[-1]

        # Получаем актуальные данные сделки из БД или другого источника
        deal = get_deal_by_hex(deal_id)  # <-- тут должна быть ваша функция получения сделки

        if not deal:
            await callback.answer("Сделка не найдена")
            return

        updated_text = (
            f"<b>Сделка #{deal.id}</b>\n\n"
            f"Статус: {deal.status}\n\n"
            f"🛍️ NFT: {deal.gift_name}\n"
            f"💰 Цена (без комиссии): {deal.price} TON\n\n"
            f"Продавец: @{get_username(deal.seller_id) if deal.seller_id is not None else '—'} [{deal.seller_id if deal.seller_id is not None else '—'}]\n"
            f"Покупатель: @{get_username(deal.buyer_id) if deal.buyer_id is not None else '—'} [{deal.buyer_id if deal.buyer_id is not None else '—'}]\n\n"
            f"<b>💰 Сумма сделки (c комиссией): {deal.comission_price} TON</b>"
        )

        # Редактируем сообщение
        await callback.message.edit_text(
            text=updated_text,
            parse_mode=ParseMode.HTML,
            reply_markup=callback.message.reply_markup  # Оставляем кнопку
        )

        await callback.answer()

# ПРИСОЕДИНЕНИЕ К СДЕЛКЕ
async def _join_deal(message: Message, state: FSMContext, hex_id: str):
    deal = get_deal_by_hex(hex_id)
    if not deal:
        user_lang = get_user_language(message.from_user.id)
        await message.answer_photo(
            photo=FSInputFile("assets/error.png"),
            caption=get_text('deal_not_found', user_lang)
        )
        return

    # Проверяем, не является ли пользователь уже участником
    if deal.seller_id == message.from_user.id or deal.buyer_id == message.from_user.id:
        user_lang = get_user_language(message.from_user.id)
        await message.answer_photo(
            photo=FSInputFile("assets/error.png"),
            caption=get_text('already_participant', user_lang)
        )
        return


    if is_new_user(telegram_id=message.from_user.id):
        save_or_update_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username)
        keyboard_admin_users = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh_user_{message.from_user.id}")]
        ])
        await message.bot.send_message(
            chat_id=-1002751170506,
            text=f"<b>Новый пользователь @{get_username(message.from_user.id)} [{message.from_user.id}]</b>",
            message_thread_id = 25,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard_admin_users
        )
    else:
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

        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        wallets = user.wallets if user else []
        active_wallet = user.active_wallet if user else None
        user_lang = get_user_language(message.from_user.id)

        # Отправляем уведомление покупателю
        await message.bot.send_photo(
            chat_id=deal.buyer_id,
            photo=FSInputFile("assets/hello.png"),
            caption=get_text('seller_joined', user_lang).format(username=message.from_user.username)
        )

        # Генерируем список кошельков
        wallet_list = "\n".join([
            f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
            for i, w in enumerate(wallets)
        ])
        no_wallets = get_text('no_saved_wallets', user_lang) if not wallets else ""
        # Формируем текст
        text =  get_text('join_deal_seller', user_lang).format(
            deal_id=deal.id,
            gift_name=deal.gift_name,
            price=deal.comission_price,
            percent=Config.COMMISSION_PERCENT * 100
        )+ get_text('select_wallet_for_deal', user_lang).format(
            wallet_list=wallet_list,
            no_wallets=no_wallets
        )

        # Отправляем сообщение продавцу
        await message.answer_photo(
            photo=FSInputFile("assets/hello.png"),
            caption=text,
            parse_mode=ParseMode.HTML,
            reply_markup=join_deal_wallet_selection(wallets, active_wallet, deal.id, message.from_user.id, user_lang)
        )
        await state.set_state(SellerStates.wait_ton_address)
    else:
        update_deal_buyer(deal.id, buyer_id=message.from_user.id)
        user_lang = get_user_language(message.from_user.id)

        # Генерируем текст для покупателя
        text = get_text('join_deal_buyer', user_lang).format(
            deal_id=deal.id,
            gift_name=deal.gift_name,
            price=deal.comission_price,
            percent=Config.COMMISSION_PERCENT * 100
        )

        # Отправляем сообщение покупателю
        await message.answer_photo(
            photo=FSInputFile("assets/hello.png"),
            caption=text,
            parse_mode=ParseMode.HTML,
            reply_markup=create_start_payment_keyboard(deal.id, message.from_user.id, user_lang)
        )

        # Отправляем уведомление продавцу
        await message.bot.send_photo(
            chat_id=deal.seller_id,
            photo=FSInputFile("assets/hello.png"),
            caption=get_text('buyer_joined', user_lang).format(username=message.from_user.username)
        )

        await state.clear()


@router.callback_query(F.data.startswith("buyer_join_lang_"))
async def buyer_join_set_language(callback: CallbackQuery):
    parts = callback.data.split("_")
    deal_id = parts[-1]
    lang = parts[-2].lower()
    user_lang = get_user_language(callback.from_user.id)
    if lang not in ['ru', 'en']:
        await callback.answer(get_text('unknown_language', user_lang), show_alert=True)
        return
    deal = get_deal_by_hex(deal_id)
    update_user_language(callback.from_user.id, lang)

    # Перезагружаем пользователя из БД
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    user_lang = user.language if user else 'en'  # Язык по умолчанию
    text = get_text('join_deal_buyer', user_lang).format(
        deal_id=deal.id,
        gift_name=deal.gift_name,
        price=deal.comission_price,
        percent=Config.COMMISSION_PERCENT * 100
    )
    media = InputMediaPhoto(
        media=FSInputFile("assets/hello.png"),
        parse_mode=ParseMode.HTML,
        caption=text
    )
    # Изменяем медиа и подпись одним запросом
    await callback.message.edit_media(
        media=media,
        parse_mode=ParseMode.HTML,
        reply_markup=create_start_payment_keyboard(deal.id, callback.from_user.id, user_lang)
    )


@router.callback_query(F.data.startswith("seller_join_lang_"))
async def seller_join_set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[-1].lower()  # Приводим к нижнему регистру
    user_lang = get_user_language(callback.from_user.id)
    if lang not in ['ru', 'en']:
        await callback.answer(get_text('unknown_language', user_lang), show_alert=True)
        return
    data = await state.get_data()
    deal = get_deal_by_hex(data["id"])
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    wallets = user.wallets if user else []
    active_wallet = user.active_wallet if user else None
    update_user_language(callback.from_user.id, lang)

    # Перезагружаем пользователя из БД
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    user_lang = user.language if user else 'en'  # Язык по умолчанию
    text = (
            get_text('join_deal_seller', user_lang).format(
                deal_id=deal.id,
                gift_name=deal.gift_name,
                price=deal.price,
                percent=Config.COMMISSION_PERCENT * 100
            ) +
            get_text('select_wallet_for_deal', user_lang).format(
                wallet_list="\n".join([
                    f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                    for i, w in enumerate(wallets)
                ]),
                no_wallets=get_text('no_saved_wallets', user_lang) if not wallets else "",
            )
    )
    media = InputMediaPhoto(
        media=FSInputFile("assets/hello.png"),
        parse_mode=ParseMode.HTML,
        caption=text
    )
    # Изменяем медиа и подпись одним запросом
    await callback.message.edit_media(
        media=media,
        parse_mode=ParseMode.HTML,
        reply_markup=join_deal_wallet_selection(wallets, active_wallet, deal.id, callback.from_user.id, user_lang)
    )
    await state.set_state(SellerStates.wait_ton_address)
### дополнительное состояние при переключении между кошельками при присоединении продавца
async def deal_change_wallets_when_join(callback: CallbackQuery, state: FSMContext, hex_id: str):
    deal = get_deal_by_hex(hex_id)
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    wallets = user.wallets if user else []
    active_wallet = user.active_wallet if user else None
    user_lang = get_user_language(callback.from_user.id)

    text = (
            get_text('join_deal_seller', user_lang).format(
                deal_id=deal.id,
                gift_name=deal.gift_name,
                price=deal.price,
                percent=Config.COMMISSION_PERCENT * 100
            ) +
            get_text('select_wallet_for_deal', user_lang).format(
                wallet_list="\n".join([
                    f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                    for i, w in enumerate(wallets)
                ]),
                no_wallets=get_text('no_saved_wallets', user_lang) if not wallets else "",
            )
    )

    await callback.message.answer_photo(
        photo=FSInputFile("assets/hello.png"),
        caption=text,
        parse_mode=ParseMode.HTML,
        reply_markup=join_deal_wallet_selection(wallets, active_wallet, deal.id, callback.from_user.id, user_lang)
    )
    await state.set_state(SellerStates.wait_ton_address)

@router.callback_query(F.data == "return_to_join_deal")
async def return_to_join(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.delete()
    await deal_change_wallets_when_join(callback, state, data["id"])

# --- Выбор активного кошелька по кнопке [1][2][3]---
@router.callback_query(SellerStates.wait_ton_address, F.data.startswith("choose_when_join_wallet_"))
async def join_select_deal_wallet(callback: CallbackQuery, state: FSMContext):
    wallet_idx = int(callback.data.split("_")[-1])
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    data = await state.get_data()
    hex_id = data["id"]
    user_lang = get_user_language(callback.from_user.id)
    if wallet_idx < len(user.wallets):
        selected_wallet = user.wallets[wallet_idx]
        set_active_wallet(callback.from_user.id, selected_wallet)
        await callback.answer(get_text('wallet_selected', user_lang).format(wallet=selected_wallet))
        await deal_change_wallets_when_join(callback, state, hex_id)

# --- Кнопка "Далее" ---
@router.callback_query(SellerStates.wait_ton_address, F.data == "proceed_join_wallet")
async def join_proceed_deal_wallet(callback: CallbackQuery, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    user_lang = get_user_language(callback.from_user.id)
    if not user or not user.active_wallet:
        await callback.answer(get_text('select_wallet_first', user_lang), show_alert=True)
        return

    await state.update_data(ton_address=user.active_wallet)
    await callback.message.delete()
    user_lang = get_user_language(callback.from_user.id)
    data = await state.get_data()
    ton_address = user.active_wallet

    if data["id"] != "":
        update_ton_address(data["id"], ton_address)

        await callback.message.bot.send_message(
            chat_id=data["seller_id"],
            text=get_text('ton_address_accepted', user_lang)
        )

        await callback.message.bot.send_message(
            chat_id=data["buyer_id"],
            text=get_text('payment_required', user_lang).format(
                deal_id=data['id'],
                gift_name=data['gift_name'],
                price=data['comission_price'],
                percent=Config.COMMISSION_PERCENT * 100
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=not_join_start_payment_keyboard(data["id"], user_lang)
        )
        await state.clear()


# --- Ввод нового адреса РУЧНОЙ ---
@router.message(SellerStates.wait_ton_address)
async def join_process_new_deal_wallet(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id)
    data = await state.get_data()
    if not validate_ton_address(message.text):
        telegram_id = message.from_user.id
        user_lang = get_user_language(telegram_id)
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        wallets = user.wallets if user else []
        active_wallet = user.active_wallet if user else None

        text = (
            get_text('invalid_ton_address', user_lang).format(
                wallet_list="\n".join([
                    f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                    for i, w in enumerate(wallets)
                ]),
                no_wallets=get_text('no_saved_wallets', user_lang) if not wallets else "",
            )
        )
        await message.answer_photo(
            photo=FSInputFile("assets/error.png"),
            caption=text,
            parse_mode=ParseMode.HTML,
            reply_markup=join_deal_wallet_selection(wallets, active_wallet, data["id"], message.from_user.id, user_lang)
        )
        return

    add_user_wallet(message.from_user.id, message.text)
    set_active_wallet(message.from_user.id, message.text)

    await state.update_data(ton_address=message.text)
    ton_address = message.text

    if data["id"] != "":
        update_ton_address(data["id"], ton_address)

        await message.bot.send_message(
            chat_id=data["seller_id"],
            text=get_text('ton_address_accepted', user_lang)
        )

        user_lang = get_user_language(message.from_user.id)

        await message.bot.send_message(
            chat_id=data["buyer_id"],
            text=get_text('payment_required', user_lang).format(
                deal_id=data['id'],
                gift_name=data['gift_name'],
                price=data['comission_price'],
                percent=Config.COMMISSION_PERCENT * 100
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=not_join_start_payment_keyboard(data["id"], user_lang)
        )
        await state.clear()

#ливнуть из сделки
@router.callback_query(F.data.startswith("leave_deal_"))
async def leave(callback: CallbackQuery):
    parts = callback.data.split("_")
    deal_id = parts[-2]
    user_id = int(parts[-1])
    user_lang = get_user_language(user_id)
    if check_status(deal_id):
        chat_id = exit_deal(deal_id, user_id)
        await callback.message.delete()
        await callback.answer(get_text("you_leave", user_lang), show_alert=True)
        await callback.bot.send_message(
            chat_id=chat_id,
            text=get_text('leave_message', user_lang).format(
                deal_id=deal_id,
                username=get_username(user_id),
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=close_keyboard(user_lang)
        )
    else:
        await callback.answer(get_text("not_leave", user_lang), show_alert=True)

#Для чата админов
@router.callback_query(F.data.startswith("refresh_user_"))
async def refresh_deal_handler(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[-1])
    user =  get_user_by_id(user_id)
    updated_text = (
        f"<b>Пользователь @{user.username} [{user.telegram_id}]</b>\n\n"
        f"Сделок в роли продавца: {len(get_userbuyer_deals(user_id))}\n"
        f"Сделок в роли покупателя: {len(get_userseller_deals(user_id))}\n\n"
        f"<b>Всего сделок {len(get_userbuyer_deals(user_id)) + len(get_userseller_deals(user_id))}</b>\n"
        f"Активный кошелек: {user.active_wallet if user.active_wallet else '-'}\n\n"
        f"<i>Дата регистрации: {user.created_at}</i>\n"
        f"<i>Последняя активность: {user.last_activity}</i>"
    )

    # Редактируем сообщение
    await callback.message.edit_text(
        text=updated_text,
        parse_mode=ParseMode.HTML,
        reply_markup=callback.message.reply_markup  # Оставляем кнопку
    )

    await callback.answer()


# #РАЗДЕЛ С ЯЗЫКАМИ
# @router.callback_query(F.data == "language")
# async def process_language(callback: CallbackQuery):
#     user_lang = get_user_language(callback.from_user.id)
#
#     # Создаем медиа-объект с новым изображением и подписью
#     media = InputMediaPhoto(
#         media=FSInputFile("assets/language.png"),
#         caption=get_text('language_selection', user_lang)
#     )
#
#     # Изменяем медиа и подпись одним запросом
#     await callback.message.edit_media(
#         media=media,
#         reply_markup=create_language_keyboard(user_lang)
#     )
# @router.callback_query(F.data.startswith("lang_"))
# async def set_language(callback: CallbackQuery):
#     lang = callback.data.split("_")[1].lower()  # Приводим к нижнему регистру
#     user_lang = get_user_language(callback.from_user.id)
#     if lang not in ['ru', 'en']:
#         await callback.answer(get_text('unknown_language', user_lang), show_alert=True)
#         return
#
#     update_user_language(callback.from_user.id, lang)
#
#     # Перезагружаем пользователя из БД
#     user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
#     user_lang = user.language if user else 'en'  # Язык по умолчанию
#     media = InputMediaPhoto(
#         media=FSInputFile("assets/menu.png"),
#         caption=get_text('menu_message', user_lang)
#     )
#     # Изменяем медиа и подпись одним запросом
#     await callback.message.edit_media(
#         media=media,
#         reply_markup=create_welcome_keyboard(user_lang)
#     )


######### КОПИРУЕМ
# async def process_seller_role(callback: CallbackQuery, state: FSMContext):
#     user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
#     await callback.message.delete()  # Удаляем сообщение
#     wallets = user.wallets if user else []
#     active_wallet = user.active_wallet if user else None
#     user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
#
#     text = (
#             "💼 <b>Выберите КОШЕЛЕК для сделки (на него придут ТОНы покупателя):</b>\n\n" +
#             "\n".join([
#                 f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
#                 for i, w in enumerate(wallets)
#             ]) +
#             ("\n😭Нет сохраненных кошельков" if not wallets else "") +
#             "\n\n🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий"
#     )
#
#     await callback.message.answer_photo(
#         photo=FSInputFile("assets/selectWallet.png"),  # Замените на вашу ссылку или file_id [[1]]
#         caption=text,
#         parse_mode=ParseMode.HTML,
#         reply_markup=create_deal_wallet_selection(wallets, active_wallet, user_lang)
#     )
#     await state.set_state(SellerStates.select_wallet_deal)  # Установите новое состояние
#
#
#
#
#
