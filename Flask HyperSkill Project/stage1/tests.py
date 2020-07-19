from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.flask_test import FlaskTest

from hstest.driver.driver import get_driver

from time import sleep


class FlaskProjectTest(FlaskTest):

    def __init__(self, module_to_test):
        self.time_limit = 3
        super().__init__(module_to_test)

    def generate(self):
        return [TestCase(attach=self.check)]

    def check(self, reply, attach):
        driver = get_driver()
        driver.get('http://127.0.0.1:5000/')
        found_text = driver.find_element_by_tag_name('body').text
        if found_text != 'Hello, world!':
            return CheckResult.wrong("Can't find 'Hello, world!' in the main page!")
        sleep(2)
        return CheckResult.correct()


if __name__ == '__main__':
    FlaskProjectTest('web.main').run_tests()
