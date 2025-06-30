from datetime import datetime, timedelta
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, InstrumentedAttribute

from database.models import Base, Deal, User, Refund # Импорт модели Deal [[3]]
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
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                wallets=[wallet_address] if wallet_address else [],
                active_wallet=wallet_address
            )
            session.add(user)
        else:
            if wallet_address and wallet_address not in user.wallets:
                user.wallets.append(wallet_address)
        session.commit()
def get_user_wallets(telegram_id: int) -> list:
    """Получает все кошельки пользователя"""
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    return user.wallets if user else []

def add_user_wallet(telegram_id: int, wallet_address: str):
    print(f" кошелек {wallet_address} сохранен для {telegram_id}")
    with Session() as session:  # Создаем новую сессию
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=None,
                wallets=[wallet_address],
                active_wallet=wallet_address
            )
            session.add(user)
        else:
            if wallet_address not in user.wallets:
                user.wallets = [*user.wallets, wallet_address]
                user.active_wallet = wallet_address  # Автоматически делаем новый кошелек активным
        session.commit()

def set_active_wallet(telegram_id: int, wallet_address: str):
    print(f"Активный кошелек {wallet_address} установлен для {telegram_id}")
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user and wallet_address in user.wallets:
        user.active_wallet = wallet_address
        session.commit()


def delete_user_wallet(telegram_id: int, wallet_address: str):
    """Удаляет кошелек из списка пользователя"""
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user and wallet_address in user.wallets:
            # Удаляем кошелек из списка
            user.wallets = [w for w in user.wallets if w != wallet_address]

            # Если удаляемый кошелек был активным
            if user.active_wallet == wallet_address:
                # Если остались кошельки - выбираем первый
                if user.wallets:
                    user.active_wallet = user.wallets[0]
                else:
                    user.active_wallet = None

            session.commit()

def get_user_language(telegram_id: int) -> InstrumentedAttribute | None:
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    return user.language if user and user.language in ['ru', 'en'] else 'ru'

def update_user_language(telegram_id: int, language: str):
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        user.language = language
        session.commit()
    else:
        # Создаем нового пользователя с выбранным языком
        new_user = User(telegram_id=telegram_id, language=language)
        session.add(new_user)
        session.commit()

def create_refund(
    deal_id: str,                # HEX как строка
    wallet_address: str,
    refund_amount: float,
):
    refund = Refund(
        deal_id=deal_id,
        wallet_address=wallet_address,
        refund_amount=refund_amount,
    )
    session.add(refund)
    session.commit()

def check_refund_exists( deal_id: str) -> bool:
    return session.query(Refund).filter(Refund.deal_id == deal_id).first() is not None

def get_active_deals():
    """Получает все сделки со статусом 'created' старше 1 часа"""
    threshold = datetime.utcnow() - timedelta(hours=1)
    return session.query(Deal).filter(
        Deal.status == 'created',
        Deal.date < threshold
    ).all()

def check_status(hex_id: str) -> bool:
    """Проверяет статус сделки"""
    deal = session.query(Deal).filter_by(id=hex_id).first()
    if deal.status== 'created':
        return True
    else:
        return False


def exit_deal(hex_id, user_id: int) -> int | None:
    """Выходит из сделки, удаляя user_id из seller_id или buyer_id, и возвращает id оставшегося участника."""
    deal = session.query(Deal).filter_by(id=hex_id).first()

    if not deal:
        return None

    remaining_id = None
    if deal.seller_id == user_id:
        remaining_id = deal.buyer_id
        deal.seller_id = None
    elif deal.buyer_id == user_id:
        remaining_id = deal.seller_id
        deal.buyer_id = None

    session.commit()
    return remaining_id

def get_username(telegram_id: int) -> InstrumentedAttribute | None:
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    return user.username