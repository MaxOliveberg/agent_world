import unittest

from src.agent_world.tests.clock_tests.clock_tests import TestClock
from src.agent_world.tests.currency_tests.currency_tests import TestCurrency
from src.agent_world.tests.currency_tests.wallet_tests import TestWallet
from src.agent_world.tests.scheduler_tests.scheduler_queue_tests import TestSchedulerQueue
from src.agent_world.tests.scheduler_tests.scheduler_tests import TestScheduler
from src.agent_world.tests.statistics_tests.dict_blackboard_tests import TestDictBlackboard


# Todo: Improve test coverage


def load_tests():
    resulting_suite = unittest.TestSuite()
    resulting_suite.addTest(TestSchedulerQueue())
    resulting_suite.addTest(TestScheduler())
    resulting_suite.addTest(TestWallet())
    resulting_suite.addTest(TestClock())
    resulting_suite.addTest(TestDictBlackboard())
    resulting_suite.addTest(TestCurrency())
    return resulting_suite


if __name__ == "__main__":
    suite = load_tests()
    runner = unittest.TextTestRunner()
    runner.run(suite)
