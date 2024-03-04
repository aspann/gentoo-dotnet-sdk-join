import shutil
import pytest
import os

from gdsj.log.logger import Log
from gdsj.parsers.dev_kit_parser import DevKitParser
from gdsj.parsers.runtime_parser import RuntimeParser
from gdsj.models.cli_args import CliArgs
from utils import dotnet_opt_slug


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_devkit_parser(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir,
        dotnet_opt_slug(version_str)
    )
    parser = DevKitParser(log_fixture, skeleton_sdk_dir, None)
    assert parser.initialized


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_devkit_parser_from_args(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir,
        dotnet_opt_slug(version_str)
    )

    parser = DevKitParser.from_args(log_fixture, CliArgs(
        verbosity="debug",
        log_output=f"{test_dotnet_dir}/test.log",
        log_target="both",
        sdk=skeleton_sdk_dir,
        dest=None,
        version=False,
        runtime_join=False
    ))
    assert parser.initialized


def test_devkit_parser_empty_sdk(log_fixture: Log):
    assert not DevKitParser(log_fixture, None, None).initialized


def test_devkit_parser_empty_major_version(log_fixture: Log):
    assert not DevKitParser(log_fixture, "tmp/non_existent", None).initialized


def test_devkit_parser_cause_exception(log_fixture: Log):
    assert not DevKitParser(
        # needs a non-existent version in a non-existent path
        log_fixture, "tmp/non_existent/123.2", None
    ).initialized


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_devkit_parser_cause_2nd_exception(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir,
        dotnet_opt_slug(version_str)
    )
    # removing the default version subdirs and create an major version inside,
    # which is not allowed by default to trigger the second exception
    shutil.rmtree(os.path.join(skeleton_sdk_dir, "sdk", f"{version_str}.100"))
    os.makedirs(os.path.join(skeleton_sdk_dir, "sdk", f"{version_str}"))
    parser = DevKitParser(log_fixture, skeleton_sdk_dir, None)
    assert not parser.initialized


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_devkit_parser_non_writable(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    non_writable_dir = os.path.join(test_dotnet_dir, "non_writable")
    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir,
        dotnet_opt_slug(version_str)
    )

    # make it non-writable
    os.makedirs(non_writable_dir)
    os.chmod(non_writable_dir, 0o555)

    assert not DevKitParser(
        log_fixture, skeleton_sdk_dir, non_writable_dir
    ).initialized

    # recover write
    os.chmod(non_writable_dir, 0o755)


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_devkit_parser_join(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir,
        dotnet_opt_slug(version_str)
    )
    parser = DevKitParser(log_fixture, skeleton_sdk_dir, None)
    assert parser.initialized
    assert parser.join() is None


def test_devkit_parser_join_error(log_fixture: Log):
    parser = DevKitParser(log_fixture, "tmp/non_existent/123.2", None)
    assert not parser.initialized
    assert parser.join() is None


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_runtime_parser(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir,
        dotnet_opt_slug(version_str)
    )
    dk_parser = DevKitParser(log_fixture, skeleton_sdk_dir, None)
    rt_parser = RuntimeParser(dk_parser)
    assert dk_parser.initialized
    assert rt_parser.initialized
    assert rt_parser.join() is None


def test_runtime_parser_without_parser():
    # setting forcebly an empty devKitParser
    # (this should never happen under normal circumstances)
    parser = RuntimeParser(None)
    parser.parser = None
    assert not parser.initialize()
