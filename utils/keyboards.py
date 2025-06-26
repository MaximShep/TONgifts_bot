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
