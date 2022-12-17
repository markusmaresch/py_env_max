#
# -*- coding: utf-8 -*-
#
from database import Database


class StatCmd:

    @staticmethod
    def statistics(env_name: str, force: bool = False) -> bool:
        # Attempt to update existing python environment
        print('statistics: {} (force={})'.format(env_name, force))
        db_name = '{}.json'.format(env_name)
        db = Database()
        if not db.load(db_name):
            # alternatively could call env_import and continue
            return False

        packages = db.packages_get_names_all()
        num_packages = len(packages)

        print('StatCmd: {}'.format(env_name))
        print('\tPackages: total: {}'.format(num_packages))
        for level in range(1, 100):
            pack_level = db.packages_get_names_by_level(level=level)
            if pack_level is None or len(pack_level) < 1:
                break
            print('\t\tLevel\t{}:\t{}'.format(level, len(pack_level)))
        # for

        db.close()
        return True
