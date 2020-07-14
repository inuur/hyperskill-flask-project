import multiprocessing
import signal
import subprocess
import threading
import sys
import os

from typing import Tuple

from hstest.check_result import CheckResult
from hstest.dynamic.handle import SystemHandler
from hstest.dynamic.handle_stdin import StdinHandler
from hstest.dynamic.handle_stdout import StdoutHandler
from hstest.exceptions import WrongAnswerException, FatalErrorException
from hstest.outcomes import Outcome
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.test_run import TestRun
from hstest.utils import failed, passed


class FlaskTest(StageTest):
    tryout_ports = ['5000', '5001', '5002', '5003', '5004']
    t = None

    def __init__(self, module_to_test: str):
        super().__init__(module_to_test)
        self.t = multiprocessing.Process(target=self.run_flask)

    def run_flask(self):
        print('RUN')
        os.system('python web/main.py')
        pass

    def run(self):
        # RUN FLASK APP
        self.t.start()

    def stop(self):
        # STOP FLASK APP
        pid = self.t.pid
        if self.t is not None:
            try:
                os.kill(pid, signal.SIGINT)
            except ProcessLookupError:
                pass
        self.t.terminate()
        pass

    def _run_test(self, test: TestCase) -> str:
        StdinHandler.set_input_funcs(test.input_funcs)
        StdoutHandler.reset_output()
        TestRun.curr_test_run.error_in_test = None

        self.run()
        self._check_errors(test)

        return StdoutHandler.get_output()

    def run_tests(self, debug=False) -> Tuple[int, str]:
        if debug:
            import hstest.utils as hs
            hs.failed_msg_start = ''
            hs.failed_msg_continue = ''
            hs.success_msg = ''

        curr_test: int = 0
        try:
            SystemHandler.set_up()
            tests = self.generate()
            if len(tests) == 0:
                raise FatalErrorException('No tests provided by "generate" method')

            for test in tests:
                curr_test += 1

                red_bold = '\033[1;31m'
                reset = '\033[0m'
                StdoutHandler.real_stdout.write(
                    red_bold + f'\nStart test {curr_test}' + reset + '\n'
                )

                TestRun.curr_test_run = TestRun(curr_test, test)

                self.create_files(test.files)

                output: str = self._run_test(test)
                result: CheckResult = self._check_solution(test, output)

                self.delete_files(test.files)

                if not result.result:
                    raise WrongAnswerException(result.feedback)

            return passed()

        except BaseException as ex:
            outcome: Outcome = Outcome.get_outcome(ex, self, curr_test)
            fail_text = str(outcome)
            return failed(fail_text)

        finally:
            StageTest.curr_test_run = None
            self.stop()
            self.after_all_tests()
            SystemHandler.tear_down()
