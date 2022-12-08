#
# -*- coding: utf-8 -*-
#
import difflib
import os
import sys
import json
import typing
import datetime

from utils import Utils
from release_filter import ReleaseFilter
from constraints import Constraints
from version import Version


class DateTimeEncoder(json.JSONEncoder):  # is not used for unknown reasons
    def __init__(self):
        super().__init__()

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, obj)


class PyPi:
    PACKAGE_NAME = 'package_name'


class Database:
    CONFIG = 'config'
    PACKAGES = 'packages'
    #
    VERSION_INSTALLED = 'version_installed'
    VERSION_REQUIRED = 'version_required'
    SUMMARY = 'summary'
    REQUIRES = 'requires'
    REQUIRED_BY = 'required_by'
    #
    LEVEL = 'level'
    RELEASES_RECENT = 'releases_recent'
    RELEASES_CHECKED_TIME = 'releases_checked_time'

    def truncate(self) -> dict:
        self.tables = dict()
        self.tables[self.CONFIG] = dict(note='JSON style nested database for packages')
        self.tables[self.PACKAGES] = dict()
        return self.tables

    def __init__(self):
        self.dirty = False  # is this correct ?
        self.tables = self.truncate()

    def close(self):
        # cleanup memory ...
        return

    def set_dirty(self, flag: bool, reason: str = None):
        if self.dirty == flag:
            return
        if flag and reason is not None:
            print('set_dirty: {} (only first one !)'.format(reason))
        self.dirty = flag

    def get_dirty(self) -> bool:
        return self.dirty

    def dump(self, json_path: str) -> bool:
        if not self.get_dirty():
            print('Info: NOT written: {} .. dirty was {}'
                  .format(json_path, self.get_dirty()))
            return True
        # fi
        try:
            old_path = json_path + '.old'
            have_old = False
            if os.path.exists(old_path):
                os.remove(old_path)
            if os.path.exists(json_path):
                os.rename(json_path, old_path)
                have_old = True
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.tables, f, ensure_ascii=True, indent=4, sort_keys=True)
                # s = json.dumps(self.tables, cls=DateTimeEncoder)
                # json.dump(s, f, ensure_ascii=True, indent=4, sort_keys=True)
                # f.write(s)
                print('Info: written: {} .. dirty was {}'
                      .format(json_path, self.get_dirty()))
                self.set_dirty(False)
            # with
            if have_old and False:
                with open(old_path, 'r') as f_old, open(json_path, 'r') as f_new:
                    diffs = difflib.ndiff(f_old.readlines(), f_new.readlines())
                    pattern = '"{}":'.format(Database.RELEASES_CHECKED_TIME)
                    for d in diffs:
                        if not d.startswith('+ ') and not d.startswith('- '):
                            continue
                        if d.find(pattern) >= 0:
                            continue
                        print(d, end='')
                    # for
                # with
            return True
        except Exception as e:
            print('Error: dump: {} .. {}'.format(json_path, e))
            return False

    def load(self, json_path: str, verbose: bool = True) -> bool:
        try:
            with open(json_path) as f:
                self.tables = json.load(f)
                self.set_dirty(False)
                return True
        except:
            if verbose:
                print('Error: load: {}'.format(json_path))
            return False

    def table_packages(self) -> dict:
        return self.tables[self.PACKAGES]

    def package_set(self, table: dict, key: str, p: dict) -> bool:
        # map from pip's name to our own ones
        # here: key, package_name, version_installed, version_required
        # also merge updates
        # Problem: p could be deep tree dictionary
        if table.get(key) is None:
            table[key] = p
            self.set_dirty(True, reason='new {}'.format(key))
            return True
        # fi
        # need to update
        keys = p.keys()
        for k in keys:
            table_key = table.get(key)
            if table_key is not None:
                table_key_sub_k = table_key.get(k)
                if table_key_sub_k == p[k]:
                    # no need to update
                    continue
            table_key[k] = p[k]
            self.set_dirty(True, reason='update {}/{}'.format(key, k))
        return True

    def packages_set(self, packages_installed_list_of_dicts: typing.List[dict]) -> bool:
        table = self.table_packages()
        # table.clear()
        for p in packages_installed_list_of_dicts:
            key_raw = p.get(PyPi.PACKAGE_NAME)
            if key_raw is None:
                return False
            key = Utils.canonicalize_name(key_raw)
            if not self.package_set(table, key, p):
                return False
        return True

    def package_remove(self, name: str) -> bool:
        table = self.table_packages()
        p = table.get(name)
        if p is None:
            return False
        del table[name]
        self.set_dirty(True, reason='delete: {}'.format(name))
        return True

    def package_set_required_by(self, name: str, required_by: [str]) -> bool:
        table = self.table_packages()
        p = table.get(name)
        if p is None:
            p = table[name] = dict()
        if len(required_by) > 0:
            old_required_by = p.get(Database.REQUIRED_BY)
            if old_required_by != required_by:
                p[Database.REQUIRED_BY] = required_by
                self.set_dirty(True, reason='required_by: {}/{}'
                               .format(name, required_by))
            else:
                pass  # print('RequiredBy: same or empty before')
        return True

    def package_set_summary(self, name: str, summary: str) -> bool:
        table = self.table_packages()
        p = table.get(name)
        if p is None or summary is None:
            return False
        if summary:
            summary = summary.strip()
            if summary != 'UNKNOWN' and summary[-1] == '.':
                summary = summary[:-1]
            old_summary = p.get(Database.SUMMARY)
            if old_summary is None or old_summary != summary:
                p[Database.SUMMARY] = summary
                self.set_dirty(True, reason='summary: {}/{}'.format(name, summary))
            else:
                pass  # print('Summary: same or empty before')
        return True

    def package_get_releases_recent(self, name: str, release_filter: ReleaseFilter) -> [str]:
        table = self.table_packages()
        d = table.get(name)
        if d is None:
            # we assume update only
            return None
        releases = d.get(Database.RELEASES_RECENT)
        if releases is None:
            return None
        if len(releases) < 1:
            return None  # should not happen - indicates a too strict filter on environment import

        re_invalid_pattern = ReleaseFilter.get_re_invalid_pattern(release_filter=release_filter)
        rs = [r for r in releases if ReleaseFilter.valid(r, re_invalid_pattern=re_invalid_pattern)]
        s = Version.sort(releases=rs, reverse=True)
        return s

    def package_set_releases_recent(self, name: str,
                                    releases: [str], checked_time: int) -> bool:
        if releases is None:
            return False
        table = self.table_packages()
        d = table.get(name)
        if d is None:
            # we assume update only
            return False
        old_releases = d.get(Database.RELEASES_RECENT)
        if old_releases is not None:
            releases += old_releases
            releases = list(sorted(set(releases), reverse=False))
            # releases = Version.sort(releases=releases, reverse=True)
            # now merged - could still be the same
        if old_releases is None:
            d[Database.RELEASES_RECENT] = releases
            self.set_dirty(True, reason='releases: {}/{} no old'.format(name, releases))
        elif len(old_releases) != len(releases):
            d[Database.RELEASES_RECENT] = releases
            self.set_dirty(True, reason='releases: {}/{} diff len'.format(name, releases))
        elif sorted(old_releases) != sorted(releases):
            d[Database.RELEASES_RECENT] = releases
            self.set_dirty(True, reason='releases: {}/{} diff2'.format(name, releases))
        else:
            pass  # print('Releases: same or empty before')

        old_checked_time = d.get(Database.RELEASES_CHECKED_TIME)
        if old_checked_time is None or old_checked_time != checked_time:
            d[Database.RELEASES_CHECKED_TIME] = checked_time
            diff = checked_time - old_checked_time \
                if old_checked_time is not None else 99999
            self.set_dirty(True, reason='checked_time: {}: {}'
                           .format(name, diff))
        else:
            print('Release check time: same or empty before')

        return True

    def package_set_level(self, name: str, level: int) -> bool:
        table = self.table_packages()
        d = table.get(name)
        if d is None:
            # we assume update only
            return False
        old_level = d.get(Database.LEVEL)
        if old_level is None:
            pass
        elif old_level == level:
            return True
        else:
            self.set_dirty(True, reason='set_level: {}: {} -> {}'
                           .format(name, old_level, level))
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
        seen = set()
        a = set([r['package_name'] for r in requires])
        dupes = [x for x in a if seen.add(x)]
        if len(dupes) > 0:  # we could salvage the situation here, but the problem is at inserting
            print('error multiple packages as requirements: {} {}: {}'.format(name, dupes[0], requires))
        return [Utils.canonicalize_name(r['package_name']) for r in requires]

    def package_get_required_by(self, name: str) -> [str]:
        table = self.table_packages()
        d = table.get(name)
        required_by = d.get(Database.REQUIRED_BY)
        if required_by is None:
            return []
        return [Utils.canonicalize_name(r) for r in required_by]

    def package_get_version_required(self, name: str) -> typing.Union[str, object]:
        table = self.table_packages()
        d = table.get(name)
        if d is None:
            return None
        vr = d.get(Database.VERSION_REQUIRED)
        if vr is None:
            return '0.0.1'
        return vr

    def packages_get_names_all(self) -> [str]:
        table = self.table_packages()
        keys = table.keys()
        return [Utils.canonicalize_name(k) for k in keys]

    def packages_get_names_by_level(self, level: int, less_then: bool = False) -> [str]:
        table = self.table_packages()
        keys_all = table.keys()
        keys_level = list()
        for k in keys_all:
            lev = self.package_get_level(k)
            if less_then:
                if lev > level:
                    continue
            else:
                if lev != level:
                    continue
            keys_level.append(k)
        return [Utils.canonicalize_name(k) for k in keys_level]

    def packages_get_contraints(self, package: str) -> Constraints:
        constraints = Constraints(package=package)

        def recurse_dict(d):
            for k, v in d.items():
                if isinstance(v, dict):
                    recurse_dict(v)
                else:
                    if k != Database.REQUIRES:
                        continue
                    for r in v:
                        pn = r.get(PyPi.PACKAGE_NAME)
                        if pn != package:
                            # could be dangerous, need to make sure we are comparing in the same names-spaces
                            continue
                        vr = r.get(Database.VERSION_REQUIRED)
                        if vr is None:
                            # no constraint given at all
                            continue
                        constraints.append(vr)  # can be comma separated
                    # for
            return

        table = self.table_packages()
        recurse_dict(table)
        constraints.optimize()
        return constraints

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
