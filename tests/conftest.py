import os
import tempfile
import shutil
import pytest

from gdsj.log.logger import Log


@pytest.fixture()
def temp_dir():
    dirpath = tempfile.mkdtemp()
    yield dirpath
    # shutil.rmtree(dirpath)


@pytest.fixture()
def log_fixture():
    return Log(
        "debug",
        "file",
        "/tmp/something.log"
    )


@pytest.fixture()
def test_dotnet_dir(temp_dir: str):
    target_dir = temp_dir
    # Print a message indicating the start of the test directory creation script
    # print("running test dir creation script...")

    # Define the SDK versions to be processed
    sdks = ["2.0", "3.1", "5.0", "6.0", "7.0", "8.0"]

    # Clean up any existing data in the specified directory
    opt_dir = os.path.join(target_dir, 'opt')
    if os.path.isdir(opt_dir):
        shutil.rmtree(opt_dir)

    # Iterate through the SDK versions, creating the necessary directories and files for each
    for sdk in sdks:
        base_path = os.path.join(target_dir, 'opt', 'dotnet-sdk-bin')
        if float(sdk) < 5.0:
            base_path = os.path.join(
                target_dir, 'opt', 'dotnetcore-sdk-bin')

        # print(f"creating test-structure for SDK: {sdk}..")

        # Create directories and touch files
        for dir_path in [
            os.path.join(base_path, f"dotnet-sdk-bin-{sdk}", f"sdk/{sdk}.100"),
            os.path.join(
                base_path, f"dotnet-sdk-bin-{sdk}", f"shared/Microsoft.AspNetCore.App/{sdk}.100"),
            os.path.join(
                base_path, f"dotnet-sdk-bin-{sdk}", f"shared/Microsoft.NETCore.App/{sdk}.100")
        ]:
            os.makedirs(dir_path, exist_ok=True)
            # Create file to keep dir
            # Actually obsolete
            open(os.path.join(dir_path, '.keep'), 'w')
    return target_dir
