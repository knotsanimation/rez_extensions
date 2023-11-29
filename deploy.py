import getpass
import json
import logging
import os
import shutil
import datetime
import sys
from pathlib import Path

from pythonning.filesystem import set_path_read_only
from pythonning.git import get_current_commit_hash


LOGGER = logging.getLogger(__name__)

THISDIR = Path(__file__).parent

CONTENT_SRC_PATHS = [
    THISDIR / "include",
    THISDIR / "rezplugins",
]

KNOTS_SKYNET_PATH = Path(os.environ["KNOTS_SKYNET_PATH"]).resolve()
assert KNOTS_SKYNET_PATH.exists()

EXTENSION_DST_PATH = KNOTS_SKYNET_PATH / "apps" / "rez" / "extensions"
assert EXTENSION_DST_PATH.exists()


def create_deploy_info(info_path: Path):
    info_content = {
        "deployed": str(datetime.datetime.utcnow()),
        "user": getpass.getuser(),
        "commit": get_current_commit_hash(),
    }
    with open(info_path, "w+") as info_file:
        json.dump(info_content, info_file, indent=4, sort_keys=True)


def deploy_content(content_src_path: Path, target_dir: Path):
    content_dst_path = target_dir / content_src_path.name
    LOGGER.debug(f"copying {content_src_path} to {content_dst_path}")
    # overwrite if exists
    if content_src_path.is_file():
        shutil.copy2(content_src_path, content_dst_path)
    else:
        shutil.copytree(
            content_src_path,
            content_dst_path,
            dirs_exist_ok=True,
        )

    LOGGER.debug(f"setting dst content to read-only")
    set_path_read_only(content_dst_path)


def main():
    info_path = EXTENSION_DST_PATH / "DEPLOY.info"
    LOGGER.info(f"writting {info_path}")
    create_deploy_info(info_path)

    for content_src_path in CONTENT_SRC_PATHS:
        LOGGER.info(f"deploying <{content_src_path}>")
        deploy_content(content_src_path, EXTENSION_DST_PATH)

    LOGGER.info("finished")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="{levelname: <7} | {asctime} [{name}] {message}",
        style="{",
        stream=sys.stdout,
    )
    main()
