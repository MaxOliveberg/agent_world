import unittest

from src.agent_world.clock.clock import Clock, IClockDelegate, InvalidTimeException, AlreadySubscribedToClockException


class ToySubscriber(IClockDelegate):
    def __init__(self, start_time=0):
        self._current_time = start_time

    def set_time(self, time):
        self._current_time = time


class TestClock(unittest.TestCase):

    def test_set_time(self):
        clock = Clock()
        clock.set_time_to(1)
        self.assertEqual(1, clock.current_time(), msg="Clock does not have correct time")

    def test_set_invalid_time(self):
        clock = Clock(1)
        self.assertRaises(InvalidTimeException, clock.set_time_to, 0)

    def test_advance_time_by(self):
        clock = Clock()
        clock.advance_time_by(1)
        self.assertEqual(1, clock.current_time(), msg="Time not correct")

    def test_advance_time_by_invalid_time(self):
        clock = Clock()
        self.assertRaises(InvalidTimeException, clock.advance_time_by, -1)

    def test_subscribing(self):
        clock = Clock()
        toy_subscriber = ToySubscriber()
        clock.subscribe(toy_subscriber)
        self.assertTrue(toy_subscriber in clock._subscribers, msg="Subscriber not subscribed")

    def test_double_subscribe(self):
        clock = Clock()
        toy_subscriber = ToySubscriber()
        clock.subscribe(toy_subscriber)
        self.assertRaises(AlreadySubscribedToClockException, clock.subscribe, toy_subscriber)

    def test_remove_subscribe(self):
        clock = Clock()
        toy_subscriber = ToySubscriber()
        clock.subscribe(toy_subscriber)
        # So that the clock_tests does not pass if the implementation is blank
        self.assertTrue(toy_subscriber in clock._subscribers, msg="Subscriber did not even get added")
        clock.unsubscribe(toy_subscriber)
        self.assertTrue(toy_subscriber not in clock._subscribers, msg="Subscriber not unsubscribed")

    def test_set_time_subscriber(self):
        clock = Clock()
        toy_subscriber = ToySubscriber()
        clock.subscribe(toy_subscriber)
        clock.set_time_to(1)
        self.assertTrue(clock.current_time() == 1 and toy_subscriber._current_time == 1,
                        msg="Subscriber and clock times not equal")

    def test_advance_time_subscriber(self):
        clock = Clock()
        toy_subscriber = ToySubscriber()
        clock.subscribe(toy_subscriber)
        clock.advance_time_by(1)
        self.assertTrue(clock.current_time() == 1 and toy_subscriber._current_time == 1,
                        msg="Subscriber and clock times not equal")

    def runTest(self):
        self.test_advance_time_subscriber()
        self.test_set_time()
        self.test_subscribing()
        self.test_set_time_subscriber()
        self.test_remove_subscribe()
        self.test_advance_time_by()
        self.test_advance_time_by_invalid_time()
        self.test_double_subscribe()
        self.test_set_invalid_time()


if __name__ == "__main__":
    unittest.main()
