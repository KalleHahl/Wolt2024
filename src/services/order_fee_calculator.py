import math
from datetime import datetime


class FeeCalculator:
    def __init__(self):
        self._base_fee = 200
        self._additional_distance = 100
        self._extra_item_fee = 50
        self._bulk_fee = 120
        self._max_fee_value = 1500
        self._free_delivery = 20000

    def calculate_fee(self, order):
        if order.cart_value >= self._free_delivery:
            return 0
        cart_fee = self._cart_value(order.cart_value)
        distance_fee = self._distance_fee(order.delivery_distance)
        item_fee = self._item_fee(order.number_of_items)
        fee = distance_fee + item_fee + cart_fee
        fee = fee * 1.2 if self._friday_rush(order.time) else fee
        return min(fee, self._max_fee_value)

    def _cart_value(self, cart_value):
        if cart_value >= 1000:
            return 0
        return 1000 - cart_value

    def _distance_fee(self, distance):
        if distance <= 1000:
            return self._base_fee

        return (
            self._base_fee
            + math.ceil((distance - 1000) / 500) * self._additional_distance
        )

    def _item_fee(self, items):
        if items <= 4:
            return 0
        if items <= 12:
            return (items - 4) * self._extra_item_fee
        return 9 * self._extra_item_fee + (items - 12) * self._bulk_fee

    def _friday_rush(self, time):
        time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        friday = time.weekday() == 4
        rush_hour = 15 <= time.hour < 19

        if friday and rush_hour:
            return True

        return False
