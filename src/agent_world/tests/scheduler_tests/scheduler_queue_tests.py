import unittest
from src.agent_world.scheduler.scheduler import _SchedulerQueue, ScheduledEvent
from src.agent_world.tests.scheduler_tests.test_helpers import _generate_sequential_events


class TestSchedulerQueue(unittest.TestCase):

    def test_add(self):
        event = ScheduledEvent(None, 0, "0")
        queue = _SchedulerQueue()
        queue.add_event(event)
        self.assertTrue(queue.is_not_empty(), "Queue does not contain any object")

    def test_add_all(self):
        events = _generate_sequential_events(5)
        queue = _SchedulerQueue()
        queue.add_all(events)
        self.assertEqual(5, queue.size())

    def test_single_remove(self):
        event = ScheduledEvent(None, 0, "0")
        queue = _SchedulerQueue()
        queue.add_event(event)
        self.assertTrue(queue.is_not_empty(), "Queue does not contain any object")
        queue.remove_event("0")
        self.assertTrue(queue.is_empty(), "Queue is not empty")

    def test_iterator(self):
        events = _generate_sequential_events(5)
        queue = _SchedulerQueue()
        queue.add_all(events)
        res_str = ""
        for event in queue:
            res_str += event.identifier
        self.assertEqual("01234", res_str)

    def test_remove(self):
        events = _generate_sequential_events(5)
        queue = _SchedulerQueue()
        queue.add_all(events)
        queue.remove_event("2")
        res_str = ""
        for event in queue:
            res_str += event.identifier
        self.assertEqual("0134", res_str)

    def test_timed_iterator(self):
        events = _generate_sequential_events(5)
        queue = _SchedulerQueue()
        queue.add_all(events)
        res_str = ""
        for event in queue.timed_iter(3):
            res_str += event.identifier
        self.assertEqual("0123", res_str)

    def runTest(self):
        self.test_add()
        self.test_remove()
        self.test_add_all()
        self.test_iterator()
        self.test_remove()
        self.test_timed_iterator()


if __name__ == "__main__":
    unittest.main()
