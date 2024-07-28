import logging


class LogFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG:
            "\x1b[33;90m%(asctime)s\x1b[0m [\x1b[38;20m%(levelname)s\x1b[0m]\t   \x1b[33;90m%(message)s\x1b[0m",         # noqa
        logging.INFO:
            "\x1b[33;90m%(asctime)s\x1b[0m [\x1b[33;32m%(levelname)s\x1b[0m]\t   \x1b[31;37m%(message)s\x1b[0m",         # noqa
        logging.WARNING:
            "\x1b[33;90m%(asctime)s\x1b[0m [\x1b[33;20m%(levelname)s\x1b[0m]  \x1b[31;37m%(message)s\x1b[0m",            # noqa
        logging.ERROR:
            "\x1b[33;90m%(asctime)s\x1b[0m [\x1b[31;20m%(levelname)s\x1b[0m]\t   \033[1m\x1b[33;97m%(message)s\x1b[0m",  # noqa
        logging.CRITICAL:
            "\x1b[33;90m%(asctime)s\x1b[0m [\x1b[31;1m%(levelname)s\x1b[0m] \x1b[31;20m%(message)s\x1b[0m",              # noqa
    }

    def format(self, record: logging.LogRecord) -> str:
        """formats log output

        Args:
            record (LogRecord): record(message) to format

        Returns:
            str: formatted string
        """
        format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(format)
        return formatter.format(record)
