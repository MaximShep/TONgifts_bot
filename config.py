from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
# Загрузка переменных окружения из .env файла
load_dotenv(".env")
# Расшифровка seed-фразы [[5]]
# CIPHER_KEY = os.getenv("CIPHER_KEY").encode()
# ENCRYPTED_PRIVATE_KEY = os.getenv("ENCRYPTED_PRIVATE_KEY").encode()
# cipher = Fernet(CIPHER_KEY)
# PRIVATE_KEY = cipher.decrypt(ENCRYPTED_PRIVATE_KEY).decode()


class Config:
    # Конфигурации бота
    BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен из @BotFather [[1]]
    TONAPI_TOKEN = os.getenv("TONAPI_TOKEN")
    DATABASE_URL = "sqlite:///database/db.db"
    BOT_USERNAME = os.getenv("BOT_USERNAME")
    # Параметры TON SDK
    ADMIN_TON_ADDRESS = os.getenv("ADMIN_TON_ADDRESS")  # Адрес админского кошелька [[9]]
    COMMISSION_PERCENT = float(os.getenv("COMMISSION_PERCENT"))  # Комиссия 5%
    REFERAL_COMMISSION = float(os.getenv("REFERAL_COMMISSION"))  # Комиссия 5%
    # PRIVATE_KEY = PRIVATE_KEY
    MNEMONICS = os.getenv("MNEMONICS").split()