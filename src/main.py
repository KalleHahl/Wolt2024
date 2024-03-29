from fastapi import FastAPI, Depends

from src.models.order import OrderInfo, OrderFeeResponse
from src.services.order_fee_calculator import FeeCalculator

app = FastAPI()


def create_calculator() -> FeeCalculator:
    return FeeCalculator()


@app.get("/")
def main_route():
    """
    Main route to check if server is running
    """
    return {"message": "Server is running"}


@app.post("/api/calculate_delivery_fee", response_model=OrderFeeResponse)
def delivery_fee(
    order: OrderInfo, calculator: FeeCalculator = Depends(create_calculator)
) -> OrderFeeResponse:
    """
    Endpoint to calculate delivery fee based on cart value, distance, number of items and time of delivery
    """
    cart_value = order.cart_value
    distance = order.delivery_distance
    items = order.number_of_items
    time = order.time
    fee = calculator.calculate_fee(cart_value, distance, items, time)  # type: ignore[arg-type]
    return OrderFeeResponse(delivery_fee=fee)
