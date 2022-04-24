class StatisticsHandler:
    def log(self, dictionary):
        raise NotImplementedError

    def read_from(self, file):
        raise NotImplementedError

    def query_keys(self, keys):
        raise NotImplementedError

    def query_values(self, values):
        raise NotImplementedError

    def query_pairs(self, pairs):
        raise NotImplementedError


class WorldDataHandler:

    def set_value(self, identifier, timestamp, value):
        raise NotImplementedError

    def get_value(self, identifier):
        raise NotImplementedError
    # Todo: Historic values
