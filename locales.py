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
        "give_me_money":"💸Вывести TON",
        "russian": "🇷🇺Русский",
        "english": "🇺🇸English",
        "arabian": "العربية🇦🇪",
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
        "already_full": "Ой, а тут уже все есть",
        "canceled": "Сделка была отменена!",
        "invalid_link_format": "❌Неверный формат ссылки",
        "invalid_referral_link": "❌Неверная реферальная ссылка",
        "new_referral": "🤙У вас новый реферал @{username}!",
        "referral_program": (
            "🤝РЕФЕРАЛЬНАЯ программа, ваша ссылка:\n\n"
            "<code>{link}</code>\n\n"
            "🔘Количество приведенных пользователей: <u><b>{count}</b></u>\n"
            "🔘Заработано: <u><b>{revenue}</b></u>\n"
            "<blockquote>{commission}% с комиссии бота со сделок рефералов</blockquote>\n\n"
            "💳Активный кошелек: \n<i>{active_wallet}</i>\n"
            "<blockquote>Вывести средства можно только от <u>1 TON</u></blockquote>"
        ),
        "payout_success": "Средства выведены на {wallet}",
        "insufficient_funds": "Недостаточно TON для вывода",
        "add_wallet_first": "Добавьте кошелек для вывода средств",
        "no_wallets": "Добавьте кошелек",
        "no_username": "❌ Для использования этого бота вам необходимо установить username (имя пользователя) в настройках Telegram!"
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
        "give_me_money": "💸Withdraw TON",
        "russian": "🇷🇺Russian",
        "english": "🇺🇸English",
        "arabian": "العربية🇦🇪",
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
        "already_full": "Oops, everything's already here",
        "canceled": "The deal has been cancelled!",
        "invalid_link_format": "❌Invalid link format",
        "invalid_referral_link": "❌Invalid referral link",
        "new_referral": "🤙You have a new referral @{username}!",
        "referral_program": (
            "🤝Referral program, your link:\n\n"
            "<code>{link}</code>\n\n"
            "🔘Referrals invited: <u><b>{count}</b></u>\n"
            "🔘Earned: <u><b>{revenue}</b></u>\n"
            "<blockquote>{commission}% from bot's fee from referral deals</blockquote>\n\n"
            "💳Active wallet: <i>{active_wallet}</i>\n"
            "<blockquote>Minimum payout is <u>1 TON</u></blockquote>"
        ),
        "payout_success": "Funds sent to {wallet}",
        "insufficient_funds": "Insufficient balance for payout",
        "add_wallet_first": "Add a wallet to receive payouts",
        "no_wallets": "No wallets added",
        "no_username": "❌ To use this bot, you need to set username in the Telegram settings!"
    },
    "AR": {
        "role_seller": "🎁 البائع",
        "role_buyer": "💸 المشتري",
        "back_button": "🔙 رجوع",
        "wallet_button": "💸 المحفظة",
        "referral_button": "🫂 الإحالة",
        "create_deal": "🚀 إنشاء صفقة",
        "language_button": "🌍 اللغة",
        "support_button": "🤝 الدعم",
        "done_button": "تم",
        "confirm_payment": "تأكيد الدفع",
        "start_payment": "الانتقال إلى الدفع",
        "add_wallet": "➕ إضافة",
        "delete_wallet": "❌ حذف",
        "back_to_menu": "🔙 إلى القائمة",
        "back_to_wallets": "🔙 إلى المحافظ",
        "delete_button": "❌ حذف",
        "cancel_button": "🔙 إلغاء",
        "cancel_deal": "❌ إلغاء الصفقة",
        "proceed_button": "متابعة ➡️",
        "leave_button": "❌ مغادرة",
        "close_button": "إغلاق",
        "tonkeep": "💸 الانتقال إلى Tonkeeper",
        "transfer_nft_button": "📦 تحويل NFT",
        "give_me_money": "💸 سحب TON",
        "russian": "🇷🇺 Русский",
        "english": "🇺🇸 English",
        "arabian": "العربية🇦🇪",
        "menu_message": '🤙 ما زلت معنا في <b>Mivelon Guarantor</b>، بوتنا يقدم:\n'
                        "<i>🔘 معاملات آمنة مع هدايا NFT\n"
                        "🔘 نظام إدارة محافظ فريد\n"
                        "🔘 التحقق التلقائي من نقل الهدية</i>\n"
                        "أنشئ صفقة أو انضم إلى صفقة موجودة\n"
                        "<blockquote><i>رسوم 1% طوال شهر يوليو</i></blockquote>",
        "welcome_message": '🤙 أهلاً بك في <b>Mivelon Guarantor</b>، بوتنا يوفر:\n'
                           "<i>🔘 معاملات آمنة مع هدايا NFT\n"
                           "🔘 نظام إدارة محافظ فريد\n"
                           "🔘 التحقق التلقائي من نقل الهدية</i>\n"
                           "أنشئ صفقة أو انضم إلى صفقة موجودة\n"
                           "<blockquote><i>رسوم 1% طوال شهر يوليو</i></blockquote>",
        "role_selection": "𝟏 اختر دورك\n"
                          "🔘<b>البائع</b> - المالك الحالي للهدية\n"
                          "🔘<b>المشتري</b> - الشخص الذي يدفع العملات\n"
                          "<blockquote><i>لإنشاء صفقة تحتاج إلى <u>رابط الهدية</u>.</i></blockquote>",
        "deal_not_found": "الصفقة غير موجودة. تحقق من الكود HEX.",
        "already_participant": "أنت بالفعل أحد المشاركين في هذه الصفقة.",
        "seller_joined": "انضم البائع @{username} [{user_id}] إلى الصفقة!\n"
                         "🔘 صفقات بدور البائع: {userbuyer_deals}\n"
                         "🔘 صفقات بدور المشتري: {userseller_deals}\n"
                         "🔘<b>إجمالي الصفقات {deals}</b>\n"
                         "<blockquote>تأكد من أنك تتحدث مع نفس المستخدم</blockquote>",
        "buyer_joined": "انضم المشتري @{username} [{user_id}] إلى الصفقة!\n"
                        "🔘 صفقات بدور البائع: {userbuyer_deals}\n"
                        "🔘 صفقات بدور المشتري: {userseller_deals}\n"
                        "🔘<b>إجمالي الصفقات {deals}</b>\n"
                        "<blockquote>تأكد من أنك تتحدث مع نفس المستخدم</blockquote>",
        "select_wallet_for_deal": "💼 <b>لمتابعة العملية، <u>اختر محفظتك</u> (سيتم تحويل الأموال إليها):</b>\n"
                                  "{wallet_list}\n"
                                  "{no_wallets}\n"
                                  "<blockquote>🔗 يمكنك <i><b>إدخال عنوان جديد</b></i> أو اختيار واحد موجود</blockquote>",
        "select_wallet": "𝟐️/𝟒 <b><u>اختر محفظة</u> لتلقي الأموال:</b>\n"
                         "{wallet_list}\n"
                         "{no_wallets}\n"
                         "<blockquote>🔗 يمكنك <i><b>إدخال عنوان جديد</b></i> أو اختيار واحد موجود</blockquote>",
        "no_saved_wallets": "لا يوجد محافظ محفوظة",
        "commission_info": "(الرسوم {percent}% يدفعها المشتري)",
        "join_deal_seller": "<b>🔗 لقد انضممت إلى الصفقة #{deal_id}</b>\n"
                            "🛍️ أنت تبيع: {gift_name}\n"
                            "💰 قيمة NFT: {price} TON\n"
                            "<blockquote><i>(الرسوم {percent}% يدفعها المشتري، الحد الأدنى للرسوم 0.01 TON)</i></blockquote>",
        "join_deal_buyer": "<b>🔗 لقد انضممت إلى الصفقة #{deal_id}</b>\n"
                           "🛍️ أنت تشترِي: {gift_name}\n"
                           "💰 المبلغ المستحق: <u><b>{price} TON</b></u>\n"
                           "<blockquote><i>الرسوم هي {percent}% من قيمة الصفقة (الحد الأدنى للرسوم 0.01 TON)</i></blockquote>",
        "ton_address_confirmed": "تم قبول عنوان TON! انتظر بدء دفع المشتري",
        "payment_required": "<b>🔗 الدفع للصفقة #{deal_id}</b>\n"
                            "🛍️ أنت تشترِي: {gift_name}\n"
                            "💰 المبلغ المستحق: <b>{price} TON</b>\n"
                            "<i>الرسوم هي {percent}% من قيمة الصفقة</i>",
        "invalid_ton_address": "❗️ تنسيق العنوان غير صحيح. <u><i>حاول مرة أخرى</i></u> ❗️\n"
                               "💼 <b>اختر محفظة لتلقي الأموال:</b>\n"
                               "{wallet_list}\n"
                               "{no_wallets}\n"
                               "<blockquote>🤝يمكنك <i><b>إدخال عنوان جديد</b></i> أو اختيار واحد موجود</blockquote>",
        "deal_created": "<b>تم إنشاء الصفقة! #{hex_id}</b>\n"
                        "🛍️ NFT المعروضة للبيع: {gift_name}\n"
                        "💰 السعر: <u>{price}</u> TON\n"
                        "<blockquote><i>(الرسوم {percent}% يدفعها المشتري)</i></blockquote>\n"
                        "🔗 شارك الرابط مع الطرف الآخر:\n"
                        "|\n"
                        "|-<code>{link}</code>",
        "ton_address_accepted": "تم قبول عنوان TON! انتظر بدء دفع المشتري",
        "select_wallet_first": "⚠️ اختر محفظة أولاً!",
        "wallet_selected": "المحفظة النشطة: {wallet}",
        "selected_ton_address": "𝟑/𝟒 العنوان المحدد:\n"
                                "<blockquote><code>{ton_address}</code></blockquote>\n"
                                "🔗 <u>أرسل رابط الهدية</u>:",
        "referral_program": "😭 برنامج الإحالة قيد التطوير",
        "language_selection": "🌏 اختر اللغة / Choose language",
        "unknown_language": "🤔 اللغة غير متاحة",
        "buyer_enter_gift_link": "𝟐/𝟑 أرسل رابط الهدية 🔗",
        "deal_time_out": "الصفقة #{deal_id} ألغيت تلقائيًا بسبب عدم النشاط",
        "leave_message": "@{username} غادر الصفقة #{deal_id}",
        "invalid_gift_link": "رابط غير صحيح. حاول مرة أخرى:",
        "enter_price": "🆗 أدخل سعر الهدية بـTON (مثال: 0.01):",
        "deal_canceled": "❌ الصفقة ألغيت",
        "price_must_be_number": "يجب أن يكون السعر رقمًا أكبر من 0.\n"
                                "<i>استخدم '.' للأرقام العشرية</i>\n"
                                "حاول مرة أخرى:",
        "you_leave": "لقد غادرت الصفقة",
        "not_leave": "لا يمكنك المغادرة في هذه المرحلة",
        "send_ton_payment": (
            "الدفع للصفقة #{deal_id}\n"
            "\n"
            "|- 💰 حوّل <b>{amount}</b> TON إلى العنوان التالي:\n"
            f"|<code>{Config.ADMIN_TON_ADDRESS}</code>\n"
            f"\n"
            "|- ⚠️ يجب كتابة التعليق التالي:\n"
            "|<code>{comment}</code>\n"
            "<blockquote>لديك 15 دقيقة لإكمال الدفع، وسيتم التحقق تلقائيًا</blockquote>"
        ),
        "payment_started_notification": "بدأ المشتري الدفع. انتظر التأكيد.",
        "payment_timeout": "⏰ انتهت مدة الدفع. الصفقة ألغيت.",
        "payment_confirmed": "✅ تم تأكيد الدفع! انتظر استلام الهدية...\n"
                             "<blockquote>سيتم تسجيل التحويل تلقائيًا. إذا لم تستلم الهدية خلال 15 دقيقة، سيتم إعادة الأموال</blockquote>",
        "payment_received_notification": "🎁 تم استلام الدفع من @{username}. قم بنقل الـNFT للمشتري.\n"
                                         "<blockquote>سيتم تسجيل التحويل تلقائيًا، لديك 15 دقيقة لذلك</blockquote>",
        "payment_timeout_refund": "⏳ الوقت انتهى. نبدأ بإرجاع الأموال...",
        "deal_completed_buyer": "✅ تم استلام NFT! الصفقة اكتملت\n"
                                "تابعوا آخر أخبار Mivelon Guarantor في [القناة الرسمية]({link}) 🚀",
        "deal_completed_seller": "✅ الصفقة اكتملت! تم تحويل {price} TON إليك\n"
                                 "تابعوا آخر أخبار Mivelon Guarantor في [القناة الرسمية]({link}) 🚀",
        "transfer_money_error": "❌ خطأ في تحويل الأموال. تواصل مع الدعم.",
        "your_wallets": "<b>💼 محافظك:</b>",
        "enter_ton_address_prompt": "📥 <b>أدخل عنوان محفظة TON</b>\n"
                                    "مثال: EQ... أو UQ...",
        "wallet_invalid_address_format": "⚠️ <b>تنسيق العنوان غير صحيح!</b>\n"
                                         "<i>يجب أن يبدأ العنوان بـ EQ أو UQ ويحتوي على 48 رمزًا</i>",
        "wallet_added_success": "✅ <b>تمت إضافة المحفظة!</b>",
        "select_wallet_to_delete": "👇 اختر المحفظة التي تريد حذفها:",
        "no_wallets_to_delete": "❌ ليس لديك محافظ محفوظة",
        "wallet_selection_error": "❌ خطأ في اختيار المحفظة",
        "confirm_wallet_deletion": "هل ترغب في حذف المحفظة؟\n{wallet}",
        "success_delete": "✅ تم حذف المحفظة!",
        "already_full": "عذرًا، كل شيء موجود هنا بالفعل",
        "canceled": "الصفقة ألغيت!",
        "invalid_link_format": "❌ رابط غير صحيح",
        "invalid_referral_link": "❌ رابط إحالة غير صحيح",
        "new_referral": "🤙 لديك إحالة جديدة @{username}!",
        "referral_program": (
            "🤝 برنامج الإحالة، رابطك:\n"
            "<code>{link}</code>\n"
            "🔘 عدد المستخدمين الذين أحالتهم: <u><b>{count}</b></u>\n"
            "🔘 الأرباح: <u><b>{revenue}</b></u>\n"
            "<blockquote>{commission}% من عمولة الروبوت في صفقات الإحالات</blockquote>\n"
            "💳 المحفظة النشطة:\n"
            "<i>{active_wallet}</i>\n"
            "<blockquote>يمكنك سحب الأموال عند الوصول إلى 1 TON فقط</blockquote>"
        ),
        "payout_success": "تم تحويل الأموال إلى {wallet}",
        "insufficient_funds": "TON غير كافية للسحب",
        "add_wallet_first": "أضف محفظة لسحب الأموال",
        "no_wallets": "أضف محفظة",
        "no_username": "❌ لاستخدام هذا الروبوت، يجب عليك تعيين اسم مستخدم في إعدادات Telegram!"
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