import unittest
from datetime import datetime
from src.services.order_fee_calculator import FeeCalculator
from src.services.order_fee_calculator import FeeCalculatorConstants


class TestFeeCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = FeeCalculator()
        self.friday_rush = "2024-01-19T18:00:00Z"
        self.not_friday_rush = "2024-01-14T18:00:00Z"

    def test_cart_value_under_threshold(self):
        return_value = self.calculator._cart_value(700)
        self.assertEqual(300, return_value)

    def test_cart_value_over_threshhold(self):
        return_value = self.calculator._cart_value(1100)
        self.assertEqual(0, return_value)

    def test_distance_fee_under_base_fee_treshhold(self):
        return_value = self.calculator._distance_fee(900)
        self.assertEqual(200, return_value)

    def test_distance_fee_over_base_fee_treshhold(self):
        return_value = self.calculator._distance_fee(1001)
        self.assertEqual(300, return_value)

    def test_item_fee_under_extra_item_charge_threshold(self):
        return_value = self.calculator._item_fee(3)
        self.assertEqual(0, return_value)

    def test_item_fee_over_extra_item_charge_under_bulk_threshold(self):
        return_value = self.calculator._item_fee(7)
        self.assertEqual(150, return_value)

    def test_item_fee_over_bulk_threshold(self):
        return_value = self.calculator._item_fee(13)
        self.assertEqual(570, return_value)

    def test_parse_time(self):
        return_value = self.calculator._parse_time(self.friday_rush)
        self.assertIsInstance(return_value, datetime)

    def test_not_friday_rush(self):
        parsed_time = self.calculator._parse_time(self.not_friday_rush)
        self.assertFalse(self.calculator._is_friday_rush(parsed_time))

    def test_is_friday_rush(self):
        parsed_time = self.calculator._parse_time(self.friday_rush)
        self.assertTrue(self.calculator._is_friday_rush(parsed_time))

    def test_calculate_fee(self):
        cart_value = 790
        delivery_distance = 2235
        number_of_items = 4
        return_value = self.calculator.calculate_fee(
            cart_value, delivery_distance, number_of_items, self.not_friday_rush
        )
        self.assertEqual(710, return_value)

    def test_calculate_fee_cart_value_over_free_delivery_treshold(self):
        cart_value = FeeCalculatorConstants.FREE_DELIVERY.value
        delivery_distance = 1540
        number_of_items = 15
        return_value = self.calculator.calculate_fee(
            cart_value, delivery_distance, number_of_items, self.not_friday_rush
        )
        self.assertEqual(0, return_value)

    def test_calculate_fee_friday_rush(self):
        cart_value = 790
        delivery_distance = 2235
        number_of_items = 4
        return_value = self.calculator.calculate_fee(
            cart_value, delivery_distance, number_of_items, self.friday_rush
        )
        self.assertEqual(852, return_value)
