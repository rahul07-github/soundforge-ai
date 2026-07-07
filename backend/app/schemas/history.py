from datetime import datetime
from pydantic import BaseModel


class HistoryResponse(BaseModel):
    id: int
    user_id: int
    song_id: int
    created_at: datetime
    action: str

    class Config:
        from_attributes = True