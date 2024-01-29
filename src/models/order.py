from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class OrderInfo(BaseModel):
    cart_value: int = Field(..., ge=0)
    delivery_distance: int = Field(..., ge=0)
    number_of_items: int = Field(..., ge=0)
    time: str

    @field_validator("time")
    def validate_time_is_ISO(cls, time_str: str) -> datetime:
        """Validator to check if time is UTC in ISO format and convert it to datetime object"""
        try:
            time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
            return time
        except:
            raise ValueError("Date must be UTC in ISO format")


class OrderFeeResponse(BaseModel):
    delivery_fee: int = Field(..., ge=0)
