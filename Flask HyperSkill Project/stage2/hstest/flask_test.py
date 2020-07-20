import os
import signal
import subprocess
import sys

from hstest.stage_test import StageTest


class FlaskTest(StageTest):
    _kill = os.kill
    process = None

    def run(self):

        if self.process is None:
            self.process = subprocess.Popen([
                sys.executable, self.file_to_test
            ])

    def after_all_tests(self):
        if self.process is not None:
            try:
                self._kill(self.process.pid, signal.SIGINT)
            except Exception as e:
                pass
