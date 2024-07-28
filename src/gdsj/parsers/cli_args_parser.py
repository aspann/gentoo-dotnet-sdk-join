import argparse
import os

from ..models.cli_args import CliArgs


class CliArgsParser:
    def __init__(self, parser: argparse.ArgumentParser = None):
        self.parser = parser
        if parser is None:
            # default initialization (empty parser with default module name)
            self.parser = argparse.ArgumentParser("gentoo-dotnet-sdk-join")

    def parse(self) -> CliArgs:
        self.parser.add_argument(
            "-s", "--sdk",
            help="dotnet SDK source(root) path, default: $DOTNET_ROOT",
            default=os.environ["DOTNET_ROOT"]
        )
        self.parser.add_argument(
            "-d", "--dest",
            help="dotnet SDK destination path, default: $DOTNET_ROOT",
            default=None
        )
        self.parser.add_argument(
            "-rt", "--runtime-join",
            help="runtime join, default: enabled",
            default=True,
            action="store_true"
        )
        """application wide options like version, logging, etc."""
        self.parser.add_argument(
            "-V", "--version",
            help="shows the current version",
            default=None,
            action="store_true"
        )
        self.parser.add_argument(
            "-v", "--verbosity",
            help="loglevel, default: info",
            choices=["debug", "info", "warning", "error", "critical", ],
            default="info"
        )
        self.parser.add_argument(
            "-lt", "--log-target",
            help="log target, default: stdout",
            choices=["stdout", "file", "both"],
            default="stdout"
        )
        self.parser.add_argument(
            "-lo", "--log-output",
            help="log output(must be set if -t [file|both]), default: unset",
            default=None
        )

        res = self.parser.parse_args()
        # if unset, copy over from sdk (must be the same, then)
        if not res.dest:
            res.dest = res.sdk

        # unpack namespace into keyworded arguments to feed dataclass
        return CliArgs(**vars(res))
