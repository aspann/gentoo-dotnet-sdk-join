from . import __version__
from .log.logger import Log
from .parsers.cli_args_parser import CliArgsParser
from .parsers.runtime_parser import RuntimeParser
from .parsers.dev_kit_parser import DevKitParser


def main():
    args = CliArgsParser().parse()  # init and parsing (CLI-)args
    log = Log.from_args(args)                 # init logging (needs above)

    if args.version:
        log.raw(f"v{__version__}")
        return

    # (main) logic start
    log.info(f"Join(src [-s]): '{args.sdk}'")
    log.info(f"Join(dest [-d]): '{args.dest}'")

    sdk_parser = DevKitParser.from_args(log, args)
    sdk_parser.join()

    # almangenate runtimes (within SDK)
    if args.runtime_join:
        RuntimeParser(sdk_parser).join()

    # (main) logic end


if __name__ == "__main__":
    main()
