#
# -*- coding: utf-8 -*-
#
import typing

from pip._vendor.packaging import version
from pip._vendor.distlib.version import NormalizedVersion


class Version:

    @staticmethod
    def sort(releases: [str], reverse: bool) -> [str]:
        try:
            s = sorted(releases, key=lambda x: version.Version(x), reverse=reverse)
        except:
            # there are all sorts of invalid versions, which cause an exeption above
            # therefore use regular reverse sort and hope for minimal damage
            # need to post-clean
            s = sorted(releases, reverse=reverse)
            # print('Has invald: {}'.format(rs))
        return s

    @staticmethod
    def convert(release: str) -> version.Version:
        return version.Version(release)

    @staticmethod
    def normalized(release: str) -> typing.Union[NormalizedVersion, object]:
        try:
            return NormalizedVersion(release)
        except:
            # like "2022.*" .. what to do ?
            # not a valid PEP440 version !
            return None
