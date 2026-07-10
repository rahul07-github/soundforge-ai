from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database.connection import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)

    plan = Column(String(50), nullable=False)

    amount = Column(Float, nullable=False)

    payment_status = Column(String(20), default="SUCCESS")

    transaction_id = Column(String(100), unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)