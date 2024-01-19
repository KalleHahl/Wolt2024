import math
from datetime import datetime


class FeeCalculator:
    BASE_FEE = 200
    BASE_FEE_THRESHOLD = 1000
    MAX_FEE = 1500
    FREE_DELIVERY = 20000
    CART_VALUE_THRESHOLD = 1000
    ADDITIONAL_DISTANCE_CHARGE = 100
    EXTRA_ITEM_CHARGE = 50
    EXTRA_ITEM_CHARGE_THRESHOLD = 4
    BULK_CHARGE = 120
    BULK_CHARGE_THRESHOLD = 12
    RUSH_HOUR_MULTIPLIER = 1.2
    RUSH_HOUR_START = 15
    RUSH_HOUR_END = 19

    def calculate_fee(
        self, cart_value: int, distance: int, items: int, time: str
    ) -> int:
        if cart_value >= self.FREE_DELIVERY:
            return 0
        cart_fee = self._cart_value(cart_value)
        distance_fee = self._distance_fee(distance)
        item_fee = self._item_fee(items)
        fee = distance_fee + item_fee + cart_fee
        parsed_time = self._parse_time(time)
        fee = (
            int(fee * self.RUSH_HOUR_MULTIPLIER)
            if self._friday_rush(parsed_time)
            else fee
        )
        return min(fee, self.MAX_FEE)

    def _cart_value(self, cart_value: int) -> int:
        if cart_value >= self.CART_VALUE_THRESHOLD:
            return 0
        return self.CART_VALUE_THRESHOLD - cart_value

    def _distance_fee(self, distance: int) -> int:
        if distance <= self.BASE_FEE_THRESHOLD:
            return self.BASE_FEE

        return (
            self.BASE_FEE
            + math.ceil((distance - self.BASE_FEE_THRESHOLD) / 500)
            * self.ADDITIONAL_DISTANCE_CHARGE
        )

    def _item_fee(self, items: int) -> int:
        if items <= self.EXTRA_ITEM_CHARGE_THRESHOLD:
            return 0
        if items <= self.BULK_CHARGE_THRESHOLD:
            return (items - self.EXTRA_ITEM_CHARGE_THRESHOLD) * self.EXTRA_ITEM_CHARGE
        return (
            9 * self.EXTRA_ITEM_CHARGE
            + (items - self.BULK_CHARGE_THRESHOLD) * self.BULK_CHARGE
        )

    def _parse_time(self, time: str) -> datetime:
        # TODO: some type of error if the time string isnt in the ISO
        return datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

    def _friday_rush(self, time: datetime) -> bool:
        friday = time.weekday() == 4
        rush_hour = self.RUSH_HOUR_START <= time.hour < self.RUSH_HOUR_END

        if friday and rush_hour:
            return True

        return False
