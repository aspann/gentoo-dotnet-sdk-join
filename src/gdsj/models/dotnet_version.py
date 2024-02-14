from dataclasses import dataclass


@dataclass
class DotnetVersion:
    path: str | None = None,
    major_version: str | None = None,
    full_version: str | None = None,
    active: bool = False

    def get_combined_version(self) -> str:
        return f"{self.major_version}/{self.full_version}"
