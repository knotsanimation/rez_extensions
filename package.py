# -*- coding: utf-8 -*-

name = "rez_extensions"

version = "0.1.0"

variants = []

requires = []

description = "Extend rez features."

authors = ["Liam Collod"]

maintainers = []

uuid = "0f26f7210b3d4ab38713179a39609e10"

build_command = "python {root}/build.py"

private_build_requires = [
    "python-3+",
    "rezbuild_utils",
]


def commands():
    pass


with scope("config") as _config:
    _config.release_packages_path = "N:/skynet/apps/rez/extensions"
