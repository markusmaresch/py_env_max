#
# -*- coding: utf-8 -*-
#
import sys
import json
import typing

from pip._vendor.packaging import version


class Database:
    CONFIG = 'config'
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

    def truncate(self) -> dict:
        self.tables = dict()
        self.tables[self.CONFIG] = dict(note='JSON style nested database for packages')
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

    def table_trees(self) -> dict:
        return self.tables[self.TREES]

    def trees_get(self) -> dict:
        table = self.table_trees()
        return table

    def trees_set(self, packages_installed_list_of_dicts: typing.List[dict]) -> bool:
        table = self.table_trees()
        table.clear()
        key_name = 'key'
        for p in packages_installed_list_of_dicts:
            key = p.get(key_name)
            if key is None:
                return False
            table[key] = p
        return True

    def tree_update(self, name: str, summary: str, required_by: [str]) -> bool:
        table = self.table_trees()
        p = table.get(name)
        if p is None:
            return False
        if summary:
            p[Database.SUMMARY] = summary
        if len(required_by) > 0:
            p[Database.REQUIRED_BY] = required_by
        return True

    def tree_get_releases_recent(self, name: str) -> [str]:
        table = self.table_trees()
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

    def tree_set_releases_recent(self, name: str, releases: [str], checked_time: int) -> bool:
        table = self.table_trees()
        d = table.get(name)
        if d is None:
            # we assume update only
            return False
        d[Database.RELEASES_RECENT] = releases
        d[Database.RELEASES_CHECKED_TIME] = checked_time
        return True

    def tree_set_level(self, name: str, level: int) -> bool:
        table = self.table_trees()
        d = table.get(name)
        if d is None:
            # we assume update only
            return False
        d[Database.LEVEL] = int(level)
        return True

    def tree_get_level(self, name: str) -> int:
        table = self.table_trees()
        d = table.get(name)
        if d is None:
            return -1
        level = d.get(Database.LEVEL)
        if level is None:
            return -1
        return int(level)

    def tree_get_releases_checked_time(self, name: str) -> int:
        table = self.table_trees()
        d = table.get(name)
        t = d.get(Database.RELEASES_CHECKED_TIME)
        if t is None:
            return -1
        return t

    def tree_get_requires(self, name: str) -> [str]:
        table = self.table_trees()
        d = table.get(name)
        requires = d.get(Database.REQUIRES)
        if requires is None:
            return []
        return [r['package_name'] for r in requires]

    def tree_get_required_by(self, name: str) -> [str]:
        table = self.table_trees()
        d = table.get(name)
        required_by = d.get(Database.REQUIRED_BY)
        if required_by is None:
            return []
        return required_by

    def trees_get_names(self) -> [str]:
        table = self.table_trees()
        keys = table.keys()
        return keys

    @staticmethod
    def self_test() -> bool:
        json_path = 'database_selftest.json'
        database = Database()
        database.tree_update(name='numpy',
                             summary='Numerical library',
                             required_by=['pandas', 'many', 'others'])
        database.tree_update(name='pandas',
                             summary='Data science library',
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
