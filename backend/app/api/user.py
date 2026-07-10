from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse, UserLogin
from backend.app.auth.security import hash_password
from backend.app.auth.security import verify_password, create_access_token
from backend.app.auth.dependencies import get_current_user

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

    
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    
    hashed_password = hash_password(user.password)

    
    new_user = User(
    username=user.username,
    email=user.email,
    hashed_password=hashed_password
)

    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user  


def get_user_by_email(connection: Session, email: str):
    return connection.query(User).filter(User.email == email).first()




@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.hashed_password):
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