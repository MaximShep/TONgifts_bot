import re

def validate_ton_address(address: str) -> bool:
    """
    Проверяет корректность TON-адреса с учетом дефиса [[8]]
    """
    pattern = r"^(E|U)[A-Z0-9_\-]{47}$"  # Добавлен символ '-' [[8]]
    return re.match(pattern, address.strip().upper()) is not None

def validate_price(price: str) -> bool:
    """
    Проверяет, что цена является положительным числом [[3]]
    """
    try:
        float_price = float(price)
        return float_price > 0
    except ValueError:
        return False
    
def validate_tg_nft_link(link: str) -> bool:
    """
    Проверяет корректность ссылки вида https://t.me/nft/<название>[-<номер>].
    
    :param link: Строка с ссылкой.
    :return: True, если ссылка корректна, иначе False.
    """
    # Регулярное выражение для проверки формата ссылки
    pattern = r"^https://t\.me/nft/[A-Za-z0-9_-]+(-\d+)?$"
    
    # Очистка строки и проверка на соответствие шаблону
    return re.match(pattern, link.strip()) is not None