import math
from datetime import datetime
from enum import Enum


class Consts(Enum):
    """
    Constants used in the fee calculation
    """

    BASE_FEE = 200
    BASE_FEE_THRESHOLD = 1000
    MAX_FEE = 1500
    FREE_DELIVERY_THRESHOLD = 20000
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
        self, cart_value: int, distance: int, items: int, time: datetime
    ) -> int:
        """
        Calculate delivery fee based on cart value, distance, number of items and time of delivery
        This is the only mehtod that should be used outside of this class during runtime
        Fee is multiplied by 1.2 if it's rush hour
        Returns fee, but not more than 1500
        """

        if cart_value >= Consts.FREE_DELIVERY_THRESHOLD.value:
            return 0

        cart_fee = self._calculate_cart_value_fee(cart_value)
        distance_fee = self._calculate_distance_fee(distance)
        item_fee = self._calculate_item_fee(items)

        fee = distance_fee + item_fee + cart_fee

        final_fee = (
            int(fee * Consts.RUSH_HOUR_MULTIPLIER.value)
            if self._is_friday_rush(time)
            else fee
        )
        return min(final_fee, Consts.MAX_FEE.value)

    def _calculate_cart_value_fee(self, cart_value: int) -> int:
        """
        Calculates cart value fee based on cart value
        If cart value is over 1000, returns 0
        If cart value is under 1000, returns the counted surcharge
        """
        if cart_value >= Consts.CART_VALUE_THRESHOLD.value:
            return 0
        return Consts.CART_VALUE_THRESHOLD.value - cart_value

    def _calculate_distance_fee(self, distance: int) -> int:
        """
        Calculates distance fee based on distance
        If distance is under 1000, returns 200
        If distance is over 1000, returns 100 for every additional 500 meters + 200
        Math.ceil is used to round up the number of additional 500 meters
        """
        if distance <= Consts.BASE_FEE_THRESHOLD.value:
            return Consts.BASE_FEE.value

        return (
            Consts.BASE_FEE.value
            + math.ceil(
                (distance - Consts.BASE_FEE_THRESHOLD.value)
                / Consts.ADDITIONAL_DISTANCE_INTERVAL.value
            )
            * Consts.ADDITIONAL_DISTANCE_CHARGE.value
        )

    def _calculate_item_fee(self, items: int) -> int:
        """
        Calculates item fee based on number of items
        If number of items is under 4, returns 0
        If number of items is over 4 and under 12, returns 50 for every additional item
        If number of items is over 12, returns 50 for every additional item + 120
        """
        if items <= Consts.EXTRA_ITEM_CHARGE_THRESHOLD.value:
            return 0

        extra_item_charge_multiplier = items - Consts.EXTRA_ITEM_CHARGE_THRESHOLD.value

        if items <= Consts.BULK_CHARGE_THRESHOLD.value:
            return extra_item_charge_multiplier * Consts.EXTRA_ITEM_CHARGE.value

        return (
            extra_item_charge_multiplier * Consts.EXTRA_ITEM_CHARGE.value
            + Consts.BULK_CHARGE.value
        )

    def _is_friday_rush(self, time: datetime) -> bool:
        """
        Check if it's Friday and between 15:00 and 19:00
        """
        is_friday = time.weekday() == Consts.FRIDAY.value

        is_rush_hour = (
            Consts.RUSH_HOUR_START.value <= time.hour < Consts.RUSH_HOUR_END.value
        )

        return is_friday and is_rush_hour
