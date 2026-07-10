from pydantic import BaseModel


class MockPaymentRequest(BaseModel):
    plan: str


class PaymentResponse(BaseModel):
    message: str
    transaction_id: str