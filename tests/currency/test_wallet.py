import pytest

from src.agent_world.currency.currency import Wallet, Currency, UnsupportedCurrencyException, \
    InsufficientBalanceException


# Todo: Add negative currency exception clock
def test_deposit_no_whitelist():
    wallet = Wallet()
    currency = Currency(10, "USD")
    wallet.deposit_currency(currency)
    assert 10 == wallet.check_balance("USD")


def test_deposit_whitelist():
    wallet = Wallet(["USD"])
    currency = Currency(10, "USD")
    wallet.deposit_currency(currency)
    assert 10 == wallet.check_balance("USD")


def test_invalid_deposit_whitelist():
    wallet = Wallet(["USD"])
    currency = Currency(10, "SEK")
    with pytest.raises(UnsupportedCurrencyException):
        wallet.deposit_currency(currency)


def test_withdrawal():
    wallet = Wallet()
    wallet.deposit_currency(Currency(10, "USD"))
    currency = wallet.withdraw(5, "USD")
    assert Currency(5, "USD") == currency
    assert 5 == wallet.check_balance("USD")
    assert 0 == wallet.check_balance("SEK")

    whitelist_wallet = Wallet(["USD"])
    with pytest.raises(UnsupportedCurrencyException):
        whitelist_wallet.check_balance("SEK")


def test_invalid_withdrawal_whitelist():
    wallet = Wallet(["USD"])
    with pytest.raises(UnsupportedCurrencyException):
        wallet.withdraw(10, "SEK")


def test_insufficient_balance():
    wallet = Wallet()
    currency = Currency(1, "USD")
    wallet.deposit_currency(currency)
    with pytest.raises(InsufficientBalanceException):
        wallet.withdraw(10, "USD")


def test_can_afford():
    wallet = Wallet()
    currency_usd = Currency(1, "USD")
    currency_sek = Currency(1, "SEK")
    wallet.deposit_currency(currency_usd)
    wallet.deposit_currency(currency_sek)
    assert wallet.can_afford({"USD": 1, "SEK": 1})
    assert wallet.can_afford({"USD": 2, "SEK": 1}) is False


def test_subtract():
    wallet = Wallet()
    currency_usd = Currency(2, "USD")
    currency_sek = Currency(2, "SEK")
    wallet.deposit_currency(currency_usd)
    wallet.deposit_currency(currency_sek)
    wallet.subtract({"USD": 1, "SEK": 1})
    assert 1 == wallet.check_balance("USD")
    assert 1 == wallet.check_balance("SEK")
    with pytest.raises(InsufficientBalanceException):
        wallet.subtract({"USD": 2, "SEK": 2})


def test_withdraw_all_currencies():
    wallet = Wallet()
    empty_list = wallet.withdraw_all_currencies()
    assert len(empty_list) == 0

    wallet.deposit_currency(Currency(1, "USD"))
    wallet.deposit_currency(Currency(1, "SEK"))
    some_money = wallet.withdraw_all_currencies()
    assert len(some_money) == 2

    no_money = wallet.withdraw_all_currencies()
    assert len(no_money) == 0


def test_withdraw_all():
    wallet = Wallet()
    wallet.deposit_currency(Currency(10, "USD"))
    my_dollars = wallet.withdraw_all("USD")
    assert my_dollars.ticker == "USD" and my_dollars.amount == 10
    assert wallet.check_balance("USD") == 0
