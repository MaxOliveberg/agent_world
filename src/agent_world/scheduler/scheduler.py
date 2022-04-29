from src.agent_world.clock.clock import IClockDelegate
from src.agent_world.scheduler.IScheduler import IScheduler


class Scheduler(IScheduler, IClockDelegate):
    """
    A class to facilitate and handle the scheduling of actions

    Extends

        IScheduler, IClockDelegate

    Attributes

        current_time: int
            The current in-world time

        _queue: _SchedulerQueue
            Queue used to store scheduled events

    Methods

        schedule_event(event: ScheduledEvent) -> None
            If the event is scheduled for the future it is added to the queue of events

        cancel_event(identifier: Equatable) -> None
            Removes the event corresponding to the given identifier from the schedule

        current_time() -> int
            Returns the current time

        schedule_events(events: [ScheduledEvent]) -> None
            Iteratively schedules all events contained in the list as per schedule_event()

        advance_time_to(time: int) -> None
            If the given time is greater than the current time, the current time is set to the time and all events
            scheduled up to and including that time are executed in order

        advance_time_by(time: int) -> None
            Calls advance_time_to(current_time + time) i.e. advances time by the given time
    """

    def __init__(self, current_time=0):
        """
        :param current_time: int
        """
        self._current_time = current_time
        self._queue = _SchedulerQueue()

    def schedule_event(self, event):
        """
        Inherited from IScheduler
        :param event: ScheduledEvent
        :return: None
        """
        if event.scheduled_time >= self._current_time:
            self._queue.add_event(event)

    def cancel_event(self, identifier):
        """
        Inherited from IScheduler
        :param identifier: Equatable
        :return: None
        """
        self._queue.remove_event(identifier)

    def current_time(self):
        """
        Inherited from IScheduler
        :return: int
        """
        return self._current_time

    def schedule_events(self, events):
        """
        Inherited from IScheduler
        :param events: [ScheduledEvent]
        :return: None
        """
        for event in events:
            # Does not use the _SchedulerQueue method due to additional constraints
            self.schedule_event(event)

    def set_time(self, time):
        """
        Sets the time of this scheduler.
        :param time: int
        :return: None
        """
        if time > self._current_time:
            self._current_time = time
            for event in self._queue.timed_iter(time):
                event.scheduled_event()


class _SchedulerQueue:
    """
    A linked list used to manage the ordering of ScheduledEvents

    Attributes

    (None)

    Implements:

    __iter__, __next__

    Methods

    add_event(event: ScheduledEvent)
        Adds event of scheduled time T to the linked list at the spot after the most recent event added which also has
        the time T

    add_all(list_of_events: [ScheduledEvent])
        Adds all events contained in the list consecutively as per the add_event method

    remove_event(identifier: Equatable)
        Removes the event of the given identifier from the list. If there are multiple occurrences of the
        same identifier, the first occurrence will be removed

    peak_first() -> ScheduledEvent?
        Returns the first ScheduledEvent of the linked list without removing it from the list.
        If the list is empty, returns None

    pop() -> ScheduledEvent?
        Pops the first object from the list. If the list is empty, returns None

    size() -> int
        Returns the size of the linked list

    is_not_empty() -> Boolean
        Returns true if the list is not empty

    is_empty() -> Boolean
        Returns true if the list is empty

    timed_iter(end_time: int) -> _FixedTimedIterator
        Returns an iterator which iterates over all events up to and including the given time 'destructively', i.e.
        the elements are popped from the list as they are iterated over.
    """

    def __init__(self):
        self.first = None

    # Various adds

    def add_event(self, event):
        """
        Adds event of scheduled time T to the linked list at the spot after the most recent event added which also has
        the time T
        :param event: ScheduledEvent
        :return: None
        """
        if self.first is None:
            self.first = _Node(event)
            return
        current = self.first
        while current.next() is not None and current.next().timestamp() <= event.scheduled_time:
            current = current.next()
        new_node = _Node(event)
        new_node.set_next(current.next())
        current.set_next(new_node)

    def add_all(self, list_of_events):
        """
        Adds all events contained in the list consecutively as per the add_event method
        :param list_of_events: [ScheduledEvent]
        :return: None
        """
        for event in list_of_events:
            self.add_event(event)

    # Various removes

    def remove_event(self, identifier):
        """
        Removes the event of the given identifier from the list. If there are multiple occurrences of the
        same identifier, the first occurrence will be removed
        :param identifier: Equatable
        :return: None
        """
        if self.is_not_empty():
            current = self.first
            if current.get_content().identifier == identifier:
                self.first = current.next()
                current.set_next(None)
                return
            else:
                while current.has_next():
                    previous = current
                    current = current.next()
                    if current.get_content().identifier == identifier:
                        previous.set_next(current.next())
                        current.set_next(None)
                        return

    # Various operators

    def peak_first(self):
        """
        Returns the first ScheduledEvent of the linked list without removing it from the list.
        If the list is empty, returns None
        :return: ScheduledEvent?
        """
        if self.first:
            return self.first.get_content()

    def pop(self):
        """
        Pops the first object from the list. If the list is empty, returns None
        :return: ScheduledEvent?
        """
        if self.first is None:
            return None
        ret = self.first
        self.first = ret.next()
        return ret.get_content()

    def size(self):
        """
        Returns the size of the linked list
        :return: int
        """
        current = self.first
        size = 0
        while current is not None:
            size += 1
            current = current.next()
        return size

    # Various boolean functions

    def is_not_empty(self):
        """
        Returns true if the list is not empty
        :return: Boolean
        """
        return self.first is not None

    def is_empty(self):
        """
        Returns true if the list is empty
        :return: Boolean
        """
        return self.first is None

    # Iterator implementation

    def __iter__(self):
        """
        :return: Iterable
        """
        self._current_iter = self.first
        return self

    def __next__(self):
        """
        :return: ScheduledEvent
        """
        if self._current_iter is not None:
            ret = self._current_iter
            self._current_iter = ret.next()
            return ret.get_content()
        else:
            raise StopIteration

    def timed_iter(self, end_time):
        """
        Returns an iterator which iterates over all events up to and including the given time 'destructively', i.e.
        the elements are popped from the list as they are iterated over.
        :param end_time: int
        :return: _FixedTimeIterator
        """
        return _FixedTimeIterator(end_time, self)


