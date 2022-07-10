
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
import logging
logger = logging.getLogger(__name__)


# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    execute_command_arg = None  # set this variable to a command

    def run(self):
        """Long-running task."""
        try:
            import from_saved_state8
        except Exception:
            logger.info(f"Uncaught backend error: ", exc_info=True)
            raise
        self.finished.emit()  # tell the main thread that we are done

    def run2(self, func, *args, **kwargs):
        """Long-running task."""
        try:
            func(*args, **kwargs)
        except Exception:
            logger.info(f"Uncaught backend error: ", exc_info=True)
            raise
        self.finished.emit()  # tell the main thread that we are done


    def execute_command(self):
        from pokebot.combiner import go_to, talk
        # print(f"Executing: {self.execute_command_arg}")
        try:
            # exec(self.execute_command_arg)
            print(f"Executing: {self.execute_command_arg}")
        except Exception:
            logger.error(f"Uncaught backend error: ", exc_info=True)
        print(f"Command executed")
        self.finished.emit()  # tell the main thread that we are done

