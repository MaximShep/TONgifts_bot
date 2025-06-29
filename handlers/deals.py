from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from utils.keyboards import create_role_keyboard, create_confirmation_keyboard, create_start_payment_keyboard, \
    create_welcome_keyboard, create_deal_wallet_selection, deal_address_keyboard_seller, deal_link_keyboard_seller, \
    create_language_keyboard, join_deal_wallet_selection, deal_address_keyboard_buyer
from utils.validators import validate_ton_address, validate_price, validate_tg_nft_link
from utils.hex_generator import generate_hex_id
from database.repository import save_deal, get_deal_by_hex, update_deal_buyer, save_or_update_user, update_deal_seller, \
    update_ton_address, add_user_wallet, set_active_wallet, get_user_language, update_user_language
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
    save_or_update_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer_photo(
        photo=FSInputFile("assets/startCover.png"),  # Замените на вашу ссылку или file_id [[1]]
        caption="Добро пожаловать в Mivelon Guarantor!\n\n"
                "Этот бот обеспечивает безопасные сделки с NFT.\n"
                "Нажмите кнопку ниже, чтобы создать сделку:",
        reply_markup=create_welcome_keyboard(user_lang)
    )


# --- Команда меню ---

# Обработчик для текстового сообщения "/menu" или "Меню"
@router.message(F.text.in_({"/menu", "Меню"}))
async def menu_text(message: Message):
    user_id = message.from_user.id  # Получаем ID из callback
    user_lang = get_user_language(user_id)
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
        reply_markup=create_welcome_keyboard(user_lang)
    )

#РАЗДЕЛ С РЕФЕРАЛАМИ
@router.callback_query(F.data == "referral")
async def process_referral(callback: CallbackQuery):
    await callback.answer("Реферальная программа в разработке", show_alert=True)


#РАЗДЕЛ С ЯЗЫКАМИ
@router.callback_query(F.data == "language")
async def process_language(callback: CallbackQuery):
    user_lang = get_user_language(callback.from_user.id)

    # Создаем медиа-объект с новым изображением и подписью
    media = InputMediaPhoto(
        media=FSInputFile("assets/language.png"),
        caption="🌏Выберите ЯЗЫК / Choose LANGUAGE"
    )

    # Изменяем медиа и подпись одним запросом
    await callback.message.edit_media(
        media=media,
        reply_markup=create_language_keyboard(user_lang)
    )
@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1].lower()  # Приводим к нижнему регистру
    if lang not in ['ru', 'en']:
        await callback.answer("Недоступный язык", show_alert=True)
        return

    update_user_language(callback.from_user.id, lang)

    # Перезагружаем пользователя из БД
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    user_lang = user.language if user else 'en'  # Язык по умолчанию
    media = InputMediaPhoto(
        media=FSInputFile("assets/menu.png"),
        caption=get_text('menu_message', user_lang)
    )
    # Изменяем медиа и подпись одним запросом
    await callback.message.edit_media(
        media=media,
        reply_markup=create_welcome_keyboard(user_lang)
    )

# СОЗДАНИЕ СДЕЛКИ

