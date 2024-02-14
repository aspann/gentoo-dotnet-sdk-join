import re


class VersionHelper:
    def get_version(input: str) -> str | None:
        vreg = re.search(r's*([\d.]+)', input or '')
        if not vreg:
            return None
        return vreg.group(vreg.lastindex)
