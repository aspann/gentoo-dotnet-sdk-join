from ..helpers.symlink_helper import SymlinkHelper
from ..parsers.dev_kit_parser import DevKitParser


class RuntimeParser:
    def __init__(self, parser: DevKitParser):
        if not parser or not parser.log:
            return
        parser.log.debug("Initializing RT parser...")
        self.log = parser.log
        self.args = parser.args
        self.parser = parser
        self.initialized = self.initialize()

    def initialize(self) -> bool:
        if not self.parser:
            self.log.error("RT not found!")
            return False

        # find runtimes
        self.log.debug("RT initilized!")
        return True

    def join(self):
        self.log.debug("RT parser joining..")

        sdks = [s for s in self.parser.sdks if s != self.parser.sdk]
        for p in ["shared/Microsoft.AspNetCore.App", "shared/Microsoft.NETCore.App"]:
            SymlinkHelper.symlink_group(self.log, self.parser.sdk, sdks, p)

        self.log.debug("RT parser join-end.")
