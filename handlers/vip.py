# handlers/vip.py
from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.filters import Command
from database.repository import Session
from database.repository import add_vip, is_user_vip, remove_vip_from_user, get_vip_users
from aiogram import Bot
from config import Config
import asyncio

router = Router()

CHAT_ADMINS_ID = -1002751170506  # Например: -1002751170506
MESSAGE_THREAD_ID = 205  # Например: 184




# === Формирование кнопок и текста ===
def generate_vip_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Добавить", callback_data="vip_add"),
            InlineKeyboardButton(text="➖ Удалить", callback_data="vip_remove")
        ]
    ])


async def send_vip_list(bot: Bot):
    users = get_vip_users()
    text = "<b>Список VIP пользователей:</b>\n\n"
    if not users:
        text += "Список пуст."
    else:
        for user in users:
            username = f"@{user.username} [{user.telegram_id}]" if user.username else f"ID {user.telegram_id}"
            text += f"• {username}\n"

    markup = generate_vip_keyboard()

    await bot.send_message(
        chat_id=CHAT_ADMINS_ID,
        message_thread_id=MESSAGE_THREAD_ID,
        text=text,
        reply_markup=markup,
        parse_mode="HTML"
    )


# === Обработчики инлайн кнопок ===
@router.callback_query(F.data == "vip_add")
async def handle_vip_add(callback: CallbackQuery):
    await callback.message.reply("Введите Telegram ID пользователя для добавления в VIP:")
    await callback.answer()


@router.callback_query(F.data == "vip_remove")
async def handle_vip_remove(callback: CallbackQuery):
    await callback.message.reply("Введите Telegram ID пользователя для удаления из VIP:")
    await callback.answer()


# === Обработчик текстовых сообщений ===
@router.message()
async def handle_vip_input(message: Message):
    #
    # # Проверяем, что это нужный чат
    # if message.chat.id != CHAT_ADMINS_ID:
    #     return
    #
    # # Проверяем, что это ответ на сообщение
    # if not message.reply_to_message:
    #     await message.reply("⚠️ Это должно быть ответом на сообщение бота.")
    #     return
    #
    # # Проверяем, что есть текст в reply
    # if not message.reply_to_message.text:
    #     await message.reply("⚠️ Сообщение, на которое вы отвечаете, не содержит текста.")
    #     return
    #
    # # Проверяем, что есть текст в текущем сообщении
    # if not message.text:
    #     await message.reply("⚠️ Вы должны ввести Telegram ID.")
    #     return
    #
    # # Теперь безопасно получаем текст
    reply_text = message.reply_to_message.text
    #
    # # Проверяем, является ли текст числом
    # if not message.text.isdigit():
    #     await message.reply("⚠️ Введите корректный Telegram ID (число).")
    #     return

    telegram_id = int(message.text)

    try:
        if "для добавления" in reply_text:
            add_vip(telegram_id)
            await message.reply("✅ Пользователь добавлен в VIP.")
        elif "для удаления" in reply_text:
            if remove_vip_from_user(telegram_id):
                await message.reply("❌ Пользователь удален из VIP.")
            else:
                await message.reply("⚠️ Пользователь не является VIP.")
        else:
            await message.reply("❓ Неизвестное действие.")

        await send_vip_list(message.bot)

    except Exception as e:
        print(f"[ERROR] Ошибка при обработке: {e}")
        await message.reply(f"❌ Произошла ошибка: {e}")