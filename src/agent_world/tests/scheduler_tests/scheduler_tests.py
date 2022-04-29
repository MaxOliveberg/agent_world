import unittest

from src.agent_world.scheduler.IScheduler import ScheduledEvent
from src.agent_world.scheduler.scheduler import Scheduler
from src.agent_world.tests.scheduler_tests.test_helpers import _load_scheduler, _generate_sequential_events


class TestScheduler(unittest.TestCase):

    def test_advancing_time_to(self):
        scheduler = _load_scheduler(5)
        scheduler.set_time(3)
        self.assertEqual(1, scheduler._queue.size())

    # Deprecated clock_tests
    # def test_advancing_time_by(self):
    #     num_events = 10
    #     scheduler = _load_scheduler(num_events)
    #     for i in range(num_events):
    #         scheduler.advance_time_by(1)
    #         self.assertEqual(num_events - (i + 1), scheduler._queue.size())

    def test_lambda_execution(self):
        num_events = 10
        res_holder = _StringBuilderTestHelper()
        expect = ""
        scheduler = Scheduler(current_time=-1)
        current_time = 0
        for i in range(num_events):
            expect += str(i)
            scheduler.schedule_event(ScheduledEvent(lambda: res_holder.add_number(i), i))
        for i in range(num_events):
            scheduler.set_time(current_time)
            current_time += 1
        self.assertEqual(expect, res_holder.res_str)

    def test_scheduling_invalid_events(self):
        events = _generate_sequential_events(10)
        scheduler = Scheduler(current_time=5)
        scheduler.schedule_events(events)
        res_str = ""
        for event in scheduler._queue:
            res_str += event.identifier
        self.assertEqual("56789", res_str)

    def test_empty_queue(self):
        scheduler = Scheduler(0)
        try:
            scheduler.set_time(100)
        except AttributeError:
            self.fail("Threw some exception")

    def runTest(self):
        self.test_advancing_time_to()
        # self.test_advancing_time_by()
        self.test_lambda_execution()
        self.test_scheduling_invalid_events()
        self.test_empty_queue()


class _StringBuilderTestHelper:
    def __init__(self):
        self.res_str = ""

    def add_number(self, i):
        self.res_str += str(i)


if __name__ == "__main__":
    unittest.main()
