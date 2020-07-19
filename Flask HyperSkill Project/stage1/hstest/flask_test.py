from hstest.stage_test import StageTest

import subprocess
import platform
import signal
import os


class FlaskTest(StageTest):
    _kill = os.kill
    process = None

    def run(self):

        os.chdir('web')
        action = 'set' if platform.system() == 'Windows' else 'export'
        os.system(f'{action} FLASK_APP=app')

        if self.process is None:
            self.process = subprocess.Popen([
                'flask', 'run'
            ])

    def after_all_tests(self):
        if self.process is not None:
            try:
                self._kill(self.process.pid, signal.SIGINT)
            except Exception:
                pass
