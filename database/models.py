from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, ForeignKey, JSON, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

Base = declarative_base()

class CommissionOwner(PyEnum):
    buyer = "buyer"
    seller = "seller"

class Deal(Base):
    __tablename__ = "deals"
    id = Column(String(32), primary_key=True)
    seller_id = Column(Integer)
    buyer_id = Column(Integer)
    ton_address = Column(String(48), nullable=False)
    buyer_address = Column(String(48))
    gift_name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    comission_price = Column(Float, nullable=False)
    status = Column(String(20), default="created")
    date = Column(DateTime, default=datetime.utcnow)
    commission_owner = Column(Enum(CommissionOwner), default=CommissionOwner.buyer)
    revenue = Column(Float)
    note = Column(String(255))
    extra_data = Column(JSON, default=lambda: {})

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(Integer, primary_key=True)
    username = Column(String(50))
    wallets = Column(JSON, default=lambda: [])
    active_wallet = Column(String(48))
    created_at = Column(DateTime, default=datetime.utcnow)
    invited_by = Column(Integer, ForeignKey('users.telegram_id'))
    last_activity = Column(DateTime, default=datetime.utcnow)
    dop_column = Column(JSON, default=lambda: {})
    language = Column(String(5), default='en')  # Новая колонка

    inviter = relationship("User", remote_side=[telegram_id], foreign_keys=[invited_by])