from pydantic import BaseModel


class OrderInfo(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str


class OrderFeeResponse(BaseModel):
    delivery_fee: int
