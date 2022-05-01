import pytest

from src.agent_world.clock.clock import Clock, IClockDelegate, InvalidTimeException, AlreadySubscribedToClockException


class ToySubscriber(IClockDelegate):
    def __init__(self, start_time=0):
        self._current_time = start_time

    def set_time(self, time):
        self._current_time = time


def test_fundamental():
    clock = Clock(starting_time=1)
    assert 1 == clock.current_time()
    assert len(clock._subscribers) == 0


def test_set_time():
    clock = Clock()
    clock.set_time_to(1)
    assert 1 == clock.current_time()


def test_set_invalid_time():
    clock = Clock(1)
    with pytest.raises(InvalidTimeException):
        clock.set_time_to(0)


def test_advance_time_by():
    clock = Clock()
    clock.advance_time_by(1)
    assert 1 == clock.current_time()


def test_advance_time_by_invalid_time():
    clock = Clock()
    with pytest.raises(InvalidTimeException):
        clock.advance_time_by(-1)


def test_subscribing():
    clock = Clock()
    toy_subscriber = ToySubscriber()
    clock.subscribe(toy_subscriber)
    assert toy_subscriber in clock._subscribers


def test_double_subscribe():
    clock = Clock()
    toy_subscriber = ToySubscriber()
    clock.subscribe(toy_subscriber)
    with pytest.raises(AlreadySubscribedToClockException):
        clock.subscribe(toy_subscriber)


def test_remove_subscribe():
    clock = Clock()
    toy_subscriber = ToySubscriber()
    clock.subscribe(toy_subscriber)
    # So that the clock does not pass if the implementation is blank
    assert toy_subscriber in clock._subscribers
    clock.unsubscribe(toy_subscriber)
    assert toy_subscriber not in clock._subscribers


def test_unsubscribe_all():
    clock = Clock()
    toy_subscribers = [ToySubscriber() for _ in range(10)]
    for sub in toy_subscribers:
        clock.subscribe(sub)
    assert len(clock._subscribers) == 10
    clock.unsubscribe_all()
    assert len(clock._subscribers) == 0


def test_set_time_subscriber():
    clock = Clock()
    toy_subscriber = ToySubscriber()
    clock.subscribe(toy_subscriber)
    clock.set_time_to(1)
    assert clock.current_time() == 1 and toy_subscriber._current_time == 1


def test_advance_time_subscriber():
    clock = Clock()
    toy_subscriber = ToySubscriber()
    clock.subscribe(toy_subscriber)
    clock.advance_time_by(1)
    assert clock.current_time() == 1 and toy_subscriber._current_time == 1
