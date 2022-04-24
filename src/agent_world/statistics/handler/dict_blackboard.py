from dataclasses import dataclass

from src.agent_world.statistics.handler.statistics_handler import Blackboard


@dataclass
class TimedValue:
    timestamp: int
    value: any


class DictBlackboard(Blackboard):

    def __init__(self):
        self.__dict = {}

    def set_value(self, identifier, timestamp, value):
        self.__dict[identifier] = TimedValue(timestamp=timestamp, value=value)

    def get_value(self, identifier):
        return self.__dict[identifier]
