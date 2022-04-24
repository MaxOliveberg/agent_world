from src.agent_world.statistics.handler.statistics_handler import StatisticsHandler, WorldDataHandler


def _contained(big, small):
    for item in small:
        if item not in big:
            return False
    return True


class MaxStatisticsHandler(StatisticsHandler, WorldDataHandler):
    def set_value(self, identifier, timestamp, value):
        self.log({"name": "Value set", "identifier": identifier, "timestamp": timestamp, "value": value})
        self.__world_data_dict[identifier] = value

    def get_value(self, identifier):
        return self.__world_data_dict[identifier]

    def query_values(self, values):
        return [_dict for _dict in self.__dicts if _contained(list(_dict.values()), values)]

    def query_pairs(self, pairs):
        pass

    def query_keys(self, keys):
        return [_dict for _dict in self.__dicts if _contained(list(_dict.keys()), keys)]

    def __init__(self):
        self.__dicts = []
        self.__world_data_dict = {}

    def read_from(self, file):
        pass

    def log(self, dictionary):
        self.__dicts.append(dictionary)


if __name__ == "__main__":
    max_stat = MaxStatisticsHandler()
    for i in range(10):
        max_stat.log({"name": "Max", "age": i})
        max_stat.log({"name": "Paul", "age": i})
    print(max_stat.query_values(["Max"]))