class _FixedTimeIterator:
    """
    An iterator which iterates over all events up to and including the given time 'destructively', i.e.
        the elements are popped from the list as they are iterated over.

    Attributes

    end_time: int
        The time to iterate up to and including

    queue: _SchedulerQueue
        Queue to iterate over
    """

    def __init__(self, end_time, scheduler_queue):
        """
        :param end_time: int
        :param scheduler_queue: _SchedulerQueue
        """
        self.end_time = end_time
        self.queue = scheduler_queue

    def __iter__(self):
        """
        :return: Iterable
        """

        if self.queue.is_not_empty() and self.queue.peak_first().scheduled_time <= self.end_time:
            self._current_iter = self.queue.pop()
        else:
            self._current_iter = None
        return self

    def __next__(self):
        """
        :return: ScheduledEvent
        """
        if self._current_iter is not None:
            ret = self._current_iter
            peak = self.queue.peak_first()
            if peak and peak.scheduled_time <= self.end_time:
                self._current_iter = self.queue.pop()
            else:
                self._current_iter = None
            return ret
        else:
            raise StopIteration


class _Node:
    """
    Node class to facilitate a the linked list of _SchedulerQueue

    Attributes

    _content: ScheduledEvent
        The scheduled event in this node
    _next: _Node
        The next node in the list

    Methods

    set_next(node: _Node)
        Sets _next = node

    timestamp(): int
        returns the scheduled time for the ScheduledEvent contained in the node

    has_next(): Boolean
        Returns true if this node has a _next

    next(): _Node?
        Returns the _next field, which is either a _Node or None

    get_content(): ScheduledEvent
        Returns the scheduled event contained in the node
    """

    def __init__(self, content):
        """
        :param content: ScheduledEvent
        """
        self._content = content
        self._next = None

    def set_next(self, node):
        """
        Sets _next = node
        :param node: _Node?
        :return: None
        """
        self._next = node

    def timestamp(self):
        """
        returns the scheduled time for the ScheduledEvent contained in the node
        :return: int
        """
        return self._content.scheduled_time

    def has_next(self):
        """
        Returns true if this node has a _next
        :return: Boolean
        """
        return self._next is not None

    def next(self):
        """
        Returns the _next field, which is either a _Node or None
        :return: _Node?
        """
        return self._next

    def get_content(self):
        """
        Returns the scheduled event contained in the node
        :return: ScheduledEvent
        """
        return self._content
