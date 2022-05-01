import pytest

from src.agent_world.currency.currency import Currency, IncorrectTickerException, NegativeCurrencyException, \
    _check_negative, Wallet, BurnedCurrencyException, _check_burned


def test_validate_ticker():
    cash = Currency(1, "Cash")
    assert cash.validate("Cash")
    assert cash.validate("Crash") is False


def test_assert_ticker():
    cash = Currency(1, "Cash")
    with pytest.raises(IncorrectTickerException):
        cash.assert_ticker("Crash")


def test_raise_negative_exception():
    with pytest.raises(NegativeCurrencyException):
        Currency(-1, "USD")
    with pytest.raises(NegativeCurrencyException):
        _check_negative(-1)


def test_burned():
    currency = Currency(1, "USD")
    wallet = Wallet()
    wallet.deposit_currency(currency)
    with pytest.raises(BurnedCurrencyException):
        wallet.deposit_currency(currency)
    with pytest.raises(BurnedCurrencyException):
        _check_burned(currency)
