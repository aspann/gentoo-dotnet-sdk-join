import argparse
import os

from pathlib import Path

from ..helpers.symlink_helper import SymlinkHelper
from ..helpers.version_helper import VersionHelper
from ..log.logger import Log
from ..models.dotnet_version import DotnetVersion


class DevKitParser:
    def __init__(self, log: Log, args: argparse.Namespace):
        log.debug("Initializing SDK parser...")
        self.log = log
        # initializing other vars
        self.args = args
        self.sdk = DotnetVersion()
        self.sdks = []
        self.initialized = self.initialize()

    def initialize(self) -> bool:
        # find installed dotnet SDKs
        if not self.args.sdk:
            self.log.error("Dotnet SDK path not set")
            return False
        if not self.args.dest:
            self.args.dest = self.args.sdk
        elif not os.access(self.args.dest, os.W_OK):
            self.log.error(f"Failed to open dotnet SDK diretory: '{self.args.dest}' (write)")  # noqa
            return False

        dir, subdir = os.path.split(os.path.abspath(self.args.sdk))
        self.sdk.path = f"{dir}/{subdir}"
        self.log.debug(f"Current dotnet SDK location: {self.sdk.path}")  # noqa
        # for 100%-completeness we need to check the above vars as well ..

        # get version
        self.sdk.major_version = VersionHelper.get_version(subdir)
        if not self.sdk.major_version:
            self.log.error(f"Failed to aquire dotnet SDK version for '{subdir}'")  # noqa
            return False

        try:
            avail_versions = sorted([
                s for s in next(os.walk(f"{self.sdk.path}/sdk", followlinks=False))[1] if s.startswith(self.sdk.major_version)
            ])
            self.sdk.full_version = avail_versions[len(avail_versions)-1]
            self.log.debug(f"Current dotnet SDK version: {self.sdk.get_combined_version()}")  # noqa
        except Exception:
            self.log.error(f"Failed to aquire full dotnet SDK version for '{subdir}'")  # noqa
            return False

        # get current subversion
        for sdk_path in sorted(list(Path(dir).glob(subdir.replace(self.sdk.major_version, "*")))):
            if len(sdk_path.parts) <= 0:
                continue
            sdk_path_version = VersionHelper.get_version(sdk_path.parts[len(sdk_path.parts) - 1])  # noqa
            sdk_path_versions = sorted([
                s for s in next(os.walk(f"{sdk_path}/sdk", followlinks=False))[1] if s.startswith(sdk_path_version)
            ])
            if len(sdk_path_versions) <= 0:
                continue
            sdk = DotnetVersion(
                path=sdk_path,
                major_version=sdk_path_version,
                full_version=sdk_path_versions[len(sdk_path_versions)-1],
                active=sdk_path_versions[len(sdk_path_versions)-1] == self.sdk.full_version  # noqa
            )

            self.log.debug(f"Found dotnet SDK: '{sdk.path}' ({sdk.get_combined_version()}) active: {sdk.active}")  # noqa
            self.sdks.append(sdk)
        # todo: what if more then one active sdk in the slot? (can that ever happen?)

        # all set
        return True

    def join(self):
        self.log.debug("Joining SDKs (join_sdk)..")
        if not self.initialized:
            self.log.error("Failed to find any usable dotnet SDK")
            return

        SymlinkHelper.symlink_group(self.log, self.sdk, self.sdks)

        self.log.debug("SDK parser join-end.")
