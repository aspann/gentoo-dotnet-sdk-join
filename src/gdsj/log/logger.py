import logging
import os
import sys

from ..models.cli_args import CliArgs
from ..enums.stdout_mode import StdoutMode
from .log_formatter import LogFormatter


class Log:
    """Logging abstraction"""
    level = logging.NOTSET
    handlers = []

    def __init__(self, verbosity: str, log_target: str, log_output: str | None):
        """Constructor

        Args:
            args (argparse.Namespace): arguments (provided to main caller)
        """
        self.level = logging.NOTSET
        if isinstance(verbosity, str):
            self.level = logging.getLevelName(verbosity.upper())

        # checking stdout(mode)
        stdout = StdoutMode.STDOUT
        match log_target:
            case "both":
                if self.chk_outfile(log_output):
                    stdout = StdoutMode.BOTH
                    self.handlers.append(
                        logging.FileHandler(filename=log_output)
                    )
            case "file":
                if self.chk_outfile(log_output):
                    stdout = StdoutMode.FILE
                    self.handlers.append(
                        logging.FileHandler(filename=log_output)
                    )

        if self.level > logging.NOTSET:
            if stdout == StdoutMode.STDOUT or stdout == StdoutMode.BOTH or len(self.handlers) == 0:
                sh = logging.StreamHandler(stream=sys.stdout)
                sh.setFormatter(LogFormatter())
                self.handlers.append(sh)

            logging.basicConfig(
                level=self.level,
                format='%(asctime)s %(levelname)s %(message)s',
                handlers=self.handlers
            )

        self.debug("Logger initilaized.")

        """ this should be moved to the tests - let it sit here for now
        self.debug("selftestet (debug)")
        self.info("selftestet (info)")
        self.warning("selftestet (warn)")
        self.error("selftestet (error)")
        self.crit("selftestet (crit)")
        self.raw("")
        """

    @classmethod
    def from_args(cls, args: CliArgs):
        """Alternative constructor

        Args:
            args (argparse.Namespace): arguments (provided to main caller)
        """
        return cls(
            args.verbosity,
            args.log_target,
            args.log_output
        )

    def chk_outfile(self, filename: str) -> bool:
        dir, filename = os.path.split(os.path.abspath(filename))
        if os.access(dir, os.W_OK) and filename:
            return True

        self.error("Path not writable or inexistent!")
        return False

    def crit(self, msg: str):
        if self.level > logging.NOTSET:
            logging.critical(msg)

    def error(self, msg: str):
        if self.level > logging.NOTSET:
            logging.error(msg)

    def debug(self, msg: str):
        if self.level > logging.NOTSET:
            logging.debug(msg)

    def info(self, msg: str):
        if self.level > logging.NOTSET:
            logging.info(msg)

    def warn(self, msg: str):
        self.warning(msg)

    def warning(self, msg: str):
        if self.level > logging.NOTSET:
            logging.warning(msg)

    def raw(self, msg: str):
        if self.level > logging.NOTSET:
            logging.log(self.level + 1, msg)  # '+ 1' to hide the timestamp

    def shutdown(self):
        for handler in self.handlers:
            handler.close()
        logging.shutdown()
        self.handlers = []  # empty handlers

    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown()
