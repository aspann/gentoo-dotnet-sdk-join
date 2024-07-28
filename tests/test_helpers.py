import pathlib
import shutil
import pytest
import os

from gdsj.helpers.symlink_helper import SymlinkHelper
from gdsj.helpers.version_helper import VersionHelper
from gdsj.log.logger import Log
from gdsj.models.dotnet_version import DotnetVersion
from utils import dotnet_slug


@pytest.mark.parametrize("version_str,expected", [
    ("2.0", "2.0"),
    ("3.1", "3.1"),
    ("5.0", "5.0"),
    ("6.0", "6.0"),
    ("7.0", "7.0"),
    ("8.0", "8.0"),
    ("9.0", "9.0"),
    ("WORD-8.0.1", "8.0.1"),
    ("AnotherWord8.0", "8.0"),
    ("YwsbWQERASYRTUgxSkE", None)
])
def test_version(version_str: str, expected: str | None):
    parsed = VersionHelper.get_version(version_str)
    assert parsed == expected, \
        f"Mismatch, expected: {expected} - got: {version_str}"


def test_installed_version(test_dotnet_dir: str):
    assert VersionHelper.get_installed_version("", "") is None
    assert VersionHelper.get_installed_version(None, None) is None
    assert VersionHelper.get_installed_version(
        f"{test_dotnet_dir}/opt/sdk/", "9999"
    ) == "9999.99"


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_symlink_group(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    dir = dotnet_slug(version_str)

    # SDK
    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(
            path=f"{test_dotnet_dir}/{dir}-{version_str}/sdk/{version_str}.100",
            major_version=version_str,
            full_version=f"{version_str}.100",
        ),
        [DotnetVersion(
            path=f"{test_dotnet_dir}/opt/sdk/9999.99",
            major_version="9999",
            full_version="9999.99"
        )]
    ) is None

    # non-SDK (RT)
    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(
            path=f"{test_dotnet_dir}/{dir}-{version_str}/sdk/{version_str}.23",
            major_version=version_str,
            full_version=f"{version_str}.23",
        ),
        [DotnetVersion(
            path=f"{test_dotnet_dir}/opt/sdk/9999.99",
            major_version="9999",
            full_version="9999.99"
        )],
        "not_an_sdk"
    ) is None


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_symlink_against_empty(log_fixture: Log, version_str: str):
    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(major_version=version_str),
        []
    ) is None


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_symlink_against_dir(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    dir = dotnet_slug(version_str)
    # create directory (this is the link destination - which should fail)
    os.makedirs(f"{test_dotnet_dir}/opt/sdk/9999.99/sdk/{version_str}.100")
    os.makedirs(f"{test_dotnet_dir}/opt/sdk/9999.99/shared/{version_str}.23")

    # check against sdk
    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(
            path=f"{test_dotnet_dir}/opt/sdk/9999.99",
            major_version="9999",
            full_version="9999.99"
        ),
        [DotnetVersion(
            path=f"{test_dotnet_dir}/{dir}-{version_str}/sdk/{version_str}.100",
            major_version=version_str,
            full_version=f"{version_str}.100"
        )],
    ) is None

    # check agains non-sdk
    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(
            path=f"{test_dotnet_dir}/opt/sdk/9999.99",
            major_version="9999",
            full_version="9999.99"
        ),
        [DotnetVersion(
            path=f"{test_dotnet_dir}/{dir}-{version_str}/shared/{version_str}.23",
            major_version=version_str,
            full_version=f"{version_str}.23"
        )],
        "not_an_sdk"
    ) is None


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_symlink_against_invalid_symlink(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    path = pathlib.Path(
        os.path.join(
            test_dotnet_dir, "opt/sdk/9999.99/sdk", f"{version_str}.100"
        )
    )
    os.makedirs(path)
    shutil.rmtree(path)
    # create invalid symlink
    path.symlink_to(pathlib.Path(
        os.path.join(test_dotnet_dir, "THISshouldNeverExist_123__")
    ))

    dir = dotnet_slug(version_str)

    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(
            path=f"{test_dotnet_dir}/opt/sdk/9999.99",
            major_version="9999",
            full_version="9999.99"
        ), [DotnetVersion(
            path=f"{test_dotnet_dir}/{dir}-{version_str}/sdk/{version_str}.100",
            major_version=version_str,
            full_version=f"{version_str}.100"
        )]
    ) is None


@pytest.mark.parametrize("version_str", [
    "2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"
])
def test_symlink_against_symlink(log_fixture: Log, test_dotnet_dir: str, version_str: str):
    path = pathlib.Path(
        os.path.join(
            test_dotnet_dir, "opt/sdk/9999.99/sdk", f"{version_str}.100"
        )
    )
    os.makedirs(path)
    shutil.rmtree(path)
    # create symlink
    path.symlink_to(pathlib.Path(
        os.path.join(test_dotnet_dir, "/dev/null")
    ))

    dir = dotnet_slug(version_str)

    assert SymlinkHelper.symlink_group(
        log_fixture,
        DotnetVersion(
            path=f"{test_dotnet_dir}/opt/sdk/9999.99",
            major_version="9999",
            full_version="9999.99"
        ), [DotnetVersion(
            path=f"{test_dotnet_dir}/{dir}-{version_str}/sdk/{version_str}.100",
            major_version=version_str,
            full_version=f"{version_str}.100"
        )]
    ) is None