### создание сделки ПО КОМАНДЕ
@router.message(F.text.in_({"/create_deal", "Сделка"}))
async def start_deal_creation(message: Message, state: FSMContext, callback: CallbackQuery):
    telegram_id = message.from_user.id
    user_lang = get_user_language(telegram_id)  # # Ваша функция получения языка
    save_or_update_user(
        telegram_id=telegram_id,
        username=message.from_user.username
    )
    await message.answer_photo(
        photo=FSInputFile("assets/choose.png"),
        caption="🧑‍💻Выберите <u><b>РОЛЬ</b></u> \n\n 🎁<b>Продавец</b> - владелец подарка в данный момент \n 💸<b>Покупатель</b> - тот, кто платит тоны \n\n <i>Для создания сделки нужна <u>ссылка на подарок</u>, можно сразу скопировать её в буфер обмена.</i>",
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
        caption="🧑‍💻Выберите <u><b>РОЛЬ</b></u> \n\n 🎁<b>Продавец</b> - владелец подарка в данный момент \n 💸<b>Покупатель</b> - тот, кто платит тоны \n\n <i>Для создания сделки нужна <u>ссылка на подарок</u>, можно сразу скопировать её в буфер обмена.</i>",
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
        caption="🔗 Отправьте ссылку на подарок:",
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
            "💼 <b>Выберите КОШЕЛЕК для сделки (на него придут ТОНы покупателя):</b>\n\n" +
            "\n".join([
                f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                for i, w in enumerate(wallets)
            ]) +
            ("\n😭Нет сохраненных кошельков" if not wallets else "") +
            "\n\n🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий"
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
    if wallet_idx < len(user.wallets):
        selected_wallet = user.wallets[wallet_idx]
        set_active_wallet(callback.from_user.id, selected_wallet)
        await callback.answer(f"Выбран кошелек: {selected_wallet}")
        await process_seller_role(callback, state)  # Обновляем интерфейс

# --- Кнопка "Далее" ---
@router.callback_query(SellerStates.select_wallet_deal, F.data == "proceed_wallet")
async def proceed_deal_wallet(callback: CallbackQuery, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    if not user or not user.active_wallet:
        await callback.answer("⚠️ Сначала выберите кошелек!", show_alert=True)
        return

    await state.update_data(ton_address=user.active_wallet)
    data = await state.get_data()
    await callback.message.delete()  # Удаляем сообщение
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    await callback.message.answer_photo(
        photo=FSInputFile("assets/link.png"),
        caption=f"💳Выбранный TON-адрес:\n<code>{data["ton_address"]}</code>\n\n🔗 Отправьте ссылку на подарок:",
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
                "❗️НЕВЕРНЫЙ формат TON-адреса. <u><i>Попробуйте снова</i></u>❗️\n" +
                "💼 <b>Выберите КОШЕЛЕК для сделки (на него придут ТОНы покупателя):</b>\n\n" +
                "\n".join([
                    f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                    for i, w in enumerate(wallets)
                ]) +
                ("\n😭Нет сохраненных кошельков" if not wallets else "") +
                "\n\n🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий"
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
        caption=f"💳Выбранный TON-адрес:\n<code>{data["ton_address"]}</code>\n\n🔗 Отправьте ссылку на подарок:",
        parse_mode=ParseMode.HTML,
        reply_markup=deal_address_keyboard_seller(user_lang)
    )
    await state.set_state(SellerStates.wait_gift_name)





######   Обработка ввода ССЫЛКИ на подарок и начало ввода ЦЕНЫ (процесс ОДИНАКОВЫЙ для ОБЕИХ ролей)
@router.message(SellerStates.wait_gift_name)
async def process_gift_name(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id)  # Ваша функция получения языка
    if not validate_tg_nft_link(message.text):
        await message.answer_photo(
        photo=FSInputFile("assets/error.png"),  # Замените на вашу ссылку или file_id [[1]]
        caption="Неверный формат ссылки. Попробуйте снова:",
        reply_markup = deal_address_keyboard_seller(user_lang))
        return
    await state.update_data(gift_name=message.text)
    await message.answer_photo(
        photo=FSInputFile("assets/howMuch.png"),
        caption="💵 Введите цену подарка в TON (в формате 0.01):",
        reply_markup=deal_link_keyboard_seller(user_lang)
    )
    await state.set_state(SellerStates.wait_price)



### ОТМЕНА создания сделки
@router.callback_query(F.data == "cancel_deal")
async def cancel_deal(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(f"Сделка отменена")
    await go_menu(callback.message, state)


###СОЗДАНИЕ СДЕЛКИ В БАЗЕ ДАННЫХ
@router.message(SellerStates.wait_price)
async def process_price(message: Message, state: FSMContext):
    user_lang = get_user_language(message.from_user.id)  # Ваша функция получения языка
    if not validate_price(message.text):
        await message.answer_photo(
        photo=FSInputFile("assets/howMuch.png"),
        caption="ЦЕНА должна быть числом БОЛЬШЕ 0. \n<i>Для десятичного значения используйте '.'</i>\n\nПопробуйте снова:",
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
    await message.answer(
        f"<b>Сделка создана! #{hex_id}</b>\n\n"
        f"🛍️ NFT для продажи: {deal.gift_name}\n\n"
        f"💰 Стоимость NFT: {deal.price} TON\n"
        f"<i>(комиссию сервиса 5% оплачивает покупатель)</i>\n\n"
        f"Поделитесь ссылкой со вторым участником сделки:\n{link}",
        parse_mode=ParseMode.HTML
    )

# ПРИСОЕДИНЕНИЕ К СДЕЛКЕ
async def _join_deal(message: Message, state: FSMContext, hex_id: str):
    deal = get_deal_by_hex(hex_id)
    if not deal:
        await message.answer_photo(
            photo=FSInputFile("assets/error.png"),  # Замените на вашу ссылку или file_id [[1]]
            caption="Сделка не найдена. Проверьте HEX-код.")
        return
    # Проверяем, не является ли пользователь уже участником сделки
    if deal.seller_id == message.from_user.id or deal.buyer_id == message.from_user.id:
        await message.answer_photo(
            photo=FSInputFile("assets/error.png"),  # Замените на вашу ссылку или file_id [[1]]
            caption="Вы уже являетесь участником этой сделки.")
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
        await message.bot.send_photo(
            chat_id=deal.buyer_id,
            photo=FSInputFile("assets/hello.png"),
            caption=f"Продавец @{message.from_user.username} присоединился к сделке!"
        )
        ##### ЗАПРАШИВАЕМ КОШЕЛЕК
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        wallets = user.wallets if user else []
        active_wallet = user.active_wallet if user else None
        user_lang = get_user_language(message.from_user.id)  # Ваша функция получения языка
        text = (
                f"<b>🔗 Вы присоединились к сделке #{deal.id}</b>\n\n"+
                f"🛍️ Вы продаете: {deal.gift_name}\n"+
                f"💰 Стоимость NFT: {deal.price} TON\n"+
                f"<i>(комиссию сервиса 5% оплачивает покупатель)👇</i>\n\n"+
                "💼 <b>Для продолжения <u>Выберите КОШЕЛЕК</u> для сделки (на него придут ТОНы покупателя):</b>\n\n" +
                "\n".join([
                    f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                    for i, w in enumerate(wallets)
                ]) +
                ("\n😭Нет сохраненных кошельков" if not wallets else "") +
                "\n\n🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий"
        )

        await message.answer_photo(
            photo=FSInputFile("assets/hello.png"),  # Замените на вашу ссылку или file_id [[1]]
            caption=text,
            parse_mode=ParseMode.HTML,
            reply_markup=join_deal_wallet_selection(wallets, active_wallet, user_lang)
        )
        await state.set_state(SellerStates.wait_ton_address)
    else:
        update_deal_buyer(deal.id, buyer_id=message.from_user.id)
        user_lang = get_user_language(message.from_user.id)  # Ваша функция получения языка
        # Уведомления
        await message.answer_photo(
            photo=FSInputFile("assets/hello.png"),  # Замените на вашу ссылку или file_id [[1]]
            caption=
            f"<b>🔗 Вы присоединились к сделке #{deal.id}</b>\n\n"
            f"🛍️ Вы покупаете: {deal.gift_name}\n"
            f"💰 Сумма к оплате: <b>{deal.comission_price} TON</b>\n\n"
            f"<i>Комиссия сервиса составляет 5% от стоимости сделки (при сумме сделки менее 0.01 TON, комиссия составляет 0.01 TON)</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=create_start_payment_keyboard(deal.id, user_lang)
        )
        await message.bot.send_photo(
            chat_id=deal.seller_id,
            photo=FSInputFile("assets/hello.png"),
            caption=f"Покупатель @{message.from_user.username} присоединился к сделке!"
        )
        await state.clear()  # Сброс состояния после присоединения [[6]]
    # Запуск процесса оплаты

### дополнительное состояние при переключении между кошельками при присоединении продавца
async def deal_change_wallets_when_join(callback: CallbackQuery, state: FSMContext, hex_id: str):
    deal = get_deal_by_hex(hex_id)
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    wallets = user.wallets if user else []
    active_wallet = user.active_wallet if user else None
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    text = (
            f"<b>🔗 Вы присоединились к сделке #{deal.id}</b>\n\n"+
            f"🛍️ Вы продаете: {deal.gift_name}\n"+
            f"💰 Стоимость NFT: {deal.price} TON\n"+
            f"<i>(комиссию сервиса 5% оплачивает покупатель)👇</i>\n\n"+
            "💼 <b>Для продолжения <u>Выберите КОШЕЛЕК</u> для сделки (на него придут ТОНы покупателя):</b>\n\n" +
            "\n".join([
                f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                for i, w in enumerate(wallets)
            ]) +
            ("\n😭Нет сохраненных кошельков" if not wallets else "") +
            "\n\n🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий"
    )
    await callback.message.answer_photo(
        photo=FSInputFile("assets/hello.png"),  # Замените на вашу ссылку или file_id [[1]]
        caption=text,
        parse_mode=ParseMode.HTML,
        reply_markup=join_deal_wallet_selection(wallets, active_wallet, user_lang)
    )
    await state.set_state(SellerStates.wait_ton_address)
    # Запуск процесса оплаты

# @router.message(SellerStates.wait_ton_address)
# async def process_ton_address(message: Message, state: FSMContext):
#     if not validate_ton_address(message.text):
#         await message.answer_photo(
#             photo=FSInputFile("assets/error.png"),  # Замените на вашу ссылку или file_id [[1]]
#             caption="Неверный формат TON-адреса. Попробуйте снова:",
#         )
#         return
#     # Добавляем кошелек и устанавливаем активным
#     add_user_wallet(message.from_user.id, message.text)
#     set_active_wallet(message.from_user.id, message.text)  # Новая строка
#     await state.update_data(ton_address=message.text)
#     data = await state.get_data()
#     if data["id"] != "":
#         update_ton_address(data["id"], data["ton_address"])
#         await message.bot.send_message(
#             chat_id=data["seller_id"],
#             text=f"TON адрес принят! Ожидайте начала оплаты покупателем"
#         )
#         user_lang = get_user_language(message.from_user.id)  # Ваша функция получения языка
#         await message.bot.send_message(
#             chat_id=data["buyer_id"],
#             text=f"<b>🔗 Оплата по сделке #{data['id']}</b>\n"
#                  f"🛍️ Вы покупаете: {data['gift_name']}\n"
#                  f"💰 Сумма к оплате: <b>{data['comission_price']} TON</b>\n"
#                  f"<i>Комиссия сервиса составляет 5% от стоимости сделки</i>",
#             parse_mode=ParseMode.HTML,
#             reply_markup=create_start_payment_keyboard(data["id"], user_lang)
#         )
#         await state.clear()
#     else:
#         await message.answer_photo(
#             photo=FSInputFile("assets/link.png"),
#             caption="🔗 Отправьте ссылку на подарок:",
#         )
#         await state.set_state(SellerStates.wait_gift_name)


# --- Выбор активного кошелька по кнопке [1][2][3]---
@router.callback_query(SellerStates.wait_ton_address, F.data.startswith("choose_when_join_wallet_"))
async def join_select_deal_wallet(callback: CallbackQuery, state: FSMContext):
    wallet_idx = int(callback.data.split("_")[-1])
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    data = await state.get_data()
    hex_id = data["id"]
    if wallet_idx < len(user.wallets):
        selected_wallet = user.wallets[wallet_idx]
        set_active_wallet(callback.from_user.id, selected_wallet)
        await callback.answer(f"Выбран кошелек: {selected_wallet}")
        await deal_change_wallets_when_join(callback, state, hex_id)

# --- Кнопка "Далее" ---
@router.callback_query(SellerStates.wait_ton_address, F.data == "proceed_join_wallet")
async def join_proceed_deal_wallet(callback: CallbackQuery, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=callback.from_user.id).first()
    if not user or not user.active_wallet:
        await callback.answer("⚠️ Сначала выберите кошелек!", show_alert=True)
        return
    await state.update_data(ton_address=user.active_wallet)
    await callback.message.delete()  # Удаляем сообщение
    user_lang = get_user_language(callback.from_user.id)  # Ваша функция получения языка
    data = await state.get_data()
    if data["id"] != "":
        update_ton_address(data["id"], data["ton_address"])
        await callback.message.bot.send_message(
            chat_id=data["seller_id"],
            text=f"TON адрес принят! Ожидайте начала оплаты покупателем"
        )
        await callback.message.bot.send_message(
            chat_id=data["buyer_id"],
            text=f"<b>🔗 Оплата по сделке #{data['id']}</b>\n"
                 f"🛍️ Вы покупаете: {data['gift_name']}\n"
                 f"💰 Сумма к оплате: <b>{data['comission_price']} TON</b>\n"
                 f"<i>Комиссия сервиса составляет 5% от стоимости сделки</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=create_start_payment_keyboard(data["id"], user_lang)
        )
        await state.clear()

# --- Ввод нового адреса РУЧНОЙ ---
@router.message(SellerStates.wait_ton_address)
async def join_process_new_deal_wallet(message: Message, state: FSMContext):
    if not validate_ton_address(message.text):
        telegram_id = message.from_user.id
        user_lang = get_user_language(telegram_id)  # Ваша функция получения языка
        user = session.query(User).filter_by(telegram_id=message.from_user.id, ).first()
        wallets = user.wallets if user else []
        active_wallet = user.active_wallet if user else None
        text = (
                "❗️НЕВЕРНЫЙ формат TON-адреса. <u><i>Попробуйте снова</i></u>❗️\n" +
                "💼 <b>Выберите КОШЕЛЕК для сделки (на него придут ТОНы покупателя):</b>\n\n" +
                "\n".join([
                    f"{i + 1}.<code>{w}</code> {'✅' if w == active_wallet else ''}"
                    for i, w in enumerate(wallets)
                ]) +
                ("\n😭Нет сохраненных кошельков" if not wallets else "") +
                "\n\n🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий"
        )
        await message.answer_photo(
            photo=FSInputFile("assets/error.png"),  # Замените на вашу ссылку или file_id [[1]]
            caption=text,
            parse_mode=ParseMode.HTML,
            reply_markup=join_deal_wallet_selection(wallets, active_wallet, user_lang)
        )
        return
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
        user_lang = get_user_language(message.from_user.id)  # Ваша функция получения языка
        await message.bot.send_message(
            chat_id=data["buyer_id"],
            text=f"<b>🔗 Оплата по сделке #{data['id']}</b>\n"
                 f"🛍️ Вы покупаете: {data['gift_name']}\n"
                 f"💰 Сумма к оплате: <b>{data['comission_price']} TON</b>\n"
                 f"<i>Комиссия сервиса составляет 5% от стоимости сделки</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=create_start_payment_keyboard(data["id"], user_lang)
        )
        await state.clear()



#ливнуть из сделки
@router.callback_query(F.data == "leave_deal")
async def process_referral(callback: CallbackQuery):
    await callback.answer("Куда погнал", show_alert=True)

# поменять язык при присоединении
@router.callback_query(F.data == "join_and_change_language")
async def process_referral(callback: CallbackQuery):
    await callback.answer("Учи английский", show_alert=True)


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
