#
# -*- coding: utf-8 -*-
#
import json

from os_platform import OsPlatform


class Constraints:
    def __init__(self, package: str, requires: str):
        self.package = package
        self.requires = requires
        return


class Locked:
    def __init__(self):
        self.checked_time = 0  # int(time.time())
        self.constraints = [Constraints('tensorflow', '<1.19'),
                            Constraints('whatever', '>= 1.18')]
        return


class PyPackage:
    def __init__(self, name: str, version_installed: str, summary: str,
                 requires: [str], required_by: [str]):
        # base information coming from 'pip list P0 P1 .. Pn'
        # set this via: pip list, pip show
        self.name = name
        self.version_installed = [version_installed]  # only set the 0'th entry (any)
        self.summary = summary
        self.requires = requires
        self.required_by = required_by

        # only use if, needed
        self.locked = Locked()

        #
        # set this, if needed before update
        #
        # level generally needs to be calculated
        level = 1 if requires is None or len(requires) < 1 else (-1)
        self.level = level
        # the latest N available versions
        self.versions_recent = ['0.0']  # see PyPiCmd.get_latest
        self.versions_checked_time = 0  # int(time.time())

    def get_json(self) -> str:
        # returns recursively resolved json string
        j = json.loads(json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o))))
        return json.dumps(j, indent=1)

    def get_name(self) -> str:
        return self.name

    def get_version_installed(self, platform_id=OsPlatform.ANY) -> str:
        # get the default, or the 'own' one, unless specified otherwise
        # fix/add logic later
        return self.version_installed[OsPlatform.ANY]

    def get_versions_recent(self) -> [str]:
        # need to store before - only keep most recent 5 or so, excluding pre0, post2, nightly ...
        return self.versions_recent

    def get_version_latest(self) -> str:
        return self.get_versions_recent()[-1]

    def get_versions_checked_time(self) -> int:
        return self.versions_checked_time

    def get_level(self) -> int:
        return self.level

    def get_summary(self) -> str:
        return self.summary

    def get_requires(self) -> [str]:
        return self.requires

    def get_required_by(self) -> [str]:
        return self.required_by
