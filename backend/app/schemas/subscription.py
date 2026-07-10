from pydantic import BaseModel


class SubscriptionResponse(BaseModel):
    plan_name: str
    free_generations: int
    status: str

    class Config:
        from_attributes = True