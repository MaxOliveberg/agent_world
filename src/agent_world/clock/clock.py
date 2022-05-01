class InvalidTimeException(Exception):
    pass


class AlreadySubscribedToClockException(Exception):
    pass


class IClockDelegate:
    """
    Delegate for the IClock interface

    Methods:
        set_time(self, time)
            Sets the time of this delegate
    """

    def set_time(self, time):
        raise NotImplementedError  # pragma: no cover


class IClock:
    # todo: This is essentially a listener pattern and could be abstracted further
    # Todo: Make current_time() a property?
    """
    Interface for a clock object, with is expected to track time through integer milliseconds.

    Methods:
        current_time(self)
            Returns the current time of this clock.

        subscribe(self, delegate: IClockDelegate):
            Subscribes a delegate to this clock.

        unsubscribe(self, delegate: IClockDelegate):
            Unsubscribes a delegate from this clock.

        unsubscribe_all(self, delegate: IClockDelegate):
            Unsubscribes all delegates from this clock.

        advance_time_by(self, delta_time)
            Sets time to current_time + delta_time.

        set_time_to(self, time)
            Sets the time of this clock and informs subscribers

    """

    def current_time(self):
        """
        Returns the current time of this clock,
        :return: int
        """
        raise NotImplementedError  # pragma: no cover

    def subscribe(self, delegate: IClockDelegate):
        """
        Subscribes a delegate to this clock.
        :param delegate: IClockDelegate
        :return: None
        """
        raise NotImplementedError  # pragma: no cover

    def unsubscribe(self, delegate: IClockDelegate):
        """
        Unsubscribes a delegate from this clock
        :param delegate: IClockDelegate
        :return: None
        """
        raise NotImplementedError  # pragma: no cover

    def unsubscribe_all(self):
        """
        Unsubscribes all delegates from this clock
        :return: None
        """
        raise NotImplementedError  # pragma: no cover

    def advance_time_by(self, delta_time):
        """
        Sets the time to current_time() + delta_time.
        :param delta_time: int
        :return: None
        """
        raise NotImplementedError  # pragma: no cover

    def set_time_to(self, time):
        """
        Sets the time to the given time.
        :param time: int
        :return: None
        """
        raise NotImplementedError  # pragma: no cover


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
        Inherited from IClock
        :return: int
        """
        return self._current_time

    def subscribe(self, delegate: IClockDelegate):
        """
        Inherited from IClock
        :param delegate: IClockDelegate
        :return: None
        """
        if delegate not in self._subscribers:
            self._subscribers.append(delegate)
        else:
            raise AlreadySubscribedToClockException

    def unsubscribe(self, delegate: IClockDelegate):
        """
        Inherited from IClock
        :param delegate: IClockDelegate
        :return: None
        """
        self._subscribers.remove(delegate)

    def unsubscribe_all(self):
        """
        Inherited from IClock
        :return: None
        """
        self._subscribers.clear()

    def advance_time_by(self, delta_time):
        """
        Inherited from IClock
        :param delta_time: int
        :return: None
        """
        self.set_time_to(self._current_time + delta_time)

    def set_time_to(self, time):
        """
        Inherited from IClock
        :param time: int
        :return: None
        """
        if time > self._current_time:
            self._current_time = time
            for subscriber in self._subscribers:
                subscriber.set_time(self._current_time)
        else:
            raise InvalidTimeException
