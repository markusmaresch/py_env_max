#
# -*- coding: utf-8 -*-
#

# from pip._vendor.distlib.version import NormalizedVersion
from pip._vendor.packaging.utils import canonicalize_name


class Utils:
    @staticmethod
    def canonicalize_name(name_raw: str) -> str:
        return canonicalize_name(name_raw)
