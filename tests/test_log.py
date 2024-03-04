import logging
import pytest
import datetime

from logging import LogRecord
from gdsj.log.log_formatter import LogFormatter
from gdsj.log.logger import Log
from gdsj.models.cli_args import CliArgs


@pytest.mark.parametrize("level, entry", [
    (logging.NOTSET, 'TEST'),
    (logging.DEBUG,
     '\x1b[33;90m1970-01-01 00:00:00,000\x1b[0m [\x1b[38;20mDEBUG\x1b[0m]\t   \x1b[33;90mTEST\x1b[0m'),
    (logging.INFO,
     '\x1b[33;90m1970-01-01 00:00:00,000\x1b[0m [\x1b[33;32mINFO\x1b[0m]\t   \x1b[31;37mTEST\x1b[0m'),
    (logging.WARNING,
     '\x1b[33;90m1970-01-01 00:00:00,000\x1b[0m [\x1b[33;20mWARNING\x1b[0m]  \x1b[31;37mTEST\x1b[0m'),
    (logging.ERROR,
     '\x1b[33;90m1970-01-01 00:00:00,000\x1b[0m [\x1b[31;20mERROR\x1b[0m]\t   \x1b[1m\x1b[33;97mTEST\x1b[0m'),
    (logging.CRITICAL,
     '\x1b[33;90m1970-01-01 00:00:00,000\x1b[0m [\x1b[31;1mCRITICAL\x1b[0m] \x1b[31;20mTEST\x1b[0m')
])
def test_log_formatter(level: int, entry: str):
    record = LogRecord(
        args=None,
        func="test_log_formatter",
        lineno=0,
        name="",
        pathname="",
        exc_info="",
        msg="TEST",
        level=level,
    )

    # setting epoch = 0 timestamp (we ned to substract the offset)
    dt_offset = datetime.datetime.now(datetime.UTC).astimezone().utcoffset()
    record.created = dt_offset.total_seconds() * -1  # negate it
    record.msecs = 0

    assert LogFormatter().format(record) == entry


@pytest.mark.parametrize("verbosity, level", [
    ("debug", logging.DEBUG),
    ("info", logging.INFO),
    ("warning", logging.WARNING),
    ("error", logging.ERROR),
    ("critical", logging.CRITICAL)
])
def test_logger_verbosity_parsing(verbosity: str, level: int):
    log = Log(verbosity, "", None)
    assert log.level == level
    log.shutdown()


@pytest.mark.parametrize("method", [
    "raw", "debug", "info", "warning", "warn", "error", "crit"
])
def test_logger_method_exists(log_fixture: Log, method: str):
    assert hasattr(log_fixture, method)

    # call em (stupid, but raises coverage)
    method = getattr(log_fixture, method)
    assert method("test_message") is None


@pytest.mark.parametrize("target", ["test.log"])
def test_logger_chk_outfile_exists(log_fixture: Log, temp_dir: str, target: str):
    assert log_fixture.chk_outfile(f"{temp_dir}/{target}")


@pytest.mark.parametrize("target", ["inexistent/test.log"])
def test_logger_chk_outfile_invalid(log_fixture: Log, temp_dir: str, target: str):
    assert not log_fixture.chk_outfile(f"{temp_dir}/{target}")


@pytest.mark.parametrize("verbosity, level", [
    ("debug", logging.DEBUG),
    ("info", logging.INFO),
    ("warning", logging.WARNING),
    ("error", logging.ERROR),
    ("critical", logging.CRITICAL)
])
def test_logger_from_args(temp_dir: str, verbosity: str, level: int):
    args = CliArgs(
        verbosity=verbosity,
        log_output=f"{temp_dir}/test.log",
        log_target="both",
        sdk="",
        dest=None,
        version=False,
        runtime_join=False
    )
    log = Log.from_args(args)
    assert log.level == level
    log.shutdown()
