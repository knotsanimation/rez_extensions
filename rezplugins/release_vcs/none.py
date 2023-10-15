"""
"Passthrough" version control system for rez.
"""
import time

from rez.release_vcs import ReleaseVCS


RevisionType = int


class NoneReleaseVCS(ReleaseVCS):
    """
    A release VCS that does nothing.
    """

    def __init__(self, pkg_root, vcs_root=None):
        super().__init__(pkg_root, vcs_root=vcs_root)
        self.time: RevisionType = int(time.time())

    @classmethod
    def name(cls):
        return "none"

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
        return ""

    def tag_exists(self, tag_name: str) -> bool:
        return False

    def create_release_tag(self, tag_name: str, message: str = None):
        pass


def register_plugin():
    return NoneReleaseVCS
