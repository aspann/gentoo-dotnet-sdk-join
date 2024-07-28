import pytest

from gdsj.models.cli_args import CliArgs
from gdsj.models.dotnet_version import DotnetVersion


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
        dest="/tmp/test",
        version=True,
        verbosity="123",
        log_target="abc",
        log_output="file",
        runtime_join=True
    )
    assert args.sdk == "4.2"
    assert args.dest == "/tmp/test"
    assert args.version is True
    assert args.verbosity == "123"
    assert args.log_target == "abc"
    assert args.log_output == "file"
    assert args.runtime_join is True
