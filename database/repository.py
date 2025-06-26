from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Deal, User # Импорт модели Deal [[3]]
from utils.hex_generator import generate_hex_id  # Импорт генератора HEX [[9]]
from config import Config

# Подключение к БД
engine = create_engine(Config.DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_deal(sdelka_id:str, seller_id: int, buyer_id:int, ton_address: str, gift_name: str, price: float, comission_price: float) -> str:
    """Создает новую сделку и сохраняет в БД [[3]][[5]]"""
    deal = Deal(
        id = sdelka_id,  # Теперь функция доступна [[9]]
        seller_id=seller_id,
        buyer_id=buyer_id,
        ton_address=ton_address,
        gift_name=gift_name,
        price=price,
        comission_price=comission_price
    )
    session.add(deal)
    session.commit()
    return deal.id

def update_deal_buyer(deal_id: str, buyer_id: int):
    """Привязывает покупателя к сделке"""
    deal = session.query(Deal).filter_by(id=deal_id).first()
    if deal:  # Защита от None [[8]]
        deal.buyer_id = buyer_id
        session.commit()
def update_deal_seller(deal_id: str, seller_id: int):
    """Привязывает покупателя к сделке"""
    deal = session.query(Deal).filter_by(id=deal_id).first()
    if deal:  # Защита от None [[8]]
        deal.seller_id = seller_id
        session.commit()
def update_ton_address(deal_id: str, ton_address: int):
    """Привязывает покупателя к сделке"""
    deal = session.query(Deal).filter_by(id=deal_id).first()
    if deal:  # Защита от None [[8]]
        deal.ton_address = ton_address
        session.commit()
def update_address_buyer(deal_id: str, adress: int):
    """Привязывает адресс покупателя к сделке"""
    deal = session.query(Deal).filter_by(id=deal_id).first()
    if deal:  # Защита от None [[8]]
        deal.buyer_address = adress
        session.commit()
def update_deal_status(deal_id: str, status: str):
    """Обновляет статус сделки (payment_received, completed)"""
    deal = session.query(Deal).filter_by(id=deal_id).first()
    if deal:
        deal.status = status
        session.commit()

def get_deal_by_hex(hex_id: str) -> Type[Deal] | None:
    """Получает сделку по HEX-идентификатору [[3]]"""
    return session.query(Deal).filter_by(id=hex_id).first()  # Теперь возвращает объект Deal

def get_deal_by_id(new_id: str) -> Type[Deal] | None:
    """Получает сделку по HEX-идентификатору [[3]]"""
    return session.query(Deal).filter_by(id=new_id).first()  # Теперь возвращает объект Deal

def save_or_update_user(telegram_id: int, username: str, wallet_address: str = None):
    """
    Сохраняет или обновляет пользователя в таблице users.
    Если пользователь уже существует, обновляет только wallet_address (если передан).
    """
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        # Создаем нового пользователя
        user = User(telegram_id=telegram_id, username=username, wallet_address=wallet_address)
        session.add(user)
    else:
        # Обновляем существующего пользователя
        if wallet_address and user.wallet_address != wallet_address:
            user.wallet_address = wallet_address
    session.commit()