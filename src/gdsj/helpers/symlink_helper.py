from pathlib import Path
from ..log.logger import Log
from ..models.dotnet_version import DotnetVersion
from ..helpers.version_helper import VersionHelper


class SymlinkHelper:
    def symlink_group(log: Log, version: DotnetVersion, targets: list[DotnetVersion], segment: str = "sdk"):
        if len(targets) <= 0:
            log.error(f"Symlik targets for '{segment}' not set!")
            return

        for sdk in [s for s in targets if float(s.major_version) < float(version.major_version)]:
            # iterate through all non-active(current) SDKs
            log.info(
                "Joining {} ({})...".format(
                    sdk.combined_version, segment.replace("shared/", "")
                )
            )
            src = f"{sdk.path}/{segment}/{sdk.full_version}"
            dst = f"{version.path}/{segment}/{sdk.full_version}"

            # if segment isn't sdk we're surely linking RT
            if segment != "sdk":
                inst_ver = VersionHelper.get_installed_version(
                    f"{sdk.path}/{segment}",
                    sdk.major_version
                )
                if inst_ver:
                    src = f"{sdk.path}/{segment}/{inst_ver}"
                    dst = f"{version.path}/{segment}/{inst_ver}"
                else:
                    log.warn("could not find any installed version, skipping.")
                    continue

            dst_ul = False  # if {dst} must be removed before linking
            dst_path = Path(dst)

            if dst_path.is_dir() and not dst_path.is_symlink():
                log.warn(f"{dst} is a directory, skipping.")
                continue
            elif dst_path.is_symlink() and not dst_path.exists():
                log.warn(f"{dst} seems to be a broken symlink.")
                dst_ul = True  # force deletion of "{dst}"
            elif dst_path.is_symlink():
                log.warn(f"{dst} already linked, skipping.")
                continue

            # cleanup
            if dst_ul:
                dst_path.unlink()
            # linking
            dst_path.symlink_to(Path(src))
            log.debug(f"linked {src} to {dst}")
