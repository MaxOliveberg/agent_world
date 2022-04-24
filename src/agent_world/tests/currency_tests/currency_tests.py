import unittest

from src.agent_world.currency.currency import Currency, IncorrectTickerException


class TestCurrency(unittest.TestCase):

    def test_validate_ticker(self):
        cash = Currency(1, "Cash")
        self.assertTrue(cash.validate("Cash"), "Did not return true.")
        self.assertFalse(cash.validate("Crash"), "Did not return false")

    def test_assert_ticker(self):
        cash = Currency(1, "Cash")
        self.assertRaises(IncorrectTickerException, cash.assert_ticker, "Crash")

    def runTest(self):
        self.test_assert_ticker()
        self.test_assert_ticker()
