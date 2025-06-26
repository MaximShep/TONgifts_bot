from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def create_role_keyboard() -> InlineKeyboardMarkup:
    """Кнопки выбора роли (продавец/покупатель) [[9]]"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Продавец", callback_data="role_seller")],
            [InlineKeyboardButton(text="Покупатель", callback_data="role_buyer")]
        ]
    )
def create_welcome_keyboard() -> InlineKeyboardMarkup:
    """Новая клавиатура меню"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💸Кошелек", callback_data="wallet"),
                InlineKeyboardButton(text="🫂Рефералка", callback_data="referral")
            ],
            [
                InlineKeyboardButton(text="🚀Создать сделку", callback_data="create_deal")
            ],
            [
                InlineKeyboardButton(text="🌍Language", callback_data="language"),
                InlineKeyboardButton(text="🤝Поддержка", url="https://t.me/MivelonGuarantor_SupportBot "),
            ]
        ]
    )
def create_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Кнопка подтверждения создания сделки"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Готово", callback_data="deal_created")]
        ]
    )
def create_start_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для команды /start"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать сделку")]
        ],
        resize_keyboard=True
    )
def create_payment_keyboard(deal_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Подтвердить оплату",
                callback_data=f"confirm_payment_{deal_id}"  # Убедитесь, что deal_id передается [[8]]
            )]
        ]
    )
def create_start_payment_keyboard(deal_id: str) -> InlineKeyboardMarkup:
    """Кнопка для перехода к оплате [[8]]"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Перейти к оплате",
                callback_data=f"start_payment_{deal_id}"
            )]
        ]
    )


def create_wallets_keyboard(wallets: list, active_wallet: str) -> InlineKeyboardMarkup:
    buttons = []
    for idx, wallet in enumerate(wallets, 1):
        label = f"{idx}✅" if wallet == active_wallet else f"{idx}"
        buttons.append(
            InlineKeyboardButton(text=label, callback_data=f"select_wallet_{idx}")
        )

    keyboard = []
    # Формируем строки по 2 кнопки
    for i in range(0, len(buttons), 2):
        row = buttons[i:i + 2]
        keyboard.append(row)

    # Добавляем кнопки управления
    if wallets:
        keyboard.append([InlineKeyboardButton(text="❌ Удалить кошелек", callback_data="delete_wallet")])
    keyboard.append([InlineKeyboardButton(text="➕ Добавить кошелек", callback_data="add_wallet")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def create_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Кнопка 'В меню'"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
        ]
    )