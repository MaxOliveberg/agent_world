import pytest

from src.agent_world.scheduler.IScheduler import ScheduledEvent
from src.agent_world.scheduler.scheduler import Scheduler
from tests.scheduler.scheduler_test_helpers import _load_scheduler, _generate_sequential_events


def test_advancing_time_to():
    """
    The logic here is a bit unclear:

    1. Load a scheduler with 5 events to be executed at times 0, 1 ... 4
    2. Advance time to 3 so that all but the last event are executed
    3. Assert that only one event is still in the scheduler.

    todo: Dumb to access _queue() that should be private.
    """
    scheduler = _load_scheduler(5)
    scheduler.set_time(3)
    assert 1 == scheduler._queue.size()


def test_lambda_execution():
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
    assert expect == res_holder.res_str


def test_scheduling_invalid_events():
    events = _generate_sequential_events(10)
    scheduler = Scheduler(current_time=5)
    scheduler.schedule_events(events)
    res_str = ""
    for event in scheduler._queue:
        res_str += event.identifier
    assert "56789" == res_str


def test_empty_queue():
    scheduler = Scheduler(0)
    try:
        scheduler.set_time(100)
    except AttributeError:
        pytest.fail("Threw some exception")


class _StringBuilderTestHelper:
    def __init__(self):
        self.res_str = ""

    def add_number(self, i):
        self.res_str += str(i)
