import math
from datetime import datetime
from enum import Enum


class FeeCalculatorConstants(Enum):
    BASE_FEE = 200
    BASE_FEE_THRESHOLD = 1000
    MAX_FEE = 1500
    FREE_DELIVERY = 20000
    CART_VALUE_THRESHOLD = 1000
    ADDITIONAL_DISTANCE_CHARGE = 100
    ADDITIONAL_DISTANCE_INTERVAL = 500
    EXTRA_ITEM_CHARGE = 50
    EXTRA_ITEM_CHARGE_THRESHOLD = 4
    BULK_CHARGE = 120
    BULK_CHARGE_THRESHOLD = 12
    RUSH_HOUR_MULTIPLIER = 1.2
    RUSH_HOUR_START = 15
    RUSH_HOUR_END = 19
    FRIDAY = 4


class FeeCalculator:
    def calculate_fee(
        self, cart_value: int, distance: int, items: int, time: str
    ) -> int:
        if cart_value >= FeeCalculatorConstants.FREE_DELIVERY.value:
            return 0
        cart_fee = self._cart_value(cart_value)
        distance_fee = self._distance_fee(distance)
        item_fee = self._item_fee(items)
        fee = distance_fee + item_fee + cart_fee
        parsed_time = self._parse_time(time)
        fee = (
            int(fee * FeeCalculatorConstants.RUSH_HOUR_MULTIPLIER.value)
            if self._is_friday_rush(parsed_time)
            else fee
        )
        return min(fee, FeeCalculatorConstants.MAX_FEE.value)

    def _cart_value(self, cart_value: int) -> int:
        if cart_value >= FeeCalculatorConstants.CART_VALUE_THRESHOLD.value:
            return 0
        return FeeCalculatorConstants.CART_VALUE_THRESHOLD.value - cart_value

    def _distance_fee(self, distance: int) -> int:
        if distance <= FeeCalculatorConstants.BASE_FEE_THRESHOLD.value:
            return FeeCalculatorConstants.BASE_FEE.value

        return (
            FeeCalculatorConstants.BASE_FEE.value
            + math.ceil(
                (distance - FeeCalculatorConstants.BASE_FEE_THRESHOLD.value)
                / FeeCalculatorConstants.ADDITIONAL_DISTANCE_INTERVAL.value
            )
            * FeeCalculatorConstants.ADDITIONAL_DISTANCE_CHARGE.value
        )

    def _item_fee(self, items: int) -> int:
        if items <= FeeCalculatorConstants.EXTRA_ITEM_CHARGE_THRESHOLD.value:
            return 0

        extra_item_charge_multiplier = (
            items - FeeCalculatorConstants.EXTRA_ITEM_CHARGE_THRESHOLD.value
        )

        if items <= FeeCalculatorConstants.BULK_CHARGE_THRESHOLD.value:
            return (
                extra_item_charge_multiplier
                * FeeCalculatorConstants.EXTRA_ITEM_CHARGE.value
            )

        return (
            extra_item_charge_multiplier
            * FeeCalculatorConstants.EXTRA_ITEM_CHARGE.value
            + FeeCalculatorConstants.BULK_CHARGE.value
        )

    def _parse_time(self, time: str) -> datetime:
        # TODO: some type of error if the time string isnt in the ISO
        return datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

    def _is_friday_rush(self, time: datetime) -> bool:
        is_friday = time.weekday() == FeeCalculatorConstants.FRIDAY.value
        is_rush_hour = (
            FeeCalculatorConstants.RUSH_HOUR_START.value
            <= time.hour
            < FeeCalculatorConstants.RUSH_HOUR_END.value
        )

        if is_friday and is_rush_hour:
            return True

        return False
