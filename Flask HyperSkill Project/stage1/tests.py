from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from flasktest.flask_test import FlaskTest

from time import sleep
from driver.driver import get_driver


class FlaskProjectTest(FlaskTest):
    def generate(self):
        return [TestCase(attach=self.check)]

    def check(self, reply, attach):
        driver = get_driver()
        driver.start_client()
        driver.get('http://127.0.0.1:5000/')
        return CheckResult.correct()


if __name__ == '__main__':
    FlaskProjectTest('web.main').run_tests()
