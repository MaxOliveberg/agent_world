import pytest

from src.agent_world.statistics.handler.dict_blackboard import DictBlackboard


def test_setting_and_getting():
    blackboard = DictBlackboard()
    blackboard.set_value("test", 0, 0)
    data = blackboard.get_value("test")
    assert 0 == data.timestamp
    assert 0 == data.value
