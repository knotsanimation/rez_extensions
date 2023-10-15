"""
Minimal version control system for rez that is actually not one.
"""
import time
from pathlib import Path

from rez.release_vcs import ReleaseVCS
from rez.utils.logging_ import print_info


RevisionType = int


class SimpleReleaseVCS(ReleaseVCS):
    """
    A release VCS that doesn't really do anything.

    It still writes every release in a CHANGELOG.md file that is optional.
    """

    def __init__(self, pkg_root, vcs_root=None):
        super().__init__(pkg_root, vcs_root=vcs_root)
        self.time: RevisionType = int(time.time())

    @property
    def changelog_path(self) -> Path:
        return Path(self.vcs_root) / "CHANGELOG.md"

    @classmethod
    def name(cls):
        return "simple"

    @classmethod
    def is_valid_root(cls, path):
        return True

    @classmethod
    def search_parents_for_root(cls):
        return False

    def validate_repostate(self):
        pass

    def get_current_revision(self) -> RevisionType:
        return self.time

    def get_changelog(
        self,
        previous_revision: RevisionType = None,
        max_revisions: int = None,
    ) -> str:
        """
        Used in the ``changelog`` attribute of the ``package.py``
        """
        return f"See {self.changelog_path.name}"

    def tag_exists(self, tag_name: str) -> bool:
        changelog = self._read_changelog()
        return any(
            [
                tag_name == metadata["release"]
                for metadata in changelog.values()
            ]
        )

    def create_release_tag(self, tag_name: str, message: str = None):
        message = message or "No change notes provided."
        changelog = self._read_changelog()
        revision = str(self.get_current_revision())
        changelog[revision] = {
            "release": tag_name,
            "message": message.split("\n"),
        }
        self._write_changelog(changelog)

    def _read_changelog(self) -> dict[str, dict[str, str]]:
        """
        Deconstruct the changelog in a dict of metadata.

        A changelog looks like::

            # version.number: revision

            some user abitrary message

            # version.number: revision

            ...
        """
        if not self.changelog_path.exists():
            return {}

        content = self.changelog_path.read_text(encoding="utf-8")
        content = content.split("\n")
        content_dict = {}
        revision = None
        for line in content:
            if line.startswith("#") and not line.startswith("##"):
                # rsplit as safety for release that could contain ":"
                line = line.lstrip("#").lstrip(" ").rsplit(":", 1)
                release = line[0].strip(" ")
                revision = line[1].strip(" ")
                content_dict[revision] = {"release": release, "message": []}
                continue
            if revision:
                content_dict[revision]["message"].append(line)
        return content_dict

    def _write_changelog(self, new_content: dict[str, dict[str, str]]):
        new_text = ""
        for revision, metadata in new_content.items():
            message = "\n".join(metadata["message"])
            new_text += f"# {metadata['release']}: {revision}\n\n{message}\n"

        if not self.changelog_path.exists():
            print_info(f"creating {self.changelog_path}")
            self.changelog_path.touch()

        self.changelog_path.write_text(new_text, encoding="utf-8")


def register_plugin():
    return SimpleReleaseVCS
