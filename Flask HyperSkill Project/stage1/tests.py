from time import sleep

from hstest.check_result import CheckResult
from hstest.flask_test import FlaskTest
from hstest.test_case import TestCase
from hstest.driver.driver import get_driver

temp = None
driver = None


class FlaskProjectTest(FlaskTest):

    def __init__(self, module_to_test):
        super().__init__(module_to_test)

    def generate(self):
        return [TestCase(attach=self.test_main_page)]

    @staticmethod
    def test_main_page():
        global driver
        driver = get_driver()
        driver.get('http://127.0.0.1:5000/')
        found_text = driver.find_element_by_tag_name('body').text
        driver.close()
        if found_text != 'Hello, world!':
            return CheckResult.wrong("Can't find 'Hello, world!' in the main page!")
        return CheckResult.correct()

    def check(self, reply, attach):
        return attach()


if __name__ == '__main__':
    FlaskProjectTest('web.app').run_tests()
