#
# -*- coding: utf-8 -*-
#

from os_platform import OsPlatform


class PyPackage:
    def __init__(self, name: str, version_installed: str, summary: str,
                 requires: [str], required_by: [str]):
        level = 1 if requires is None or len(requires) < 1 else (-1)
        self.name = name
        self.version_installed = [version_installed]
        self.version_latest = ''
        self.versions_recent = ['0.0']  # see: https://github.com/wimglenn/johnnydep/blob/master/johnnydep/pipper.py
        self.level = level
        self.locked = False
        self.summary = summary
        self.requires = requires
        self.required_by = required_by
        return

    def get_name(self) -> str:
        return self.name

    def get_version_installed(self, platform_id=OsPlatform.ANY) -> str:
        # get the default, or the 'own' one, unless specified otherwise
        # fix/add logic later
        return self.version_installed[OsPlatform.ANY]

    def get_version_latest(self) -> str:
        return self.version_latest

    def get_versions_recent(self) -> [str]:
        # need to store before - only keep most recent 5 or so, excluding pre0, post2, nightly ...
        return self.versions_recent

    def get_level(self) -> int:
        return self.level

    def get_summary(self) -> str:
        return self.summary

    def get_requires(self) -> [str]:
        return self.requires

    def get_required_by(self) -> [str]:
        return self.required_by
