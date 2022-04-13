#
# -*- coding: utf-8 -*-
#
from py_package import PyPackage


class Database:
    def __init__(self):
        pass

    def package_add(self, name: str) -> PyPackage:
        p = PyPackage(name)
        return p

    def package_update_level(self, package: PyPackage, level: int) -> bool:
        return True

    def package_update_version_latest(self, package: PyPackage, version_latest: str) -> bool:
        return True
