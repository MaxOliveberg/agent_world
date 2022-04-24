class IScheduler:
    def current_time(self):
        raise NotImplementedError

    def schedule_event(self, event):
        raise NotImplementedError

    def schedule_events(self, events):
        raise NotImplementedError

    def cancel_event(self, identifier):
        raise NotImplementedError
