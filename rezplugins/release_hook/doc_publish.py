from typing import Optional

import rez.packages
import rez.resolved_context
from rez.release_hook import ReleaseHook


class DocPublishHook(ReleaseHook):
    """
    A release hook that allow to build and deploy the documentation of the package.
    """

    # default values
    _doc_command_attr = "doc_publish_command"
    _doc_require_attr = "doc_publish_requires"

    # settings that can be configured in the rez config
    schema_dict = {
        "publish_command_attr_name": str,
        "publish_require_attr_name": str,
    }

    @classmethod
    def name(cls) -> str:
        return "doc_publish"

    @property
    def doc_command_attr(self) -> str:
        if self.settings.publish_command_attr_name:
            return self.settings.publish_command_attr_name
        return self._doc_command_attr

    @property
    def doc_require_attr(self) -> str:
        if self.settings.publish_require_attr_name:
            return self.settings.publish_require_attr_name
        return self._doc_require_attr

    def post_release(
        self,
        user: str,
        install_path: str,
        variants: Optional[list[rez.packages.Variant]] = None,
        release_message=None,
        changelog=None,
        previous_version=None,
        **kwargs,
    ):
        if not variants:
            # no package were released
            return

        if self.doc_command_attr not in self.package.arbitrary_keys():
            # doesn't define a way to build doc
            return

        doc_command = getattr(self.package, self.doc_command_attr)
        if not isinstance(doc_command, str):
            raise ValueError(
                f"{self.doc_command_attr} attribute must be a string, got <{doc_command}>."
            )

        doc_command = self.package.format(doc_command)

        doc_require = [self.package.as_exact_requirement()]

        if self.doc_require_attr in self.package.arbitrary_keys():
            user_doc_require = getattr(self.package, self.doc_require_attr)
            if not isinstance(user_doc_require, list):
                raise ValueError(
                    f"{self.doc_require_attr} attribute must be a list[str], got <{user_doc_require}>."
                )
            doc_require += user_doc_require

        print(f"resolving env {doc_require} ...")
        context = rez.resolved_context.ResolvedContext(doc_require)
        cwd = self.package.root
        print(f"calling doc publish command <{doc_command}> with cwd={cwd} ...")
        context.execute_shell(command=doc_command, cwd=cwd, block=True)


def register_plugin():
    return DocPublishHook
