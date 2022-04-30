import pytest

from src.agent_world.currency.currency import Currency, IncorrectTickerException


def test_validate_ticker():
    cash = Currency(1, "Cash")
    assert cash.validate("Cash")
    assert cash.validate("Crash") is False


def test_assert_ticker():
    cash = Currency(1, "Cash")
    with pytest.raises(IncorrectTickerException):
        cash.assert_ticker("Crash")
