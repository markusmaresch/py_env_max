#
# -*- coding: utf-8 -*-
#
import os.path
import sys
import json
import typing
import datetime

from pip._vendor.packaging import version
from pip._vendor.packaging.utils import canonicalize_name


class DateTimeEncoder(json.JSONEncoder):  # is not used for unknown reasons
    def __init__(self):
        super().__init__()

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, obj)


class Database:
    CONFIG = 'config'
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

    def truncate(self) -> dict:
        self.tables = dict()
        self.tables[self.CONFIG] = dict(note='JSON style nested database for packages')
        self.tables[self.PACKAGES] = dict()
        return self.tables

    def __init__(self):
        self.tables = self.truncate()

    def close(self):
        # cleanup memory ...
        return

    def dump(self, json_path: str) -> bool:
        try:
            old_path = json_path + '.old'
            if os.path.exists(old_path):
                os.remove(old_path)
            if os.path.exists(json_path):
                os.rename(json_path, old_path)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.tables, f, ensure_ascii=True, indent=4, sort_keys=True)
                # s = json.dumps(self.tables, cls=DateTimeEncoder)
                # json.dump(s, f, ensure_ascii=True, indent=4, sort_keys=True)
                # f.write(s)
                print('Info: written: {}'.format(json_path))
                return True
        except Exception as e:
            print('Error: dump: {} .. {}'.format(json_path, e))
            return False

    def load(self, json_path: str) -> bool:
        try:
            with open(json_path) as f:
                self.tables = json.load(f)
                return True
        except:
            print('Error: load: {}'.format(json_path))
            return False

    def c_name(self, name_raw: str) -> str:
        return canonicalize_name(name_raw)

    def table_packages(self) -> dict:
        return self.tables[self.PACKAGES]

    def package_set(self, table: dict, key: str, p: dict) -> bool:
        # map from pip's name to our own ones
        # here: key, package_name, version_installed, version_required
        # also merge updates
        # Problem: p could be deep tree dictionary
        table[key] = p
        return True

    def packages_set(self, packages_installed_list_of_dicts: typing.List[dict]) -> bool:
        table = self.table_packages()
        table.clear()
        key_name = 'package_name'
        for p in packages_installed_list_of_dicts:
            key_raw = p.get(key_name)
            if key_raw is None:
                return False
            key = self.c_name(key_raw)
            if not self.package_set(table, key, p):
                return False
        return True

    def package_update(self, name: str, summary: str,
                       required_by: [str]) -> bool:
        table = self.table_packages()
        p = table.get(name)
        if p is None:
            return False
        if summary:
            p[Database.SUMMARY] = summary
        if len(required_by) > 0:
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

    def package_set_releases_recent(self, name: str,
                                    releases: [str], checked_time: int) -> bool:
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
        requires = d.get(Database.REQUIRES)
        if requires is None:
            return []
        return [self.c_name(r['package_name']) for r in requires]

    def package_get_required_by(self, name: str) -> [str]:
        table = self.table_packages()
        d = table.get(name)
        required_by = d.get(Database.REQUIRED_BY)
        if required_by is None:
            return []
        return [self.c_name(r) for r in required_by]

    def packages_get_names(self) -> [str]:
        table = self.table_packages()
        keys = table.keys()
        return [self.c_name(k) for k in keys]

    @staticmethod
    def self_test() -> bool:
        json_path = 'database_selftest.json'
        database = Database()
        database.package_update(name='numpy',
                                summary='Numerical library',
                                required_by=['pandas', 'many', 'others'])
        database.package_update(name='pandas',
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
