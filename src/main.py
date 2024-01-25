from fastapi import FastAPI

from src.models.order import OrderInfo, OrderFeeResponse
from src.services.order_fee_calculator import FeeCalculator

app = FastAPI()

calculator = FeeCalculator()


@app.get("/")
def main_route():
    return {"message": "Server is running"}


@app.post("/api/calculate_delivery_fee", response_model=OrderFeeResponse)
def delivery_fee(order: OrderInfo) -> OrderFeeResponse:
    cart_value = order.cart_value
    distance = order.delivery_distance
    items = order.number_of_items
    time = order.time
    fee = calculator.calculate_fee(cart_value, distance, items, time)  # type: ignore[arg-type]
    return OrderFeeResponse(delivery_fee=fee)
