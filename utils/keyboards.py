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
    """Клавиатура управления кошельками с улучшенным интерфейсом"""
    buttons = []

    # Строка с номерами кошельков
    wallet_row = [
        InlineKeyboardButton(
            text=f"{i + 1}✅" if wallet == active_wallet else f"{i + 1}",
            callback_data=f"select_wallet_{i + 1}"
        )
        for i, wallet in enumerate(wallets)
    ]
    buttons.append(wallet_row)

    # Кнопки управления
    control_buttons = [
        InlineKeyboardButton(text="➕ Добавить", callback_data="add_wallet"),
        InlineKeyboardButton(text="❌ Удалить", callback_data="delete_wallet")
    ]
    buttons.append(control_buttons)

    # Кнопка возврата в меню
    buttons.append([InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_delete_wallet_keyboard(wallets: list) -> InlineKeyboardMarkup:
    """Клавиатура выбора кошелька для удаления"""
    buttons = []

    # Строка с номерами кошельков
    wallet_row = [
        InlineKeyboardButton(
            text=str(idx + 1),
            callback_data=f"delete_select_{idx}"
        )
        for idx in range(len(wallets))
    ]
    buttons.append(wallet_row)

    # Кнопки управления
    control_buttons = [
        InlineKeyboardButton(text="🔙 К кошелькам", callback_data="wallet"),
        InlineKeyboardButton(text="🔝 В меню", callback_data="back_to_menu")
    ]
    buttons.append(control_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Кнопка 'В меню'"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
        ]
    )
def create_delete_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Удалить", callback_data="confirm_delete"),
            InlineKeyboardButton(text="🔙 Отмена", callback_data="cancel_delete")
        ]
    ])
def create_back_to_wallets_keyboard() -> InlineKeyboardMarkup:
    """Кнопки возврата в кошельки и меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 К кошелькам", callback_data="wallet"),
            InlineKeyboardButton(text="🔝 В меню", callback_data="back_to_menu")
        ]
    ])