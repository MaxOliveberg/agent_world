import unittest

from src.agent_world.currency.currency import Wallet, Currency, UnsupportedCurrencyException, \
    InsufficientBalanceException


class TestWallet(unittest.TestCase):
    # Todo: Add negative currency exception clock_tests
    def test_deposit_no_whitelist(self):
        wallet = Wallet()
        currency = Currency(10, "USD")
        wallet.deposit_currency(currency)
        self.assertEqual(10, wallet.check_balance("USD"))

    def test_deposit_whitelist(self):
        wallet = Wallet(["USD"])
        currency = Currency(10, "USD")
        wallet.deposit_currency(currency)
        self.assertEqual(10, wallet.check_balance("USD"))

    def test_invalid_deposit_whitelist(self):
        wallet = Wallet(["USD"])
        currency = Currency(10, "SEK")
        try:
            wallet.deposit_currency(currency)
            self.assertTrue(False, "Did not throw exception when depositing unsupported currency")
        except UnsupportedCurrencyException:
            self.assertTrue(True)

    def test_withdrawal(self):
        wallet = Wallet()
        wallet.deposit_currency(Currency(10, "USD"))
        currency = wallet.withdraw(5, "USD")
        self.assertEqual(Currency(5, "USD"), currency, msg="Did not successfully withdraw 5 USD")
        self.assertEqual(5, wallet.check_balance("USD"), msg="Remaining balance not 5 USD")

    def test_invalid_withdrawal_whitelist(self):
        wallet = Wallet(["USD"])
        try:
            wallet.withdraw(10, "SEK")
            self.assertTrue(False, "Managed to withdraw an unsupported currency")
        except UnsupportedCurrencyException:
            self.assertTrue(True)
        except InsufficientBalanceException:
            self.assertTrue(False, "Raised InsufficientBalanceException when UnsupportedCurrencyException was expected")

    def test_insufficient_balance(self):
        wallet = Wallet()
        currency = Currency(1, "USD")
        wallet.deposit_currency(currency)
        try:
            wallet.withdraw(10, "USD")
            self.assertTrue(False, "Managed to withdraw a balance that did not exist")
        except InsufficientBalanceException:
            self.assertTrue(True)

    def test_can_afford(self):
        wallet = Wallet()
        currency_usd = Currency(1, "USD")
        currency_sek = Currency(1, "SEK")
        wallet.deposit_currency(currency_usd)
        wallet.deposit_currency(currency_sek)
        self.assertTrue(wallet.can_afford({"USD": 1, "SEK": 1}), "Returns false despite having a sufficient balance")
        self.assertFalse(wallet.can_afford({"USD": 2, "SEK": 1}),
                         "Returns true despite not having a sufficient balance")

    def test_subtract(self):
        wallet = Wallet()
        currency_usd = Currency(2, "USD")
        currency_sek = Currency(2, "SEK")
        wallet.deposit_currency(currency_usd)
        wallet.deposit_currency(currency_sek)
        wallet.subtract({"USD": 1, "SEK": 1})
        self.assertEqual(1, wallet.check_balance("USD"), "Incorrect USD amountl")
        self.assertEqual(1, wallet.check_balance("SEK"), "Incorrect SEK amount")

    def runTest(self):
        self.test_withdrawal()
        self.test_insufficient_balance()
        self.test_deposit_whitelist()
        self.test_invalid_withdrawal_whitelist()
        self.test_deposit_no_whitelist()
        self.test_invalid_deposit_whitelist()
        self.test_can_afford()
        self.test_subtract()


if __name__ == "__main__":
    unittest.main()
