from pathlib import Path
from ..log.logger import Log
from ..models.dotnet_version import DotnetVersion


class SymlinkHelper:
    def symlink_group(log: Log, version: DotnetVersion, targets: list[DotnetVersion], segment: str = "sdk"):
        if len(targets) - 1 <= 0:
            log.error(f"Symlik targets for '{segment}' not set!")
            return

        for sdk in [s for s in targets if s.full_version != version.full_version]:
            # iterate through all non-active(current) SDKs
            log.debug(f"Joining {sdk.combined_version}...")
            src = f"{sdk.path}/{segment}/{sdk.full_version}"
            dst = f"{version.path}/{segment}/{sdk.full_version}"
            dst_ul = False  # if {dst} must be removed before linking
            dst_path = Path(dst)

            if dst_path.is_dir() and not dst_path.is_symlink():
                log.warn(f"{dst} is a directory, skipping.")
                continue
            elif dst_path.is_symlink() and not dst_path.exists():
                log.warn(f"{dst} seems to be a broken symlink.")
                dst_ul = True  # force deletion of "{dst}"
                break
            elif dst_path.is_symlink():
                log.warn(f"{dst} already linked, skipping.")
                continue

            try:
                # cleanup
                if dst_ul:
                    dst_path.unlink()
                # linking
                dst_path.symlink_to(Path(src))
                log.debug(f"linked {src} to {dst}")
            except Exception:
                log.error(f"could not link '{src}' to '{dst}'")
