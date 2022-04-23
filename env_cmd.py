#
# -*- coding: utf-8 -*-
#
from database import Database
from pip_cmd import PipCmd


class EnvCmd:

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
        packages = PipCmd.pip_list()
        if packages is None:
            return False
        db = Database()
        if not PipCmd.pip_show(db, packages=packages):
            return False
        if not EnvCmd.env_check_consistency(db):
            return False
        # calc levels
        # get versions_recent via PypiCmd.get_releases (needs parallel execution)
        ok = True if db.dump(json_path=db_name) else False
        db.close()
        return ok

    @staticmethod
    def env_update(env_name: str) -> bool:
        # Attempt to update existing python environment
        print('env_update: {}'.format(env_name))
        return True
