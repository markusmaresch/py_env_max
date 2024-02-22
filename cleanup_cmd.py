#
# -*- coding: utf-8 -*-
#
import json

from database import Database


class CleanupCmd:

    @staticmethod
    def top_level(env_name: str, force: bool = False) -> bool:
        # Attempt to update existing python environment
        print('top_level: {} (force={})'.format(env_name, force))
        db_name = '{}.json'.format(env_name)
        db = Database()
        if not db.load(db_name):
            # alternatively could call env_import and continue
            return False

        #
        # cat $(git ls-files --recurse-submodules | grep -e "\.py$" ) | grep -e "^import " -e "^from " | grep import | sort -u
        #

        try:
            with open('top_level_exceptions.json', 'r') as f:
                tl = json.load(f)
        except Exception as e:
            print(f'Json for Exceptions: {e} ?')
            return False

        packages = db.packages_get_names_all()
        num_packages = len(packages)

        print('top_level: {}'.format(env_name))
        print('Packages: total: {}'.format(num_packages))
        num_top_level = 0
        level = 0
        while True:
            level += 1
            packages_per_level = db.packages_get_names_by_level(level=level)
            if packages_per_level is None or len(packages_per_level) < 1:
                break
            # print('\t\tLevel\t{}:\t{}'.format(level, len(packages_per_level)))
            num_level_top_level = 0
            for package_name in packages_per_level:
                required_by = db.package_get_required_by(package_name)
                if required_by is None:
                    continue
                rb_len = len(required_by)
                if rb_len > 0:
                    # print(f'Level: {level} package_name: {package_name} required by: {required_by}')
                    continue
                summary = db.package_get_summary(package_name)

                if package_name in tl['top_level_exceptions']:
                    continue

                print(f'Top level or orphan: {level} / {package_name} .. {summary}')
                num_top_level += 1
                num_level_top_level += 1
            # for
            if num_level_top_level > 0:
                print(f'Total for {level}: {num_level_top_level}')
                print('\n')
        # for

        print('Top level or orphans: {}'.format(num_top_level))
        db.close()
        return True
