#
# -*- coding: utf-8 -*-
#
import time
import os

from database import Database
from pip_cmd import PipCmd
from pypi_cmd import PyPiCmd


class EnvCmd:

    @staticmethod
    def env_calc_levels(db: Database) -> bool:
        keys = db.packages_get_names()
        print('Check levels for {} packages'.format(len(keys)))
        levels_max = 15
        level = 0
        old_len_lod = 99999
        lod = keys
        while True:
            level += 1
            if level >= levels_max:
                break
            if old_len_lod == len(lod) == 1:
                break
            if len(lod) < 1:
                break
            next_lod = list()
            for d in lod:
                dependencies = db.package_get_requires(name=d)
                if level == 1:
                    if len(dependencies) < 1:
                        db.package_set_level(name=d, level=level)
                        continue
                    # fi
                    next_lod.append(d)
                    continue
                # fi
                # level > 1
                found_below = 0
                needed_below = len(dependencies)
                for dep in dependencies:
                    ll = db.package_get_level(dep)
                    if ll < 0:
                        continue
                    if ll < level:
                        found_below += 1
                # for
                #
                # need for fix
                #
                cyclical = False
                satisfied = (found_below >= needed_below)
                if not satisfied:
                    if d == 'dedupe':
                        if needed_below >= 14 and found_below == needed_below - 1:
                            # nasty hack for cyclical dependencies, which are otherwise hard to detect
                            cyclical = True
                #
                # need for fix
                #
                if satisfied or cyclical:
                    db.package_set_level(name=d, level=level)
                else:
                    next_lod.append(d)
            # for
            old_len_lod = len(lod)
            del lod
            lod = next_lod
        # while
        if len(lod) > 0:
            print('')
            print('Did NOT resolve all packages below')
            for p in lod:
                # not entirely correct !!
                dependencies = db.package_get_requires(p)
                print('  {} {}'.format(p, dependencies))
            print('Did NOT resolve all packages above (could be cyclical behavior)')
            print('')
            return False
        return True

    @staticmethod
    def env_get_releases(db: Database) -> bool:
        keys = db.packages_get_names()
        print('Check releases for {} packages'.format(len(keys)))
        now = int(time.time())
        packages_needed = set()
        for package_name in keys:
            t = db.package_get_releases_checked_time(package_name)
            diff = (now - t) if t > 0 else 9999999
            if diff > 60 * 60:
                packages_needed.add(package_name)
        # for
        if len(packages_needed) < 1:
            print('All packages uptodate for releases ...')
            return True
        print('Get releases for {} packages'.format(len(packages_needed)))
        releases_all = PyPiCmd.get_release_many(packages_needed)
        if releases_all is None:
            return False
        i = 0
        for package_name in packages_needed:
            releases = releases_all[i]
            if releases is None:
                continue
            if not db.package_set_releases_recent(package_name, releases, now):
                return False
            self_check = False
            if self_check:
                rr = db.package_get_releases_recent(package_name)
                if rr is None:
                    return False
            i += 1
        return True

    @staticmethod
    def env_check_consistency(db: Database) -> bool:
        keys = db.packages_get_names()
        print('Testing consistency of {} packages'.format(len(keys)))
        packages_needed = set()
        for name in keys:
            needed = db.package_get_requires(name) + db.package_get_required_by(name)
            for n in needed:
                packages_needed.add(n)
        # for
        print('Found {} depending packages'.format(len(packages_needed)))
        missing = 0
        for name in packages_needed:
            if name in keys:
                continue
            print('  Not found: {} ?'.format(name))
            missing += 1
        # for
        print('Missing depending packages: {}'.format(missing))
        return True

    @staticmethod
    def env_import(env_name: str) -> bool:
        # read existing environment and store in internal database
        db_name = '{}.json'.format(env_name)
        print('env_import: {}'.format(env_name))
        develop = True
        if develop and os.path.exists(db_name):
            db = Database()
            db.load(db_name)
        else:
            packages = PipCmd.pip_list()
            if packages is None:
                return False
            db = Database()
            if not PipCmd.pip_show(db, packages=packages):
                return False
            if not EnvCmd.env_check_consistency(db):
                return False
        # fi
        if not EnvCmd.env_calc_levels(db):
            return False
        if not EnvCmd.env_get_releases(db):  # could be done in parallel to other work
            return False
        ok = True if db.dump(json_path=db_name) else False
        db.close()
        return ok

    @staticmethod
    def env_update(env_name: str) -> bool:
        # Attempt to update existing python environment
        print('env_update: {}'.format(env_name))
        return True
