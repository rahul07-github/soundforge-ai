from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionResponse

router = APIRouter(
    prefix="/subscription",
    tags=["Subscription"]
)


@router.get(
    "/",
    response_model=SubscriptionResponse
)
def get_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    return subscription