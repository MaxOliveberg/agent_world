import unittest

from src.agent_world.statistics.statistics import initialise_statistics, dispose


class TestStatistics(unittest.TestCase):

    def run_sub_test(self, stat_handler_type):
        # Could be some tasty threading problems stemming from this...
        initialise_statistics(stat_handler_type=stat_handler_type)

        # Todo: Do stuff

        dispose()
        return True

    def test_for_all_types(self):
        configs_to_test = ["max"]
        for config_to_run in configs_to_test:
            self.assertTrue(self.run_sub_test(stat_handler_type=config_to_run), f"Config {config_to_run} failed.")

    def runTest(self):
        self.test_for_all_types()


if __name__ == "__main__":
    unittest.main()
