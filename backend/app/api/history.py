from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.auth.dependencies import get_current_user

from backend.app.models.user import User
from backend.app.models.history import History

from backend.app.schemas.history import HistoryResponse

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get(
    "/",
    response_model=list[HistoryResponse]
)
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    history = (
        db.query(History)
        .filter(History.user_id == current_user.id)
        .order_by(History.created_at.desc())
        .all()
    )

    return history 


@router.delete(
    "/{history_id}",
    status_code=status.HTTP_200_OK
)
def delete_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    history = (
        db.query(History)
        .filter(
            History.id == history_id,
            History.user_id == current_user.id
        )
        .first()
    )

    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History not found"
        )

    db.delete(history)
    db.commit()

    return {
        "message": "History deleted successfully"
    }