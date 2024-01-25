import unittest
from datetime import datetime
from src.services.order_fee_calculator import FeeCalculator


class TestFeeCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = FeeCalculator()
        self.friday_rush = datetime(2024, 1, 12, 18, 0, 0)
        self.not_friday_rush = datetime(2024, 1, 14, 18, 0, 0)
        self.free_delivery = 20000

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

    def test_not_friday_rush(self):
        self.assertFalse(self.calculator._is_friday_rush(self.not_friday_rush))

    def test_is_friday_rush(self):
        self.assertTrue(self.calculator._is_friday_rush(self.friday_rush))

    def test_calculate_fee(self):
        cart_value = 790
        delivery_distance = 2235
        number_of_items = 4
        return_value = self.calculator.calculate_fee(
            cart_value, delivery_distance, number_of_items, self.not_friday_rush
        )
        self.assertEqual(710, return_value)

    def test_calculate_fee_cart_value_over_free_delivery_treshold(self):
        cart_value = self.free_delivery
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
