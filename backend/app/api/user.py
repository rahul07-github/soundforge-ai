from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.models.subscription import Subscription
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create FREE subscription
    subscription = Subscription(
        user_id=new_user.id,
        plan_name="FREE",
        free_generations=3,
        status="ACTIVE"
    )

    db.add(subscription)
    db.commit()

    return new_user


def get_user_by_email(connection: Session, email: str):
    return connection.query(User).filter(
        User.email == email
    ).first()


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get(
    "/profile",
    response_model=UserResponse
)
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user