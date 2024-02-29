import os
import tempfile
import pytest

from gdsj.log.logger import Log


@pytest.fixture()
def temp_dir():
    dirpath = tempfile.mkdtemp()
    yield dirpath


@pytest.fixture()
def log_fixture():
    return Log("debug", "file", "/tmp/gdsj.log")


@pytest.fixture()
def test_dotnet_dir(temp_dir: str):
    target_dir = temp_dir

    # Define the SDK versions to be processed
    sdkVers = ["2.0", "3.1", "5.0", "6.0", "7.0", "8.0"]

    # Iterate through the SDK versions, creating the necessary directories and files for each
    for version in sdkVers:
        base_path = os.path.join(target_dir, 'opt')
        dir = f"dotnet{"" if float(version) >= 5 else "core"}-sdk-bin"
        # Create directories and touch files
        for dir_path in [
            os.path.join(
                base_path,
                f"{dir}-{version}", f"sdk/{version}.100"
            ),
            os.path.join(
                base_path,
                f"{dir}-{version}", f"shared/Microsoft.AspNetCore.App/{version}.100"
            ),
            os.path.join(
                base_path,
                f"{dir}-{version}", f"shared/Microsoft.NETCore.App/{version}.100"
            ),
            # other needed paths
            os.path.join(base_path, "sdk/9999.99/")
        ]:
            os.makedirs(dir_path, exist_ok=True)
            # Create file to keep dir (Actually obsolete)
            open(os.path.join(dir_path, '.keep'), 'w')
    return target_dir
