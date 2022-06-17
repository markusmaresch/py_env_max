#
# -*- coding: utf-8 -*-
#
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
    def normalized(release: str) -> NormalizedVersion:
        return NormalizedVersion(release)
