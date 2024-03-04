import os
import re

from glob import iglob


class VersionHelper:
    @staticmethod
    def get_version(input: str) -> str | None:
        vreg = re.search(r's*([\d.]+)', input or '')
        if not vreg:
            return None
        return vreg.group(vreg.lastindex)

    @staticmethod
    def get_installed_version(in_dir: str, version: str) -> str | None:
        dirs = [d for d in iglob(f"{in_dir}/{version}.*") if os.path.isdir(d)]  # noqa
        if dirs and len(dirs) == 1:
            return os.path.basename(os.path.normpath(dirs[0]))
        return None
