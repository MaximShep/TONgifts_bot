from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils.keyboards import create_role_keyboard, create_confirmation_keyboard, create_start_payment_keyboard, create_welcome_keyboard
from utils.validators import validate_ton_address, validate_price, validate_tg_nft_link
from utils.hex_generator import generate_hex_id
from database.repository import save_deal, get_deal_by_hex, update_deal_buyer, save_or_update_user, update_deal_seller, update_ton_address
from config import Config
from aiogram.types import FSInputFile  # Для локальных файлов [[3]]
from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode

router = Router()


class SellerStates(StatesGroup):
    wait_ton_address = State()
    wait_gift_name = State()
    wait_price = State()


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
    await state.update_data(id="")
    await callback.message.answer("💳 Введите ваш TON-адрес:")
    await state.set_state(SellerStates.wait_ton_address)

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
    save_or_update_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        wallet_address=message.text  # Сохраняем TON-адрес как wallet_address 
    )
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
            text=
            f"<b>🔗 Оплата по сделке #{data["id"]}</b>\n\n"
            f"🛍️ Вы покупаете: {data["gift_name"]}\n"
            f"💰 Сумма к оплате: <b>{data["comission_price"]} TON</b>\n\n"
            f"<i>Комиссия сервисса составляет 5% от стоимости сделки (при сумме сделки менее 0.01 TON, комиссия составляет 0.01 TON)</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=create_start_payment_keyboard(data["id"])
        )
        await state.clear()
    else:
        await message.answer_photo(
        photo=FSInputFile("assets/link.png"),
        caption="🔗 Отправьте ссылку на подарок:")
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
