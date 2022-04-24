import unittest

from src.agent_world.statistics.handler.dict_blackboard import DictBlackboard


class TestDictBlackboard(unittest.TestCase):
    def test_setting_and_getting(self):
        blackboard = DictBlackboard()
        blackboard.set_value("test", 0, 0)
        data = blackboard.get_value("test")
        self.assertEqual(0, data.timestamp, "Timestamp not correct")
        self.assertEqual(0, data.value, "Value not correct")

    def runTest(self):
        self.test_setting_and_getting()
