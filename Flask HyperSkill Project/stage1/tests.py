from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase

from driver import get_driver


class FlaskProjectTest(StageTest):
    def generate(self):
        return [TestCase()]

    def check(self, reply, attach):
        driver = get_driver()
        print(driver)
        return CheckResult.wrong()


if __name__ == '__main__':
    FlaskProjectTest('web.main').run_tests()
