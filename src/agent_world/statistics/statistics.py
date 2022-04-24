from src.agent_world.statistics.handler.max_statistics_handler import MaxStatisticsHandler
from src.agent_world.statistics.handler.statistics_handler import StatisticsHandler, WorldDataHandler


class StatisticsWrapper(StatisticsHandler, WorldDataHandler):

    def set_value(self, identifier, timestamp, value):
        if self.__data_handler:
            return self.__data_handler.set_value(identifier, timestamp, value)

    def get_value(self, identifier):
        if self.__data_handler:
            return self.__data_handler.get_value(identifier)

    def __init__(self):
        self.__stat_handler = None
        self.__data_handler = None

    def configure(self, stat_handler: StatisticsHandler, data_handler: WorldDataHandler):
        self.__stat_handler = stat_handler
        self.__data_handler = data_handler

    def log(self, dictionary):
        if self.__stat_handler:
            return self.__stat_handler.log(dictionary)

    def read_from(self, file):
        if self.__stat_handler:
            return self.__stat_handler.read_from(file)

    def query_keys(self, keys):
        if self.__stat_handler:
            return self.__stat_handler.query_keys(keys)

    def query_values(self, values):
        if self.__stat_handler:
            return self.__stat_handler.query_values(values)

    def query_pairs(self, pairs):
        if self.__stat_handler:
            return self.__stat_handler.query_pairs(pairs)


statistics_manager = StatisticsWrapper()


def initialise_statistics(stat_handler_type="max"):
    global statistics_manager
    if stat_handler_type == "max":
        new_handler = MaxStatisticsHandler()
        statistics_manager.configure(new_handler, new_handler)
