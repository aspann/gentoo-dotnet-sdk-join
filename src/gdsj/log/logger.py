import argparse
import logging
import os
import sys
from ..enums.stdout_mode import StdoutMode
from .log_formatter import LogFormatter


class Log:
    """Logging abstraction"""
    level = logging.NOTSET

    def __init__(self, args: argparse.Namespace):
        """Constructor

        Args:
            args (argparse.Namespace): arguments (provided to main caller)
        """
        log_handlers = []
        self.level = logging.NOTSET
        if isinstance(args.verbosity, str):
            self.level = logging.getLevelName(args.verbosity.upper())

        # checking stdout(mode)
        stdout = StdoutMode.STDOUT
        match args.log_target:
            case "both":
                if self.chk_outfile(args.log_output):
                    stdout = StdoutMode.BOTH
                    log_handlers.append(
                        logging.FileHandler(filename=args.log_output))
            case "file":
                if self.chk_outfile(args.log_output):
                    stdout = StdoutMode.FILE
                    log_handlers.append(
                        logging.FileHandler(filename=args.log_output))

        if self.level > logging.NOTSET:
            if stdout == StdoutMode.STDOUT or stdout == StdoutMode.BOTH or len(log_handlers) == 0:
                sh = logging.StreamHandler(stream=sys.stdout)
                sh.setFormatter(LogFormatter())
                log_handlers.append(sh)

            logging.basicConfig(
                level=self.level,
                format='%(asctime)s %(levelname)s %(message)s',
                handlers=log_handlers
            )

        self.debug("Logger initilaized.")

        """ this hsould be moved to the tests - let it sit here for now
        self.debug("selftestet (debug)")
        self.info("selftestet (info)")
        self.warn("selftestet (warn)")
        self.error("selftestet (error)")
        self.crit("selftestet (crit)")
        self.raw("")
        """

    def chk_outfile(self, filename: str) -> bool:
        dir, filename = os.path.split(os.path.abspath(filename))
        if os.access(dir, os.W_OK) and filename:
            return True
        elif not filename:
            self.error("No file provided!")
        else:  # not found - or not writable
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
        if self.level > logging.NOTSET:
            logging.warn(msg)

    def raw(self, msg: str):
        if self.level > logging.NOTSET:
            logging.log(self.level + 1, msg)  # '+ 1' to hide the timestamp
