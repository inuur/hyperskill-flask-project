from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
from selenium import webdriver

import os
import platform


class DriverDetector:
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MAC = 'Darwin'  # ??

    @staticmethod
    def get_driver():
        system = platform.system()
        if system == DriverDetector.WINDOWS:
            return DriverDetector.get_windows_driver()
        if system == DriverDetector.LINUX:
            return DriverDetector.get_linux_driver()
        if system == DriverDetector.MAC:
            return DriverDetector.get_mac_driver()
        raise Exception("Can't detect OS name")

    @staticmethod
    def get_windows_driver():
        pass

    @staticmethod
    def get_mac_driver():
        pass

    @staticmethod
    def get_linux_driver():
        pass


class TicTacToeTest(StageTest):
    def generate(self):
        return [TestCase()]

    def check(self, reply, attach):
        system = platform.system()
        if system == 'Windows':
            print('this is windows!')
        return CheckResult.correct()

    @staticmethod
    def get_driver():
        system = platform.system()
        if system == 'Windows':
            print('this is windows!')


if __name__ == '__main__':
    TicTacToeTest('web.main').run_tests()
