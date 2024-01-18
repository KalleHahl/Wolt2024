from fastapi import FastAPI
from pydantic import BaseModel


class OrderInfo(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str


app = FastAPI()


@app.get("/")
def main_route():
    return {"message": "moi"}


@app.post("/delivery_fee")
def delivery_fee(order: OrderInfo):
    return order
