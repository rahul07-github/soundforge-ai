from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User

from app.schemas.payment import (
    MockPaymentRequest,
    PaymentResponse,
)

from app.services.payment_service import process_mock_payment


router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
) 


@router.post(
    "/mock",
    response_model=PaymentResponse
)
def mock_payment(
    payment: MockPaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    result = process_mock_payment(
    db=db,
    user=current_user,
    plan=payment.plan,
)
    return result