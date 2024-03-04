import os
import shutil
import tempfile
import pytest

from gdsj.log.logger import Log
from utils import dotnet_slug


@pytest.fixture()
def temp_dir():
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)


@pytest.fixture()
def log_fixture():
    return Log("debug", "file", "/tmp/gdsj.log")


@pytest.fixture()
def test_dotnet_dir(temp_dir: str):
    target_dir = temp_dir

    # Define the SDK versions to be processed
    sdkVers = ["2.0", "3.1", "5.0", "6.0", "7.0", "8.0", "9.0"]

    # Iterate through the SDK versions, creating the necessary directories and files for each
    for version in sdkVers:
        base_path = os.path.join(target_dir, 'opt')
        # Create directories and touch files
        for dir_path in [
            os.path.join(
                base_path,
                f"{dotnet_slug(version)}-{version}",
                f"sdk/{version}.100"
            ),
            os.path.join(
                base_path,
                f"{dotnet_slug(version)}-{version}",
                f"shared/Microsoft.AspNetCore.App/{version}.23"
            ),
            os.path.join(
                base_path,
                f"{dotnet_slug(version)}-{version}",
                f"shared/Microsoft.NETCore.App/{version}.23"
            ),
            # other needed paths
            os.path.join(base_path, "sdk/9999.99/")
        ]:
            os.makedirs(dir_path, exist_ok=True)
    return target_dir
