class InvalidTimeException(Exception):
    pass


class AlreadySubscribedToClockException(Exception):
    pass


class IClockDelegate:
    def set_time(self, time):
        raise NotImplementedError


class IClock:
    # todo: This is essentially a listener pattern and could be abstracted further
    def current_time(self):
        raise NotImplementedError

    def subscribe(self, delegate: IClockDelegate):
        raise NotImplementedError

    def unsubscribe(self, delegate: IClockDelegate):
        raise NotImplementedError

    def unsubscribe_all(self):
        raise NotImplementedError

    def advance_time_by(self, delta_time):
        raise NotImplementedError

    def set_time_to(self, time):
        raise NotImplementedError


class Clock(IClock):
    """
    A clock object to drive time forward in game simulations

    Extends

        IClock

    Attributes

        _subscribers: [IClockDelegate]
            Subscribers to the time defined by the clock

        _current_time: Int
            The current time

    Methods:

    current_time(self) -> int
        Returns the current time, _current_time

    subscribe(self, delegate: IClockDelegate): -> None
        Subscribes delegate to clock
        Throws AlreadySubscribedToClockException

    unsubscribe(self, delegate: IClockDelegate): -> None
        Unsubscribes delegate from this clock, if it is subscribed.

    unsubscribe_all(self): -> None
        Removes all subscribers

    advance_time_by(self, delta_time): -> None
        Advances time to _current_time + delta_time
        Throws InvalidTimeException

    set_time_to(self, time): -> None
        Sets _current_time to time.
        Throws InvalidTimeException


    """

    # Todo: Subscribers should never be subscribed to more than one clock
    def __init__(self, starting_time=0):
        self._subscribers = []
        self._current_time = starting_time

    def current_time(self):
        """
        :return: int
        """
        return self._current_time

    def subscribe(self, delegate: IClockDelegate):
        """
        :param delegate: IClockDelegate
        :return: None
        """
        if delegate not in self._subscribers:
            self._subscribers.append(delegate)
        else:
            raise AlreadySubscribedToClockException

    def unsubscribe(self, delegate: IClockDelegate):
        """
        :param delegate: IClockDelegate
        :return: None
        """
        self._subscribers.remove(delegate)

    def unsubscribe_all(self):
        """
        :return: None
        """
        self._subscribers = []

    def advance_time_by(self, delta_time):
        """
        :param delta_time: int
        :return: None
        """
        self.set_time_to(self._current_time + delta_time)

    def set_time_to(self, time):
        """
        :param time: int
        :return: None
        """
        if time > self._current_time:
            self._current_time = time
            for subscriber in self._subscribers:
                subscriber.set_time(self._current_time)
        else:
            raise InvalidTimeException
