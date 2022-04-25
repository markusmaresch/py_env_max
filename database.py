#
# -*- coding: utf-8 -*-
#
import sys
import json
from packaging import version  # needs to be installed before !! --> distutils.version import LooseVersion (distutils will go away after/with 3.12)


class Database:
    CONFIG = 'config'
    #
    PACKAGES = 'packages'
    #
    VERSION_INSTALLED = 'version_installed'
    SUMMARY = 'summary'
    REQUIRES = 'requires'
    REQUIRED_BY = 'required_by'
    #
    LEVEL = 'level'
    RELEASES_RECENT = 'releases_recent'  # ['1.0', '1.1', '1.3' ...]
    RELEASES_CHECKED_TIME = 'releases_checked_time'
    #
    LOCKED_CONSTRAINTS = 'locked_constraints'  # [ ('tensorflow', '<1.19'), (), ...]
    LOCKED_CHECKED_TIME = 'locked_checked_time'

    def truncate(self) -> dict:
        self.tables = dict()
        self.tables[self.CONFIG] = dict()
        self.tables[self.PACKAGES] = dict()
        return self.tables

    def __init__(self):
        self.tables = self.truncate()

    def close(self):
        # cleanup memory ...
        return

    def dump(self, json_path: str) -> bool:
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.tables, f, ensure_ascii=True, indent=1, sort_keys=True)
                print('Info: written: {}'.format(json_path))
                return True
        except:
            print('Error: dump: {}'.format(json_path))
            return False

    def load(self, json_path: str) -> bool:
        try:
            with open(json_path) as f:
                self.tables = json.load(f)
                return True
        except:
            print('Error: load: {}'.format(json_path))
            return False

    def table_packages(self) -> dict:
        return self.tables[self.PACKAGES]

    def package_add(self, name: str, version_installed: str, summary: str,
                    requires: [str], required_by: [str]) -> bool:
        table = self.table_packages()
        p = table.get(name)
        if p is None:
            table[name] = dict()
            p = table.get(name)
        p[Database.VERSION_INSTALLED] = version_installed
        p[Database.SUMMARY] = summary
        p[Database.REQUIRES] = requires
        p[Database.REQUIRED_BY] = required_by
        return True

    def package_get_releases_recent(self, name: str) -> [str]:
        table = self.table_packages()
        d = table.get(name)
        if d is None:
            # we assume update only
            return None
        releases = d.get(Database.RELEASES_RECENT)
        if releases is None:
            return None
        # need to sort properly !!!!
        s = sorted(releases, key=lambda x: version.Version(x), reverse=True)
        return s

    def package_set_releases_recent(self, name: str, releases: [str], checked_time: int) -> bool:
        table = self.table_packages()
        d = table.get(name)
        if d is None:
            # we assume update only
            return False
        d[Database.RELEASES_RECENT] = releases
        d[Database.RELEASES_CHECKED_TIME] = checked_time
        return True

    def package_set_level(self, name: str, level: int) -> bool:
        table = self.table_packages()
        d = table.get(name)
        if d is None:
            # we assume update only
            return False
        d[Database.LEVEL] = int(level)
        return True

    def package_get_level(self, name: str) -> int:
        table = self.table_packages()
        d = table.get(name)
        if d is None:
            return -1
        level = d.get(Database.LEVEL)
        if level is None:
            return -1
        return int(level)

    def package_get_releases_checked_time(self, name: str) -> int:
        table = self.table_packages()
        d = table.get(name)
        t = d.get(Database.RELEASES_CHECKED_TIME)
        if t is None:
            return -1
        return t

    def package_get_requires(self, name: str) -> [str]:
        table = self.table_packages()
        d = table.get(name)
        return d.get(Database.REQUIRES)

    def package_get_required_by(self, name: str) -> [str]:
        table = self.table_packages()
        d = table.get(name)
        return d.get(Database.REQUIRED_BY)

    def packages_get_names(self) -> [str]:
        table = self.table_packages()
        keys = table.keys()
        return keys

    @staticmethod
    def self_test() -> bool:
        json_path = 'database_selftest.json'
        database = Database()
        database.package_add(name='numpy', version_installed='1.19.3',
                             summary='Numerical library', requires=[],
                             required_by=['pandas', 'many', 'others'])
        database.package_add(name='pandas', version_installed='1.4.3',
                             summary='Data science library', requires=['numpy'],
                             required_by=['many', 'others'])
        database.dump(json_path)
        database.truncate()
        database.load(json_path)
        return True


def main():
    if not Database.self_test():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
