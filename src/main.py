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
    fee = calculator.calculate_fee(order)
    return {"delivery_fee": fee}
