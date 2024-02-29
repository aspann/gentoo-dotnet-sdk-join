import pytest
import os

from gdsj.log.logger import Log
from gdsj.parsers.dev_kit_parser import DevKitParser
from gdsj.parsers.runtime_parser import RuntimeParser


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0"
])
def test_devkitparser(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir, f"opt/dotnet{"" if float(version_str) >= 5 else "core"}-sdk-bin-{version_str}")
    parser = DevKitParser(log_fixture, skeleton_sdk_dir, None)
    assert parser.initialized


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0"
])
def test_runtime_parser(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    skeleton_sdk_dir = os.path.join(
        test_dotnet_dir, f"opt/dotnet{"" if float(version_str) >= 5 else "core"}-sdk-bin-{version_str}")
    dk_parser = DevKitParser(log_fixture, skeleton_sdk_dir, None)
    rt_parser = RuntimeParser(dk_parser)
    assert dk_parser.initialized
    assert rt_parser.initialized
