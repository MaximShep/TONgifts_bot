from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Deal(Base):
    __tablename__ = "deals"
    id = Column(String(32), primary_key=True)  # HEX-идентификатор
    seller_id = Column(Integer)  # Telegram ID продавца
    buyer_id = Column(Integer)  # Telegram ID покупателя
    ton_address = Column(String(48), nullable=False)  # Адрес продавца
    buyer_address = Column(String(48))  # Адрес продавца
    gift_name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    comission_price = Column(Float, nullable=False)
    status = Column(String(20), default="created")  # created, payment_received, completed

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(Integer, primary_key=True)
    username = Column(String(50))
    wallet_address = Column(String(48))
    # Дополнительные поля (например, рейтинг)