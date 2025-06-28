from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from locales import get_text

def create_role_keyboard(user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('role_seller', user_lang), callback_data="role_seller"),
            InlineKeyboardButton(text=get_text('role_buyer', user_lang), callback_data="role_buyer")
        ],
        [InlineKeyboardButton(text=get_text('back_button', user_lang), callback_data="back_to_menu")]
    ])

def create_welcome_keyboard(user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('wallet_button', user_lang), callback_data="wallet"),
            InlineKeyboardButton(text=get_text('referral_button', user_lang), callback_data="referral")
        ],
        [
            InlineKeyboardButton(text=get_text('create_deal', user_lang), callback_data="create_deal")
        ],
        [
            InlineKeyboardButton(text=get_text('language_button', user_lang), callback_data="language"),
            InlineKeyboardButton(text=get_text('support_button', user_lang), url="https://t.me/MivelonGuarantor_SupportBot ")
        ]
    ])

def create_confirmation_keyboard(user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('done_button', user_lang), callback_data="deal_created")]
    ])

def create_start_keyboard(user_lang: str = 'en') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=get_text('create_deal', user_lang))]
    ], resize_keyboard=True)

def create_payment_keyboard(deal_id: str, user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('confirm_payment', user_lang), callback_data=f"confirm_payment_{deal_id}")]
    ])

def create_start_payment_keyboard(deal_id: str, user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('start_payment', user_lang), callback_data=f"start_payment_{deal_id}")]
    ])

def create_wallets_keyboard(wallets: list, active_wallet: str, user_lang: str = 'en') -> InlineKeyboardMarkup:
    buttons = []
    wallet_row = [
        InlineKeyboardButton(
            text=f"{i + 1}✅" if wallet == active_wallet else f"{i + 1}",
            callback_data=f"select_wallet_{i + 1}"
        )
        for i, wallet in enumerate(wallets)
    ]
    buttons.append(wallet_row)
    buttons.extend([
        [
            InlineKeyboardButton(text=get_text('add_wallet', user_lang), callback_data="add_wallet"),
            InlineKeyboardButton(text=get_text('delete_wallet', user_lang), callback_data="delete_wallet")
        ],
        [InlineKeyboardButton(text=get_text('back_to_menu', user_lang), callback_data="back_to_menu")]
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_delete_wallet_keyboard(wallets: list, user_lang: str = 'en') -> InlineKeyboardMarkup:
    buttons = []
    wallet_row = [
        InlineKeyboardButton(text=str(idx + 1), callback_data=f"delete_select_{idx}") for idx in range(len(wallets))
    ]
    buttons.append(wallet_row)
    buttons.extend([
        [
            InlineKeyboardButton(text=get_text('back_to_wallets', user_lang), callback_data="wallet"),
            InlineKeyboardButton(text=get_text('back_to_menu', user_lang), callback_data="back_to_menu")
        ]
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_back_to_menu_keyboard(user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('back_to_menu', user_lang), callback_data="back_to_menu")]
    ])

def create_delete_confirmation_keyboard(user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('delete_button', user_lang), callback_data="confirm_delete"),
            InlineKeyboardButton(text=get_text('cancel_button', user_lang), callback_data="cancel_delete")
        ]
    ])

def create_back_to_wallets_keyboard(user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('back_to_wallets', user_lang), callback_data="wallet"),
            InlineKeyboardButton(text=get_text('back_to_menu', user_lang), callback_data="back_to_menu")
        ]
    ])

def deal_address_keyboard_seller(user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('back_button', user_lang), callback_data="role_seller")],
        [InlineKeyboardButton(text=get_text('cancel_deal', user_lang), callback_data="cancel_deal")]
    ])

def deal_address_keyboard_buyer(user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('back_button', user_lang), callback_data="create_deal")],
        [InlineKeyboardButton(text=get_text('cancel_deal', user_lang), callback_data="cancel_deal")]
    ])

def deal_link_keyboard_seller(user_lang: str = 'en') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('cancel_deal', user_lang), callback_data="cancel_deal")]
    ])

def create_deal_wallet_selection(wallets: list, active_wallet: str, user_lang: str = 'en') -> InlineKeyboardMarkup:
    buttons = []
    wallet_row = [
        InlineKeyboardButton(text=f"{i + 1}✅" if w == active_wallet else f"{i + 1}", callback_data=f"choose_wallet_{i}")
        for i, w in enumerate(wallets)
    ]
    buttons.append(wallet_row)
    buttons.extend([
        [
            InlineKeyboardButton(text=get_text('back_button', user_lang), callback_data="create_deal"),
            InlineKeyboardButton(text=get_text('cancel_deal', user_lang), callback_data="cancel_deal")
        ],
        [InlineKeyboardButton(text=get_text('proceed_button', user_lang), callback_data="proceed_wallet")]
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_language_keyboard(user_lang: str = 'en') -> InlineKeyboardMarkup:
    buttons = []
    buttons.append([
        InlineKeyboardButton(text=get_text('russian', user_lang), callback_data="lang_ru"),
        InlineKeyboardButton(text=get_text('english', user_lang), callback_data="lang_en")
    ])
    buttons.append([InlineKeyboardButton(text=get_text('back_button', user_lang), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def join_deal_wallet_selection(wallets: list, active_wallet: str, user_lang: str = 'en') -> InlineKeyboardMarkup:
    buttons = []
    wallet_row = [
        InlineKeyboardButton(text=f"{i + 1}✅" if w == active_wallet else f"{i + 1}", callback_data=f"choose_when_join_wallet_{i}")
        for i, w in enumerate(wallets)
    ]
    buttons.append(wallet_row)
    buttons.extend([
        [
            InlineKeyboardButton(text=get_text('language_button', user_lang), callback_data="join_and_change_language"),
            InlineKeyboardButton(text=get_text('support_button', user_lang), url="https://t.me/MivelonGuarantor_SupportBot ")
        ],
        [InlineKeyboardButton(text=get_text('leave_button', user_lang), callback_data="leave_deal")],
        [InlineKeyboardButton(text=get_text('proceed_button', user_lang), callback_data="proceed_join_wallet")]
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)