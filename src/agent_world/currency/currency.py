class IncorrectTickerException(Exception):
    pass


class Currency:
    """
    Class representing a generic currency

    Attributes

    amount: float
        Amount of the currency

    ticker: str
        A ticker used to identify which currency the object represents
    """

    def __init__(self, amount, ticker):
        self.amount = amount
        self.ticker = ticker

    def __eq__(self, other):
        return self.amount == other.amount and self.ticker == other.ticker

    def __str__(self):
        return str(self.ticker) + ": " + str(self.amount)

    def validate(self, ticker):
        return ticker == self.ticker

    def assert_ticker(self, ticker):
        if self.validate(ticker) is False:
            raise IncorrectTickerException


class ICurrencyDeposit:
    def deposit_currency(self, currency: Currency):
        raise NotImplementedError


class IWallet(ICurrencyDeposit):
    def deposit_currency(self, currency: Currency):
        raise NotImplementedError

    def check_balance(self, ticker):
        raise NotImplementedError

    def withdraw(self, amount, ticker):
        raise NotImplementedError

    def withdraw_all(self, ticker):
        raise NotImplementedError

    def withdraw_all_currencies(self):
        raise NotImplementedError

    def can_afford(self, price: dict):
        raise NotImplementedError

    def subtract(self, price: dict):
        raise NotImplementedError


class InsufficientBalanceException(Exception):
    pass


class UnsupportedCurrencyException(Exception):
    pass


class NegativeCurrencyException(Exception):
    pass


def _check_negative(amount):
    if amount < 0:
        raise NegativeCurrencyException


class Wallet(IWallet):
    """
    A class used to manage currency

    Extends
        IWallet

    Attributes

        _whitelist: bool
            Whether the wallet has a whitelist of accepted currencies

        _wallet: dict
            A dictionary used to manage the currencies

    Methods

        deposit_currency(self, currency: Currency) - None
            Deposits currency into the wallet
            Throws UnsupportedCurrencyException

        check_balance(self, ticker) - float
            Returns the balance corresponding to the provided ticker
            Throws UnsupportedCurrencyException

        withdraw(self, amount, ticker) - Currency
            Withdraws the specified amount of the ticker currency
            Throws UnsupportedCurrencyException, InsufficientBalanceException

        # Todo add new docu
    """

    def can_afford(self, price):
        # Todo: Document
        for key, value in price.items():
            # Calling check balance here handles exceptions properly
            if self.check_balance(key) < value:
                return False
        return True

    def subtract(self, price):
        # Todo: Document
        if self.can_afford(price):
            for key, value in price.items():
                self.withdraw(value, key)
        else:
            raise InsufficientBalanceException

    def withdraw_all_currencies(self):
        # Todo: Write clock_tests for this
        ret = []
        for key in self._wallet:
            # For some reason I can't iterate as key, value here?
            if self._wallet[key] > 0:
                ret.append(Currency(self._wallet[key], key))
                self._wallet[key] = 0
        return ret

    def __init__(self, supported_currencies=None):
        self._whitelist = supported_currencies is not None
        self._wallet = {}
        if supported_currencies:
            for currency in supported_currencies:
                self._wallet[currency] = 0

    def deposit_currency(self, currency: Currency):
        """
        :param currency: Currency
        :return: None
        """
        _check_negative(currency.amount)
        try:
            self._wallet[currency.ticker] += currency.amount
        except KeyError:
            if self._whitelist:
                raise UnsupportedCurrencyException
            else:
                self._wallet[currency.ticker] = 0
                self.deposit_currency(currency)  # Recursion dumb? DRY but not KISS

    def check_balance(self, ticker):
        """
        :param ticker: str
        :return: float
        """
        try:
            return self._wallet[ticker]
        except KeyError:
            if self._whitelist:
                raise UnsupportedCurrencyException
            else:
                return 0

    def withdraw(self, amount, ticker):
        """
        :param amount: float
        :param ticker: str
        :return: Currency
        """
        _check_negative(amount)
        try:
            if self._wallet[ticker] >= amount:
                self._wallet[ticker] -= amount
                return Currency(amount, ticker)
        except KeyError:
            if self._whitelist:
                raise UnsupportedCurrencyException
        raise InsufficientBalanceException

    def withdraw_all(self, ticker):
        return self.withdraw(self.check_balance(ticker), ticker)
