from pydantic import BaseModel, Field


class OrderInfo(BaseModel):
    cart_value: int = Field(..., ge=0)
    delivery_distance: int = Field(..., ge=0)
    number_of_items: int = Field(..., ge=0)
    time: str  # = Field(pattern="^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")


class OrderFeeResponse(BaseModel):
    delivery_fee: int = Field(..., ge=0)
