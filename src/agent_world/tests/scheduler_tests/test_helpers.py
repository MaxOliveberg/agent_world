from src.agent_world.scheduler.scheduler import ScheduledEvent, Scheduler


def _generate_sequential_events(num):
    """
    Generates a list of ScheduledEvents with times 0, 1, 2... num and a trivial function
    :param num: int
    :return: [ScheduledEvents]
    """
    ret = []
    for i in range(num):
        ret.append(ScheduledEvent(_empty_function, i, str(i)))
    return ret


def _load_scheduler(num_events=5):
    """
    Loads a scheduler with sequential events
    :param num_events: int
    :return: Scheduler
    """
    scheduler = Scheduler(current_time=-1)
    events = _generate_sequential_events(num_events)
    scheduler.schedule_events(events)
    return scheduler


def _empty_function():
    """
    Empty function
    :return: None
    """
    pass
