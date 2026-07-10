import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.user import User


def process_mock_payment(
    db: Session,
    user: User,
    plan: str
):
    transaction_id = "MOCK_" + uuid.uuid4().hex[:8].upper()

    if plan.lower() == "premium":
        amount = 299
    elif plan.lower() == "pro":
        amount = 599
    else:
        amount = 0

    payment = Payment(
        user_id=user.id,
        plan=plan,
        amount=amount,
        payment_status="SUCCESS",
        transaction_id=transaction_id,
    )

    db.add(payment)

    user.plan = plan
    user.subscription_start = datetime.utcnow()
    user.subscription_end = datetime.utcnow() + timedelta(days=30)

    db.commit()

    db.refresh(payment)
    db.refresh(user)

    return {
        "message": "Payment Successful",
        "transaction_id": transaction_id
    }