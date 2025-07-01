# locales.py
from config import Config

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
        "transfer_nft_button": "📦 Передать NFT",
        "russian": "🇷🇺Русский",
        "english": "🇺🇸English",
        "menu_message":     '🤙 И вы до сих пор в <b>Mivelon Guarantor</b>, наш бот - это:\n\n'
                           "<i>🔘 Безопасные сделки с NFT-подарками\n"
                           "🔘️ Уникальная система управления кошельками\n"
                           "🔘 Автоматическая проверка передачи подарка</i>\n\n"
                           "Создайте сделку или присоединитесь к существующей\n\n"
                           "<blockquote><i>ВЕСЬ июль комиссия 1%</i></blockquote>",
        "welcome_message": '🤙 Приветствуем в <b>Mivelon Guarantor</b>, наш бот - это:\n\n'
                           "<i>🔘 Безопасные сделки с NFT-подарками\n"
                           "🔘️ Уникальная система управления кошельками\n"
                           "🔘 Автоматическая проверка передачи подарка</i>\n\n"
                           "Создайте сделку или присоединитесь к существующей\n\n"
                           "<blockquote><i>ВЕСЬ июль комиссия 1%</i></blockquote>",
        "role_selection": "𝟏 Выберите РОЛЬ\n\n"
                          "🔘<b>Продавец</b> - владелец подарка в данный момент\n"
                          "🔘<b>Покупатель</b> - тот, кто платит тоны\n\n"
                          "<blockquote><i>Для создания сделки нужна <u>ссылка на подарок</u>.</i></blockquote>",
        "deal_not_found": "Сделка не найдена. Проверьте HEX-код.",
        "already_participant": "Вы уже являетесь участником этой сделки.",
        "seller_joined": "Продавец @{username} [{user_id}] присоединился к сделке!\n\n"
                        "🔘Сделок в роли продавца: {userbuyer_deals}\n"
                        "🔘Сделок в роли покупателя: {userseller_deals}\n"
                        "🔘<b>Всего сделок {deals}</b>\n\n"
                         "<blockquote>Проверьте, с этим ли пользователем вы вели диалог ранее</blockquote>",
        "buyer_joined": "Покупатель @{username} [{user_id}] присоединился к сделке!\n\n"
                        "🔘Сделок в роли продавца: {userbuyer_deals}\n"
                        "🔘Сделок в роли покупателя: {userseller_deals}\n"
                        "🔘<b>Всего сделок {deals}</b>\n\n"
                         "<blockquote>Проверьте, с этим ли пользователем вы вели диалог ранее</blockquote>",
        "select_wallet_for_deal": "💼 <b>Для продолжения <u>Выберите КОШЕЛЕК</u> для сделки (на него придут ТОНы покупателя):</b>\n\n"
                                 "{wallet_list}"
                                 "{no_wallets}"
                                 "\n\n<blockquote>🔗Можно <i><b>ввести новый адрес</b></i> или выбрать существующий</blockquote>",
        "select_wallet": "𝟐️/𝟒 <b><u>Выберите КОШЕЛЕК</u> для сделки (на него придет оплата):</b>\n\n"
                                 "{wallet_list}"
                                 "{no_wallets}"
                                 "\n\n<blockquote>🔗Можно <i><b>ввести новый адрес</b></i> или выбрать существующий</blockquote>",
        "no_saved_wallets": "Нет сохраненных кошельков",
        "commission_info": "(комиссию сервиса {percent}% оплачивает покупатель)",
        "join_deal_seller": "<b>🔗 Вы присоединились к сделке #{deal_id}</b>\n\n"
                            "🛍️ Вы продаете: {gift_name}\n"
                            "💰 Стоимость NFT: {price} TON\n"
                            "<blockquote><i>(комиссию сервиса {percent}% оплачивает покупатель, минимальная комиссия 0.01 TON)</i></blockquote>",
        "join_deal_buyer": "<b>🔗 Вы присоединились к сделке #{deal_id}</b>\n\n"
                           "🛍️ Вы покупаете: {gift_name}\n"
                           "💰 Сумма к оплате: <u><b>{price} TON</b></u>\n"
                           "<blockquote><i>Комиссия сервиса составляет {percent}% от стоимости сделки (минимальная комиссия 0.01 TON)</i></blockquote>",
        "ton_address_confirmed": "TON адрес принят! Ожидайте начала оплаты покупателем",
        "payment_required": "<b>🔗 Оплата по сделке #{deal_id}</b>\n🛍️ Вы покупаете: {gift_name}\n💰 Сумма к оплате: <b>{price} TON</b>\n<i>Комиссия сервиса составляет {percent}% от стоимости сделки</i>",
        "invalid_ton_address": "❗️НЕВЕРНЫЙ формат TON-адреса. <u><i>Попробуйте снова</i></u>❗️\n"
                               "💼 <b>Выберите КОШЕЛЕК для сделки (на него придут ТОНы покупателя):</b>\n"
                               "{wallet_list}\n"
                               "{no_wallets}\n"
                               "🤝Можно <i><b>ввести новый адрес</b></i> или выбрать существующий",
        "deal_created": "<b>Сделка создана! #{hex_id}</b>\n\n🛍️ NFT для продажи: {gift_name}\n💰 Стоимость NFT: <u>{price}</u> TON\n<blockquote><i>(комиссию сервиса {percent}% оплачивает покупатель)</i></blockquote>\n\n🔗Поделитесь ссылкой со вторым участником сделки:\n|\n|-<code>{link}</code>",
        "ton_address_accepted": "TON адрес принят! Ожидайте начала оплаты покупателем",
        "select_wallet_first": "⚠️ Сначала выберите кошелек!",
        "wallet_selected": "Активный кошелек: {wallet}",
       "selected_ton_address": "𝟑/𝟒 Выбранный TON-адрес:\n<blockquote><code>{ton_address}</code></blockquote>\n\n🔗 <u>Отправьте ссылку</u> на подарок:",
       "referral_program": "😭Реферальная программа в разработке",
       "language_selection": "🌏 Выберите язык / Choose language",
        "unknown_language": "🤔Недоступный язык",
        "buyer_enter_gift_link": "𝟐/𝟑 Отправьте ссылку на подарок 🔗",
        "deal_time_out":"Сделка #{deal_id} отменена автоматически из-за отсутствия активности",
        "leave_message":"@{username} покинул сделку #{deal_id}",
        "invalid_gift_link": "Неверный формат ссылки. Попробуйте снова:",
        "enter_price": "🆗Введите цену подарка в TON (в формате 0.01):",
        "deal_canceled": "❌ Сделка отменена",
        "price_must_be_number": "ЦЕНА должна быть числом БОЛЬШЕ 0. \n<i>Для десятичного значения используйте '.'</i>\n\nПопробуйте снова:",
        "you_leave":"Вы вышли из сделки",
        "not_leave":"Вы не можете выйти на этом этапе",
        "send_ton_payment": (
            "Оплата по сделке #{deal_id}\n"
            "\n"
            "|-💰 Переведите <b>{amount}</b> TON на адрес:\n"
            f"|<code>{Config.ADMIN_TON_ADDRESS}</code>\n"
            f"\n"
            "|-⚠️ Обязательно введите комментарий:\n|<code>{comment}</code>\n\n"
            "<blockquote>У вас 15 минут на совершение оплаты, проверка происходит автоматически</blockquote>"
        ),
        "payment_started_notification": "Покупатель начал оплату. Ожидайте подтверждения.",
        "payment_timeout": "⏰ Срок оплаты истёк. Сделка отменена.",
        "payment_confirmed": "✅ Оплата подтверждена! Ожидайте передачи подарка...\n\n"
                             "<blockquote>Передача зафиксируется автоматически. Если через 15 минут подарок не перейдет к вам в профиль, TON вернутся на счет</blockquote>",
        "payment_received_notification": "🎁 Оплата получена от @{username}. Передайте NFT покупателю.\n\n"
                                         "<blockquote>Передача зафиксируется автоматически, у вас 15 минут на это</blockquote>",
        "payment_timeout_refund": "⏳ Время истекло. Начинаем возврат средств...",
        "deal_completed_buyer": "✅ NFT получен! Сделка завершена\n\nНовости об обновлениях Mivelon Guarantor в [официальном канале]({link}) 🚀",
        "deal_completed_seller": "✅ Сделка завершена! Вам переведено {price} TON\n\nНовости об обновлениях Mivelon Guarantor в [официальном канале]({link}) 🚀",
        "transfer_money_error":"❌ Ошибка перевода средств. Свяжитесь с поддержкой.",
        "your_wallets": "<b>💼 Ваши КОШЕЛЬКИ:</b>",
        "enter_ton_address_prompt": "📥 <b>Введите адрес TON-кошелька</b>\n\nПример: EQ... или UQ...",
        "wallet_invalid_address_format": "⚠️ <b>Неверный формат адреса!</b>\n\n <i>Адрес должен начинаться с EQ или UQ и содержать 48 символов</i>",
        "wallet_added_success": "✅ <b>Кошелек добавлен!</b>",
        "select_wallet_to_delete": "👇 Выберите кошелек для удаления:",
        "no_wallets_to_delete": "❌ У вас нет сохраненных кошельков",
        "wallet_selection_error": "❌Ошибка выбора кошелька",
        "confirm_wallet_deletion": "😕Удалить кошелек?\n\n{wallet}",
        "success_delete": "✅ Кошелек удален!",
        "already_full": "Ой, а тут уже все есть"

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
        "transfer_nft_button": "📦 Transfer NFT",
        "tonkeep": "💸Go to Tonkeeper",
        "russian": "🇷🇺Russian",
        "english": "🇺🇸English",
        # Полностью переведённые ключи с сохранением форматирования
        "menu_message": '🤙 You\'re still in <b>Mivelon Guarantor</b>, our bot is:\n\n'
                        '<i>🔘 Secure NFT gift deals\n'
                        '🔘️ Unique wallet management system\n'
                        '🔘 Automatic gift transfer verification</i>\n\n'
                        'Create a deal or join an existing one\n\n'
                        '<blockquote><i>ALL JULY commission is 1%</i></blockquote>',

        "welcome_message": '🤙 Welcome to <b>Mivelon Guarantor</b>, our bot is:\n\n'
                           '<i>🔘 Secure NFT gift deals\n'
                           '🔘️ Unique wallet management system\n'
                           '🔘 Automatic gift transfer verification</i>\n\n'
                           'Create a deal or join an existing one\n\n'
                           '<blockquote><i>ALL JULY commission is 1%</i></blockquote>',

        "role_selection": "𝟏 Choose ROLE\n\n"
                          "🔘<b>Seller</b> - current gift owner\n"
                          "🔘<b>Buyer</b> - pays TON\n\n"
                          "<blockquote><i>You need a <u>gift link</u> to create a deal</i></blockquote>",

        "deal_not_found": "Deal not found. Check HEX code.",
        "already_participant": "You are already a participant of this deal.",
        "seller_joined": "Seller @{username} [{user_id}] joined the deal!\n\n"
                         "🔘Deals as seller: {userbuyer_deals}\n"
                         "🔘Deals as buyer: {userseller_deals}\n"
                         "🔘<b>Total deals: {deals}</b>\n\n"
                         "<blockquote>Check if this is the same user you talked to</blockquote>",

        "buyer_joined": "Buyer @{username} [{user_id}] joined the deal!\n\n"
                        "🔘Deals as seller: {userbuyer_deals}\n"
                        "🔘Deals as buyer: {userseller_deals}\n"
                        "🔘<b>Total deals: {deals}</b>\n\n"
                        "<blockquote>Check if this is the same user you talked to</blockquote>",

        "select_wallet_for_deal": "💼 <b>To continue <u>Select WALLET</u> for deal (TONs will come here):</b>\n\n"
                                  "{wallet_list}"
                                  "{no_wallets}"
                                  "\n\n<blockquote>🔗You can <i><b>enter new address</b></i> or select existing</blockquote>",

        "select_wallet": "𝟐/𝟒 <b><u>Select WALLET</u> for deal (payment will come here):</b>\n\n"
                         "{wallet_list}"
                         "{no_wallets}"
                         "\n\n<blockquote>🔗You can <i><b>enter new address</b></i> or select existing</blockquote>",

        "no_saved_wallets": "No saved wallets",
        "commission_info": "(service fee {percent}% paid by buyer)",
        "join_deal_seller": "<b>🔗 You joined deal #{deal_id}</b>\n\n"
                            "🛍️ You're selling: {gift_name}\n"
                            "💰 NFT price: {price} TON\n"
                            "<blockquote><i>(service fee {percent}% paid by buyer, minimum fee 0.01 TON)</i></blockquote>",

        "join_deal_buyer": "<b>🔗 You joined deal #{deal_id}</b>\n\n"
                           "🛍️ You\'re buying: {gift_name}\n"
                           "💰 Amount to pay: <u><b>{price} TON</b></u>\n"
                           "<blockquote><i>Service fee is {percent}% of deal amount (minimum fee 0.01 TON)</i></blockquote>",

        "ton_address_confirmed": "TON address accepted! Waiting for buyer's payment.",
        "payment_required": "<b>🔗 Payment for deal #{deal_id}</b>\n🛍️ You're buying: {gift_name}\n💰 Amount to pay: <b>{price} TON</b>\n<i>Service fee is {percent}% of deal amount</i>",
        "invalid_ton_address": "❗️INVALID TON address format. <u><i>Try again</i></u>❗️\n"
                               "💼 <b>Select DEAL WALLET (TONs will come here):</b>\n"
                               "{wallet_list}\n"
                               "{no_wallets}\n"
                               "🤝You can <i><b>enter new address</b></i> or select existing",

        "deal_created": "<b>Deal created! #{hex_id}</b>\n\n🛍️ NFT for sale: {gift_name}\n💰 NFT price: <u>{price}</u> TON\n<blockquote><i>(service fee {percent}% paid by buyer)</i></blockquote>\n\n🔗Share link with second participant:\n|\n|-<code>{link}</code>",
        "ton_address_accepted": "TON address accepted! Waiting for buyer's payment.",
        "select_wallet_first": "⚠️ Please select a wallet first!",
        "wallet_selected": "Active wallet: {wallet}",
        "selected_ton_address": "𝟑/𝟒 Selected TON address:\n<blockquote><code>{ton_address}</code></blockquote>\n\n🔗 <u>Send gift link</u>:",

        "referral_program": "😭 Referral program under development",
        "language_selection": "🌏 Select language / Choose language",
        "unknown_language": "🤔 Unsupported language",
        "buyer_enter_gift_link": "𝟐/𝟑 Send gift link 🔗",
        "deal_time_out": "Deal #{deal_id} canceled automatically due to inactivity",
        "leave_message": "@{username} left deal #{deal_id}",
        "invalid_gift_link": "Invalid link format. Try again:",
        "enter_price": "🆗Enter gift price in TON (format 0.01):",
        "deal_canceled": "❌ Deal canceled",
        "price_must_be_number": "PRICE must be a number GREATER THAN 0.\n<i>Use '.' for decimal values</i>\n\nTry again:",
        "you_leave": "You left the deal",
        "not_leave": "You cannot leave at this stage",
        "send_ton_payment": (
            "Payment for deal #{deal_id}\n"
            "\n"
            "|-💰 Send <b>{amount}</b> TON to address:\n"
            f"|<code>{Config.ADMIN_TON_ADDRESS}</code>\n"
            f"\n"
            "|-⚠️ Enter comment:\n|<code>{comment}</code>\n\n"
            "<blockquote>You have 15 minutes for payment, verification is automatic</blockquote>"
        ),
        "payment_started_notification": "Buyer started payment. Waiting for confirmation.",
        "payment_timeout": "⏰ Payment time expired. Deal canceled.",
        "payment_confirmed": "✅ Payment confirmed! Waiting for gift transfer...\n\n"
                             "<blockquote>Transfer will be verified automatically. If gift doesn't appear in your profile in 15 minutes, TON will be returned</blockquote>",

        "payment_received_notification": "🎁 Payment received from @{username}. Transfer NFT to buyer.\n\n"
                                         "<blockquote>Transfer will be verified automatically, you have 15 minutes</blockquote>",

        "payment_timeout_refund": "⏳ Time expired. Starting refund...",
        "deal_completed_buyer": "✅ NFT received! Deal completed\n\nNews about Mivelon Guarantor updates in [official channel]({link}) 🚀",
        "deal_completed_seller": "✅ Deal completed! You received {price} TON\n\nNews about Mivelon Guarantor updates in [official channel]({link}) 🚀",
        "transfer_money_error": "❌ Funds transfer error. Contact support.",
        "your_wallets": "<b>💼 YOUR WALLETS:</b>",
        "enter_ton_address_prompt": "📥 <b>Enter TON wallet address</b>\n\nExample: EQ... or UQ...",
        "wallet_invalid_address_format": "⚠️ <b>Invalid address format!</b>\n\n <i>Address must start with EQ or UQ and contain 48 characters</i>",
        "wallet_added_success": "✅ <b>Wallet added!</b>",
        "select_wallet_to_delete": "👇 Select wallet to delete:",
        "no_wallets_to_delete": "❌ You have no saved wallets",
        "wallet_selection_error": "❌ Wallet selection error",
        "confirm_wallet_deletion": "😕Delete wallet?\n\n{wallet}",
        "success_delete": "✅ Wallet deleted!",
        "already_full": "Oops, everything's already here"
    }

        # ... остальные ключи
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