# locales.py
LEXICON = {
    "RU": {
        "role_seller": "🎁 Продавец",
        "role_buyer": "💸 Покупатель",
        "back_button": "🔙 Назад",
        "wallet_button": "💸Кошелек",
        "referral_button": "🫂Рефералка",
        "create_deal": "🚀Создать сделку",
        "language_button": "🌍Language",
        "support_button": "🤝Поддержка",
        "done_button": "Готово",
        "confirm_payment": "Подтвердить оплату",
        "start_payment": "Перейти к оплате",
        "add_wallet": "➕ Добавить",
        "delete_wallet": "❌ Удалить",
        "back_to_menu": "🔙 В меню",
        "back_to_wallets": "🔙 К кошелькам",
        "delete_button": "❌ Удалить",
        "cancel_button": "🔙 Отмена",
        "cancel_deal": "❌ Отменить сделку",
        "proceed_button": "Далее ➡️",
        "leave_button": "❌ Выйти",
        "close_button": "Закрыть",
        "tonkeep": "💸Перейти в Tonkeeper",
        "russian": "🇷🇺Русский",
        "english": "🇺🇸English",
        "menu_message": "💎 И вы до сих пор в <b>Mivelon Guarantor</b>. Главное МЕНЮ\n\n"
                        "🔒 Безопасные сделки с NFT-подарками\n"
                        "💰 Уникальная система управления кошельками\n"
                        "✅ Автоматическая проверка передачи подарка (без подтверждений)\n\n"
                        "<i>Создайте сделку или присоединитесь к существующей:</i>",
        "welcome_message": '<tg-emoji emoji-id="5238168687164279948">👍</tg-emoji>💎Добро пожаловать в  <b>Mivelon Guarantor</b> - первый <u>полностью</u> автоматизированный гарант\n\n'
                           "🔒 Безопасные сделки с NFT-подарками\n"
                           "💰 Уникальная система управления кошельками\n"
                           "✅ Автоматическая проверка передачи подарка (без подтверждений)\n\n"
                           "<i>Создайте сделку или присоединитесь к существующей:</i>",
        "role_selection": "🧑‍💻Выберите РОЛЬ\n\n"
                          "🎁<b>Продавец</b> - владелец подарка в данный момент\n"
                          "💸<b>Покупатель</b> - тот, кто платит тоны\n\n"
                          "<i>Для создания сделки нужна <u>ссылка на подарок</u>, можно сразу скопировать её в буфер обмена.</i>",
        "deal_not_found": "Сделка не найдена. Проверьте HEX-код.",
        "already_participant": "Вы уже являетесь участником этой сделки.",
        "seller_joined": "Продавец @{username} присоединился к сделке!",
        "buyer_joined": "Покупатель @{username} присоединился к сделке!",
        "select_wallet_for_deal": "💼 <b>Для продолжения <u>Выберите КОШЕЛЕК</u> для сделки (на него придут ТОНы покупателя):</b>\n"
                                 "{wallet_list}\n"
                                 "{no_wallets}\n"
                                 "🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий",
        "select_wallet": "💼 <b><u>Выберите КОШЕЛЕК</u> для сделки (на него придут ТОНы покупателя):</b>\n"
                                 "{wallet_list}\n"
                                 "{no_wallets}\n"
                                 "🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий",
        "no_saved_wallets": "😭Нет сохраненных кошельков",
        "commission_info": "(комиссию сервиса {percent}% оплачивает покупатель)",
        "join_deal_seller": "<b>🔗 Вы присоединились к сделке #{deal_id}</b>\n"
                            "🛍️ Вы продаете: {gift_name}\n"
                            "💰 Стоимость NFT: {price} TON\n"
                            "<i>(комиссию сервиса {percent}% оплачивает покупатель)👇</i>",
        "join_deal_buyer": "<b>🔗 Вы присоединились к сделке #{deal_id}</b>\n"
                           "🛍️ Вы покупаете: {gift_name}\n"
                           "💰 Сумма к оплате: <b>{price} TON</b>\n"
                           "<i>Комиссия сервиса составляет {percent}% от стоимости сделки (при сумме сделки менее 0.01 TON, комиссия составляет 0.01 TON)</i>",
        "ton_address_confirmed": "TON адрес принят! Ожидайте начала оплаты покупателем",
        "payment_required": "<b>🔗 Оплата по сделке #{deal_id}</b>\n🛍️ Вы покупаете: {gift_name}\n💰 Сумма к оплате: <b>{price} TON</b>\n<i>Комиссия сервиса составляет {percent}% от стоимости сделки</i>",
        "invalid_ton_address": "❗️НЕВЕРНЫЙ формат TON-адреса. <u><i>Попробуйте снова</i></u>❗️\n"
                               "💼 <b>Выберите КОШЕЛЕК для сделки (на него придут ТОНы покупателя):</b>\n"
                               "{wallet_list}\n"
                               "{no_wallets}\n"
                               "🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий",
        "deal_created": "<b>Сделка создана! #{hex_id}</b>\n"
                        "🛍️ NFT для продажи: {gift_name}\n"
                        "💰 Стоимость NFT: {price} TON\n"
                        "<i>(комиссию сервиса {percent}% оплачивает покупатель)</i>\n"
                        "Поделитесь ссылкой со вторым участником сделки:\n{link}",
        "ton_address_accepted": "TON адрес принят! Ожидайте начала оплаты покупателем",
        "select_wallet_first": "⚠️ Сначала выберите кошелек!",
        "wallet_selected": "Выбран кошелек: {wallet}",
       "selected_ton_address": "💳Выбранный TON-адрес:\n<code>{ton_address}</code>\n\n🔗 <u>Отправьте ссылку</u> на подарок:",
       "referral_program": "😭Реферальная программа в разработке",
       "language_selection": "🌏 Выберите язык / Choose language",
        "unknown_language": "🤔Недоступный язык",
        "buyer_enter_gift_link": "🔗 Отправьте ссылку на подарок:",
        "deal_time_out":"Сделка #{deal_id} отменена автоматически из-за отсутствия активности",
        "leave_message":"@{username} покинул сделку #{deal_id}"

        # ... остальные ключи
    },
    "EN": {
"role_seller": "🎁 Seller",
        "role_buyer": "💸 Buyer",
        "back_button": "🔙 Back",
        "wallet_button": "💸Wallet",
        "referral_button": "🫂Referral",
        "create_deal": "🚀Create Deal",
        "language_button": "🌍Language",
        "support_button": "🤝Support",
        "done_button": "Done",
        "confirm_payment": "Confirm Payment",
        "start_payment": "Start Payment",
        "add_wallet": "➕ Add",
        "delete_wallet": "❌ Delete",
        "back_to_menu": "🔙 To Menu",
        "back_to_wallets": "🔙 To Wallets",
        "delete_button": "❌ Delete",
        "cancel_button": "🔙 Cancel",
        "cancel_deal": "❌ Cancel Deal",
        "proceed_button": "Proceed ➡️",
        "leave_button": "❌ Leave",
        "close_button": "Close",
        "tonkeep": "💸Go to Tonkeeper",
        "russian": "🇷🇺Russian",
        "english": "🇺🇸English",
        "selected_ton_address": "💳Selected TON address:\n<code>{ton_address}</code>\n\n🔗 <u>Send a link</u> to the gift:",
"menu_message": "💎 You're still in <b>Mivelon Guarantor</b>. Main MENU\n\n"
                "🔒 Secure NFT deals\n"
                "💰 Unique wallet management system\n"
                "✅ Automatic gift transfer verification (no confirmations required)\n\n"
                "<i>Create a deal or join an existing one:</i>",
"welcome_message": "💎Welcome to <b>Mivelon Guarantor</b> - the first fully automated guarantor\n\n"
                   "🔒 Secure NFT deals\n"
                   "💰 Unique wallet management system\n"
                   "✅ Automatic gift transfer verification (no confirmations required)\n\n"
                   "<i>Create a deal or join an existing one:</i>",
        "role_selection": "🧑‍💻Choose ROLE\n\n"
                          "🎁<b>Seller</b> - current gift owner\n"
                          "💸<b>Buyer</b> - pays TON\n\n"
                          "<i>You'll need a gift link to create a deal. You can copy it to clipboard now.</i>",
        "deal_not_found": "Deal not found. Check HEX code.",
        "already_participant": "You are already a participant of this deal.",
        "seller_joined": "Seller @{username} joined the deal!",
        "buyer_joined": "Buyer @{username} joined the deal!",
        "select_wallet_for_deal": "<b>💼 For deal continuation <u>Select WALLET</u> (TONs will come here):</b>\n"
                                 "{wallet_list}\n"
                                 "{no_wallets}\n"
                                 "🤝You can <i><b>enter new address</b></i> or select existing",
        "select_wallet": "<b>💼 <u>Select WALLET</u> (TONs will come here):</b>\n"
                                 "{wallet_list}\n"
                                 "{no_wallets}\n"
                                 "🤝You can <i><b>enter new address</b></i> or select existing",
        "no_saved_wallets": "😭No saved wallets",
        "commission_info": "(service fee {percent}% paid by buyer)",
        "join_deal_seller": "<b>🔗 You joined deal #{deal_id}</b>\n"
                            "🛍️ You're selling: {gift_name}\n"
                            "💰 NFT price: {price} TON\n"
                            "<i>(service fee {percent}% paid by buyer)👇</i>",
        "join_deal_buyer": "<b>🔗 You joined deal #{deal_id}</b>\n"
                           "🛍️ You're buying: {gift_name}\n"
                           "💰 Amount to pay: <b>{price} TON</b>\n"
                           "<i>Service fee is {percent}% of deal amount (for deals below 0.01 TON, fee is 0.01 TON)</i>",
        "ton_address_confirmed": "TON address accepted! Waiting for buyer's payment.",
        "payment_required": "<b>🔗 Payment for deal #{deal_id}</b>\n"
                            "🛍️ You're buying: {gift_name}\n"
                            "💰 Amount to pay: <b>{price} TON</b>\n"
                            "<i>Service fee is {percent}% of deal amount</i>",
        "invalid_ton_address": "❗️INVALID TON address format. <u><i>Try again</i></u>❗️\n"
                               "💼 <b>Select DEAL WALLET (TONs will come here):</b>\n"
                               "{wallet_list}\n"
                               "{no_wallets}\n"
                               "🤝You can <i><b>enter new address</b></i> or select existing",
        "deal_created": "<b>Deal created! #{hex_id}</b>\n"
                        "🛍️ NFT for sale: {gift_name}\n"
                        "💰 NFT price: {price} TON\n"
                        "<i>(service fee {percent}% paid by buyer)</i>\n"
                        "Share this link with second participant:\n{link>",
        "ton_address_accepted": "TON address accepted! Waiting for buyer's payment.",
        "select_wallet_first": "⚠️ Please select a wallet first!",
        "wallet_selected": "Selected wallet: {wallet}",
        "referral_program": "😭Referral program is not ready",
       "language_selection": "🌏 Выберите язык / Choose language",
        "unknown_language": "🤔Unknown language",
        "buyer_enter_gift_link": "🔗 Enter the link to the gift:",
        "deal_time_out": "The deal #{deal_id} was canceled automatically due to lack of activity",
        "leave_message": "@{username} leave the deal #{deal_id}"

        # ... остальные ключи
    }
}
# LEXICON = {
#     "RU": {
#         "menu_message": "💎 И вы до сих пор в <b>Mivelon Guarantor</b> - в главном МЕНЮ\n\n"+
#                    "💎 Безопасные сделки с NFT-подарками\n"+
#                    "💰 Уникальная система управления кошельками\n"+
#                    "✅ Автоматическая проверка передачи подарка (без подтверждений)\n\n"+
#                    "<i>Создайте сделку или присоединитесь к существующей:</i>",
#         "welcome_message": "💎Добро пожаловать в  <b>Mivelon Guarantor</b> - первый <u>полностью</u> автоматизированный гарант\n\n"+
#                    "💎 Безопасные сделки с NFT-подарками\n"+
#                    "💰 Уникальная система управления кошельками\n"+
#                    "✅ Автоматическая проверка передачи подарка (без подтверждений)\n\n"+
#                    "<i>Создайте сделку или присоединитесь к существующей:</i>",
#          "role_seller": "🎁 Продавец",
#         "role_buyer": "💸 Покупатель",
#         "back_button": "🔙 Назад",
#         "wallet_button": "💸Кошелек",
#         "referral_button": "🫂Рефералка",
#         "create_deal": "🚀Создать сделку",
#         "language_button": "🌍Language",
#         "support_button": "🤝Поддержка",
#         "done_button": "Готово",
#         "confirm_payment": "Подтвердить оплату",
#         "start_payment": "Перейти к оплате",
#         "add_wallet": "➕ Добавить",
#         "delete_wallet": "❌ Удалить",
#         "back_to_menu": "🔙 В меню",
#         "back_to_wallets": "🔙 К кошелькам",
#         "delete_button": "❌ Удалить",
#         "cancel_button": "🔙 Отмена",
#         "cancel_deal": "❌ Отменить сделку",
#         "proceed_button": "Далее ➡️",
#         "leave_button": "❌ Выйти из сделки",
#         "russian": "🇷🇺Русский",
#         "english": "🇺🇸English",
#         "referral_program": "😭Реферальная программа в разработке",
#         "language_selection": "🌏 Выберите язык / Choose language",
#         "unknown_language": "🤔Недоступный язык",
#         "buyer_enter_gift_link": "🔗 Отправьте ссылку на подарок:",
#         "select_wallet": "💼 <b>Выберите КОШЕЛЕК для сделки (на него придут ТОНы покупателя):</b>\n\n",
#         "none_wallet": "\n😭Нет сохраненных кошельков",
#         "end_wallet":  "\n\n🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий",
#         "change_wallet": "Выбран кошелек: ",
#         "selected_ton_address": "💳Выбранный TON-адрес:\n<code>{ton_address}</code>\n\n🔗 Отправьте ссылку на подарок:",
#         "deal_created": (
#             "<b>Сделка создана! #{hex_id}</b>\n"
#             "🛍️ NFT для продажи: {gift_name}\n"
#             "💰 Стоимость NFT: {price} TON\n"
#             "<i>(комиссию сервиса {Config.COMMISSION_PERCENT*100}% оплачивает покупатель)</i>\n"
#             "Поделитесь ссылкой со вторым участником сделки:\n{link}"
#         ),
#         "payment_required": (
#             "<b>🔗 Оплата по сделке #{deal_id}</b>\n"
#             "🛍️ Вы покупаете: {gift_name}\n"
#             "💰 Сумма к оплате: <b>{price} TON</b>\n"
#             "<i>Комиссия сервиса составляет {Config.COMMISSION_PERCENT*100}% от стоимости сделки</i>"
#         ),
#         "error_invalid_address": "❗️НЕВЕРНЫЙ формат TON-адреса. Попробуйте снова:\n💼 Введите адрес КОШЕЛЬКА или выберите из сохраненных:",
#         "role_selection": (
#             "🧑‍💻Выберите <u><b>РОЛЬ</b></u>\n"
#             "🎁<b>Продавец</b> - владелец подарка в данный момент\n"
#             "💸<b>Покупатель</b> - тот, кто платит тоны\n"
#             "<i>Для создания сделки нужна <u>ссылка на подарок</u>, можно сразу скопировать её в буфер обмена.</i>"
#         ),
#     },
#     "EN": {
#         "menu_message": "You're still in Mivelon Guarantor!\nThis bot ensures secure NFT deals.\nClick the button below to create a deal:",
#         "welcome_message": "Welcome to Mivelon Guarantor!\nThis bot ensures secure NFT deals.\nClick the button below to create a deal:",
#         "role_seller": "🎁 Seller",
#         "role_buyer": "💸 Buyer",
#         "back_button": "🔙 Back",
#         "wallet_button": "💸Wallet",
#         "referral_button": "🫂Referral",
#         "create_deal": "🚀Create Deal",
#         "language_button": "🌍Language",
#         "support_button": "🤝Support",
#         "done_button": "Done",
#         "confirm_payment": "Confirm Payment",
#         "start_payment": "Start Payment",
#         "add_wallet": "➕ Add",
#         "delete_wallet": "❌ Delete",
#         "back_to_menu": "🔙 To Menu",
#         "back_to_wallets": "🔙 To Wallets",
#         "delete_button": "❌ Delete",
#         "cancel_button": "🔙 Cancel",
#         "cancel_deal": "❌ Cancel Deal",
#         "proceed_button": "Proceed ➡️",
#         "leave_button": "❌ Leave Deal",
#         "russian": "🇷🇺Russian",
#         "english": "🇺🇸English"}
# }

def get_text(key: str, user_lang: str = 'ru') -> str:
    return LEXICON.get(user_lang.upper(), {}).get(key, key)