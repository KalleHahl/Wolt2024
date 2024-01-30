from pydantic import BaseModel, PositiveInt, field_validator
from datetime import datetime


class OrderInfo(BaseModel):
    cart_value: PositiveInt
    delivery_distance: PositiveInt
    number_of_items: PositiveInt
    time: str

    @field_validator("time")
    def validate_time_is_ISO(cls, time_str: str) -> datetime:
        """
        Validator to check if time string is UTC in ISO format and converts it to a datetime object if it is
        If it's not, raises a ValueError
        """
        try:
            time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
            return time
        except:
            raise ValueError("Date must be UTC in ISO format")


class OrderFeeResponse(BaseModel):
    delivery_fee: PositiveInt
