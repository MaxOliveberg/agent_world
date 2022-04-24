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

    Methods:
        validate(self, ticker): Bool
            Returns true if and only if the given ticker is equal to this currencies ticker

        assert_ticker(self, ticker)
            Throws an IncorrectTickerException if self.validate(ticker) is False
    """

    def __init__(self, amount, ticker):
        self.amount = amount
        self.ticker = ticker

    def __eq__(self, other):
        return self.amount == other.amount and self.ticker == other.ticker

    def __str__(self):
        return str(self.ticker) + ": " + str(self.amount)

    def validate(self, ticker):
        """
        Returns true if and only if the given ticker is equal to that of this currency
        :param ticker: Any
        :return: Bool
        """
        return ticker == self.ticker

    def assert_ticker(self, ticker):
        """
        Throws an IncorrectTickerException if self.validate(ticker) is False
        :param ticker: Any
        :return: None
        :raises: IncorrectTickerException
        """
        if self.validate(ticker) is False:
            raise IncorrectTickerException


class ICurrencyDeposit:
    """
    Interface for any class that has to recieve currency.

    Methods:
        deposit_currency(self, currency: Currency)
            Deposits the currency into this object.
    """

    def deposit_currency(self, currency: Currency):
        raise NotImplementedError


class IWallet(ICurrencyDeposit):
    """
    Interface for a generic wallet.

    Extends:
        ICurrencyDeposit

    Methods:
        check_balance(self, ticker): float
            Returns the balance of the given ticker contained in this wallet.

        withdraw(self, amount, ticker): Currency
            Withdraws currency of the given ticker from this wallet.

        withdraw_all(self, ticker): Currency
            Withdraws all currency of the given ticker contained in this wallet.

        withdraw_all_currencies(self): [Currency]
            Withdraws all currencies contained in this wallet.

        can_afford(self, price: dict): Bool todo: Using dicts as prices is dumb.
            Returns true if and only if the wallets contains geq the amounts given in the dictionary pairs.

        subtract(self, price: dict) todo: Burning currency like this is dumb.
            Subtracts/"burns" the currency corresponding to the dict

    """

    def deposit_currency(self, currency: Currency):
        """
        Inherited from ICurrencyDeposit
        :param currency: Currency
        :return: None
        """
        raise NotImplementedError

    def check_balance(self, ticker):
        """
        Returns the balance of the given ticker contained in this wallet.
        :param ticker: Any
        :return: None
        """
        raise NotImplementedError

    def withdraw(self, amount, ticker):
        """
        Withdraws currency of the given ticker from this wallet.
        :param amount: float
        :param ticker: Any
        :return: Currency
        """
        raise NotImplementedError

    def withdraw_all(self, ticker):
        """
        Withdraws all currency of the given ticker contained in this wallet.
        :param ticker: Any
        :return: Currency
        """
        raise NotImplementedError

    def withdraw_all_currencies(self):
        """
        Withdraws all currencies contained in this wallet.
        :return: [Currency]
        """
        raise NotImplementedError

    def can_afford(self, price: dict):
        """
        Returns true if and only if the wallets contains geq the amounts given in the dictionary pairs.
        :param price: dict
        :return: Bool
        """
        raise NotImplementedError

    def subtract(self, price: dict):
        """
        Subtracts/"burns" the currency corresponding to the dict
        :param price: dict
        :return: None
        """
        raise NotImplementedError


class InsufficientBalanceException(Exception):
    pass


class UnsupportedCurrencyException(Exception):
    pass


class NegativeCurrencyException(Exception):
    pass


def _check_negative(amount):
    """
    Checks if the amount is negative. If so, throws a NegativeCurrencyException
    :param amount:
    :return:
    """
    if amount < 0:
        raise NegativeCurrencyException


class Wallet(IWallet):
    """
    A class used to manage currency

    Extends
        IWallet

    Attributes

        __whitelist: bool
            Whether the wallet has a whitelist of accepted currencies. Setting whitelist to false will
            ensure that no UnsupportedCurrencyExceptions' are ever thrown.

        __wallet: dict
            A dictionary used to manage the currencies

    """

    def can_afford(self, price):
        """
        Inherited from IWallet.
        :param price: dict
        :return: Bool
        :raises: UnsupportedCurrencyException
        """
        for key, value in price.items():
            # Calling check balance here handles exceptions properly
            if self.check_balance(key) < value:
                return False
        return True

    def subtract(self, price):
        """
        Inherited from IWallet.
        :param price: dict
        :return: Bool
        :raises: UnsupportedCurrencyException
        :raises: InsufficientBalanceException
        """
        if self.can_afford(price):
            for key, value in price.items():
                self.withdraw(value, key)
        else:
            raise InsufficientBalanceException

    def withdraw_all_currencies(self):
        """
        Inherited from IWallet
        :return: [Currency]
        """
        ret = []
        for key in self.__wallet:
            # For some reason I can't iterate as key, value here?
            if self.__wallet[key] > 0:
                ret.append(Currency(self.__wallet[key], key))
                self.__wallet[key] = 0
        return ret

    def __init__(self, supported_currencies=None):
        self.__whitelist = supported_currencies is not None
        self.__wallet = {}
        if supported_currencies:
            for currency in supported_currencies:
                self.__wallet[currency] = 0

    def deposit_currency(self, currency: Currency):
        """
        Inherited from IWallet(ICurrencyDeposit)
        :param currency: Currency
        :return: None
        :raises: UnsupportedCurrencyException
        """
        _check_negative(currency.amount)
        try:
            self.__wallet[currency.ticker] += currency.amount
        except KeyError:
            if self.__whitelist:
                raise UnsupportedCurrencyException
            else:
                self.__wallet[currency.ticker] = 0
                self.deposit_currency(currency)  # Recursion dumb? DRY but not KISS

    def check_balance(self, ticker):
        """
        Inherited from IWallet.
        :param ticker: str
        :return: float
        :raises: UnsupportedCurrencyException
        """
        try:
            return self.__wallet[ticker]
        except KeyError:
            if self.__whitelist:
                raise UnsupportedCurrencyException
            else:
                return 0

    def withdraw(self, amount, ticker):
        """
        Inherited from IWallet
        :param amount: float
        :param ticker: str
        :return: Currency
        :raises: UnsupportedCurrencyException
        :raises: InsufficientBalanceException
        """
        _check_negative(amount)
        try:
            if self.__wallet[ticker] >= amount:
                self.__wallet[ticker] -= amount
                return Currency(amount, ticker)
        except KeyError:
            if self.__whitelist:
                raise UnsupportedCurrencyException
        raise InsufficientBalanceException

    def withdraw_all(self, ticker):
        """
        Inherited from IWallet
        :param ticker: Any
        :return: Currency
        :raises: UnsupportedCurrencyException
        """
        return self.withdraw(self.check_balance(ticker), ticker)
