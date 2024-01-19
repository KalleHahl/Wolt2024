from fastapi import FastAPI

from src.models.order import OrderInfo
from src.services.order_fee_calculator import FeeCalculator

app = FastAPI()

calculator = FeeCalculator()


@app.get("/")
def main_route():
    return {"message": "moi"}


@app.post("/delivery_fee")
def delivery_fee(order: OrderInfo):
    cart_value = order.cart_value
    distance = order.delivery_distance
    items = order.number_of_items
    time = order.time
    fee = calculator.calculate_fee(cart_value, distance, items, time)
    return {"delivery_fee": fee}
