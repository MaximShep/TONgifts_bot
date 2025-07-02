from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64

# Фиксированные ключи (НЕ ИСПОЛЬЗУЙТЕ ЭТИ КЛЮЧИ В РЕАЛЬНЫХ ПРОЕКТАХ!)
SECRET_KEY = b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10' * 2  # 32 байта для AES-256
IV = b'\x12\x34\x56\x78\x9a\xbc\xde\xf0\x0f\xed\xcb\xa9\x87\x65\x43\x21'  # 16 байт


def encode_telegram_id(telegram_id: int) -> str:
    """Детерминированное кодирование Telegram ID"""
    try:
        id_bytes = telegram_id.to_bytes(8, 'big')
        padder = padding.PKCS7(128).padder()
        padded = padder.update(id_bytes) + padder.finalize()

        cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(IV))
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded) + encryptor.finalize()

        return base64.urlsafe_b64encode(encrypted).decode('utf-8').rstrip('=')
    except Exception:
        raise ValueError("Ошибка кодирования")


def decode_telegram_id(encoded_id: str) -> int:
    """Декодирование обратно в Telegram ID"""
    try:
        padded = encoded_id + '=' * (-len(encoded_id) % 4)
        encrypted = base64.urlsafe_b64decode(padded)

        cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(IV))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        id_bytes = unpadder.update(padded_data) + unpadder.finalize()

        return int.from_bytes(id_bytes, 'big')
    except Exception:
        raise ValueError("Ошибка декодирования")