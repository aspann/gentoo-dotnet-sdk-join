import pytest
import os

from gdsj.parsers.dev_kit_parser import DevKitParser
from gdsj.parsers.runtime_parser import RuntimeParser
from gdsj.models.cli_args import CliArgs
from gdsj.helpers.version_helper import VersionHelper
from gdsj.log.logger import Log
from gdsj.models.dotnet_version import DotnetVersion

"""
tbd ...
"""


@pytest.mark.parametrize("major,full,combined", [
    ("5", "5.0.0", "5/5.0.0"),
    ("3", "3.0.0", "3/3.0.0"),
    ("6", "6.1.3", "6/6.1.3")
])
def test_dotnet_version(major: str, full: str, combined: str):
    version = DotnetVersion(
        path=None,
        major_version=major,
        full_version=full,
    )
    assert version.combined_version == combined


def test_cliargs():
    args = CliArgs(
        sdk="4.2",
        dest="/tmp/bla",
        version=True,
        verbosity="123",
        log_target="abc",
        log_output="file",
        runtime_join=True
    )
    assert args.sdk == "4.2"
    assert args.dest == "/tmp/bla"
    assert args.version is True
    assert args.verbosity == "123"
    assert args.log_target == "abc"
    assert args.log_output == "file"
    assert args.runtime_join is True


@pytest.mark.parametrize("version_str,expected", [
    ("FURZ-2.0", "2.0"),
    ("schniggedings-3.1", "3.1"),
    ("5.0", "5.0"),
    ("6.0", "6.0"),
    ("7.0", "7.0"),
    ("8.0", "8.0"),
    ("asdfasdfwerf-8.0.1", "8.0.1"),
    ("aasdfasdfasdf8.0", "8.0"),
    ("LULU", None)
])
def test_version(version_str: str, expected: str | None):
    parsed = VersionHelper.get_version(version_str)
    assert parsed == expected, \
        f"Mismatch, expected: {expected} - got: {version_str}"


def test_devkitparser(log_fixture: Log, test_dotnet_dir: str):

    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir, "opt/dotnet-sdk-bin/dotnet-sdk-bin-6.0")
    parser = DevKitParser(log_fixture, skeleton_sdk_dir, None)
    assert parser.initialized


def test_runtime_parser(log_fixture: Log, test_dotnet_dir: str, temp_dir: str):
    # Directory with correctly named subdir structure
    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir, "opt/dotnet-sdk-bin/dotnet-sdk-bin-6.0")
    print(skeleton_sdk_dir)
    dk_parser = DevKitParser(log_fixture, skeleton_sdk_dir, None)
    rt_parser = RuntimeParser(dk_parser)
    assert dk_parser.initialized
    assert rt_parser.initialized
