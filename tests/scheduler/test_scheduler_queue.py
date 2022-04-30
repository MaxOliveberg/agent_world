import pytest
from src.agent_world.scheduler.scheduler import _SchedulerQueue
from src.agent_world.scheduler.IScheduler import ScheduledEvent
from tests.scheduler.scheduler_test_helpers import _generate_sequential_events


def test_add():
    event = ScheduledEvent(None, 0, "0")
    queue = _SchedulerQueue()
    queue.add_event(event)
    assert queue.is_not_empty()


def test_add_all():
    events = _generate_sequential_events(5)
    queue = _SchedulerQueue()
    queue.add_all(events)
    assert 5, queue.size()


def test_single_remove():
    event = ScheduledEvent(None, 0, "0")
    queue = _SchedulerQueue()
    queue.add_event(event)
    assert queue.is_not_empty()
    queue.remove_event("0")
    assert queue.is_empty()


def test_iterator():
    events = _generate_sequential_events(5)
    queue = _SchedulerQueue()
    queue.add_all(events)
    res_str = ""
    for event in queue:
        res_str += event.identifier
    assert "01234" == res_str


def test_remove():
    events = _generate_sequential_events(5)
    queue = _SchedulerQueue()
    queue.add_all(events)
    queue.remove_event("2")
    res_str = ""
    for event in queue:
        res_str += event.identifier
    assert "0134" == res_str


def test_timed_iterator():
    events = _generate_sequential_events(5)
    queue = _SchedulerQueue()
    queue.add_all(events)
    res_str = ""
    for event in queue.timed_iter(3):
        res_str += event.identifier
    assert "0123" == res_str
