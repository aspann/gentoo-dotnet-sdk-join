import pathlib
import shutil
import pytest
import os

from gdsj.helpers.symlink_helper import SymlinkHelper
from gdsj.log.logger import Log
from gdsj.models.dotnet_version import DotnetVersion


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0"
])
def test_symlink_against_empty(log_fixture: Log, version_str: str):
    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(full_version=version_str),
        []
    ) is None


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0"
])
def test_symlink_against_dir(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(
            path=test_dotnet_dir,
            major_version=f"{version_str}.100",
            full_version=version_str
        ), [DotnetVersion(
            path=test_dotnet_dir,
            major_version="9999",
            full_version="9999.99"
        )]
    ) is None


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0"
])
def test_symlink_against_invalid(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    # create invalid symlink
    path = pathlib.Path(os.path.join(test_dotnet_dir, "opt/sdk/9999.99"))
    shutil.rmtree(path)
    path.symlink_to("/THISshouldNeverExist_123__")

    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(
            path=test_dotnet_dir,
            major_version=f"{version_str}.100",
            full_version=version_str
        ), [DotnetVersion(
            path=test_dotnet_dir,
            major_version="9999",
            full_version="9999.99"
        )]
    ) is None
