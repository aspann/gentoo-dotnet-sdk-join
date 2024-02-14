from ..helpers.symlink_helper import SymlinkHelper
from ..parsers.dev_kit_parser import DevKitParser


class RuntimeParser:
    def __init__(self, dev_kit: DevKitParser):
        if not dev_kit or not dev_kit.log:
            return
        dev_kit.log.debug("Initializing RT parser...")
        self.log = dev_kit.log
        self.args = dev_kit.args
        self.dev_kit = dev_kit
        self.initialized = self.initialize()

    def initialize(self) -> bool:
        if not self.dev_kit:
            self.log.error("RT not found!")
            return False

        # find runtimes
        self.log.debug("RT initilized!")
        return True

    def join(self):
        self.log.debug("RT parser joining..")

        # kind augly?
        for sdk in self.dev_kit.sdks:
            if sdk == self.dev_kit.sdk:
                continue

            SymlinkHelper.symlink_group(
                self.log, self.dev_kit.sdk, self.dev_kit.sdks, "shared/Microsoft.AspNetCore.App"
            )
            SymlinkHelper.symlink_group(
                self.log, self.dev_kit.sdk, self.dev_kit.sdks, "shared/Microsoft.NETCore.App"
            )

        self.log.debug("RT parser join-end.")
