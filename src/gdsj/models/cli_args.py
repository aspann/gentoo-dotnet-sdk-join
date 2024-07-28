from dataclasses import dataclass


@dataclass
class CliArgs:
    sdk: str
    dest: str | None
    version: bool
    verbosity: str
    log_target: str
    log_output: str | None
    runtime_join: bool
