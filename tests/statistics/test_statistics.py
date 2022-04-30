import pytest

from src.agent_world.statistics.statistics import initialise_statistics, dispose


def run_sub_test(stat_handler_type):
    # Could be some tasty threading problems stemming from this...
    initialise_statistics(stat_handler_type=stat_handler_type)

    # Todo: Do stuff

    dispose()
    return True


def test_for_all_types():
    configs_to_test = ["max"]
    for config_to_run in configs_to_test:
        assert run_sub_test(stat_handler_type=config_to_run)
