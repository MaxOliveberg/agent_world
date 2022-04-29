class ScheduledEvent:
    """
    A class representing an action or event related to the world being simulated

    Attributes

    scheduled_event: lambda
        Function corresponding to the action/event to be executed at the scheduled time

    scheduled_time: int
        Time in milliseconds when the event should be executed

    identifier: Equatable = None
        An identifier for the scheduled event, currently the concern of the implementation. Ideally this should be
        unique and lightweight, such as a string, integer or data class.

    """

    def __init__(self, scheduled_event, scheduled_time, identifier=None):
        """
        :param scheduled_event: lambda
        :param scheduled_time: int
        :param identifier: Equatable
        """
        self.scheduled_event = scheduled_event
        self.scheduled_time = scheduled_time
        self.identifier = identifier


class IScheduler:
    """
    Interface defining how a "scheduler" operates, an object which will execute lambdas at set times in the future

    Methods:
        current_time(self): int
            Returns the  current time of this scheduler

        schedule_event(self, event)
            Schedules the event

        schedule_events(self, events)
            Schedules a collection of events

        cancel_event(self, identifier)
            Cancels an event identified by the provided identifier.
    """

    def current_time(self):
        """
        Returns the  current time of this scheduler
        :return: int
        """
        raise NotImplementedError

    def schedule_event(self, event: ScheduledEvent):
        """
        Schedules the event
        :param event: ScheduledEvent
        :return: None
        """
        raise NotImplementedError

    def schedule_events(self, events):
        """
        :param events: [ScheduledEvent]
        :return: None
        """
        raise NotImplementedError

    def cancel_event(self, identifier):
        """
        Schedules a collection of events
        :param identifier: equatable
        :return: None
        """
        raise NotImplementedError
