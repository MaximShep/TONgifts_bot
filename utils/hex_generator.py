import uuid

def generate_hex_id() -> str:
    """
    Генерирует уникальный HEX-идентификатор сделки [[9]]
    """
    return uuid.uuid4().hex  # 32-символьная строка без дефисов