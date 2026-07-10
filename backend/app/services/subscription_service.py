from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.subscription import Subscription


def check_generation_limit(user_id: int, db: Session):
    """
    Check if the user has remaining free generations.
    """

    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id)
        .first()
    )

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    # If user has exhausted free generations
    if subscription.free_generations <= 0:
        raise HTTPException(
            status_code=403,
            detail="Free limit reached. Please upgrade your plan."
        )

    return subscription


def decrease_generation(user_id: int, db: Session):
    """
    Decrease free generation count after a successful song generation.
    """

    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id)
        .first()
    )

    subscription.free_generations -= 1

    db.commit()
    db.refresh(subscription)

    return subscription