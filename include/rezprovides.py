import os
from typing import Callable

REZ_PROVIDES_VAR = "REZ_PROVIDES"


def is_provided(
    package_name: str,
    env: dict,
    defined: Callable[[str], bool],
) -> list[str]:
    """
    Return a list if the given package is already provided by another package.

    This is determined by examining the environment variables, where the other
    package must define special variables specifying it already provides X packages.

    Args:
        package_name: usually this.name
        env: usually rez builtin env object from the command function
        defined: the ``defined`` function of the source package.py scope

    Returns:
        set of rez packages names that provided the given rez package.
        empty if not provided.
    """
    if not defined(REZ_PROVIDES_VAR):
        return []

    provided_packages = str(env[REZ_PROVIDES_VAR]).split(os.pathsep)
    this_provided = [
        package
        for package in provided_packages
        if package.split("-")[0] == package_name
    ]

    return list({package.split("-", 1)[1] for package in this_provided})
