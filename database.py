#
# -*- coding: utf-8 -*-
#
import sys
import json
import typing

from pip._vendor.packaging import version


class Database:
    CONFIG = 'config'
    PACKAGES = 'packages'
    TREES = 'trees'
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
        self.tables[self.CONFIG] = dict(note='JSON style nested database for packages')
        self.tables[self.PACKAGES] = dict()
        self.tables[self.TREES] = dict()
        return self.tables

    def __init__(self):
        self.tables = self.truncate()

    def close(self):
        # cleanup memory ...
        return

    def dump(self, json_path: str) -> bool:
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.tables, f, ensure_ascii=True, indent=4, sort_keys=True)
                print('Info: written: {}'.format(json_path))
                return True
        except:
            print('Error: dump: {}'.format(json_path))
            return False

    def load(self, json_path: str) -> bool:
        try:
            with open(json_path) as f:
                self.tables = json.load(f)
                if self.tables.get(self.TREES) is None:
                    self.tables[self.TREES] = dict()
                return True
        except:
            print('Error: load: {}'.format(json_path))
            return False

    #
    # trees .. rename to package_tree
    #

    def table_trees(self) -> dict:
        return self.tables[self.TREES]

    def trees_get(self) -> dict:
        table = self.table_trees()
        return table

    def trees_set(self, packages_installed_list_of_dicts: typing.List[dict]) -> bool:
        table = self.table_trees()
        table.clear()
        check_package_key = True
        key_name = 'key'  # could be wrong - could be 'package_name'
        for p in packages_installed_list_of_dicts:
            key = p.get(key_name)
            if key is None:
                return False
            if check_package_key:
                package_name = p.get('package_name')
                if package_name is None:
                    return False
                if key != package_name:
                    return False  # only self check; if it never triggers -> both are the same (could remove one)
            # fi
            table[key] = p
        return True

    #
    # packages .. phase OUT
    #

    def table_packages(self) -> dict:
        return self.tables[self.PACKAGES]

    def packages_clear(self) -> bool:
        table = self.table_packages()
        table.clear()
        return True

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
