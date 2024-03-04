def dotnet_slug(version_str: str) -> str:
    return "dotnet{}-sdk-bin".format(
        "" if float(version_str) >= 5 else "core"
    )


def dotnet_opt_slug(version_str: str) -> str:
    return "opt/dotnet{}-sdk-bin-{}".format(
        "" if float(version_str) >= 5 else "core",
        version_str
    )
