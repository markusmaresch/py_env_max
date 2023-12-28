#
# -*- coding: utf-8 -*-
#
import datetime

from database import Database
from os_platform import OsPlatform


class ScriptsCmd:
    @staticmethod
    def scripts_export(env_name: str, python_version: str, force: bool = False) -> bool:
        # create scripts for recreating existing python environment
        print('scripts_export: {} (force={})'.format(env_name, force))
        db_name = '{}.json'.format(env_name)
        db = Database()
        if not db.load(db_name):
            print('scripts_export: call environment import before')
            return False
        script_extension = OsPlatform.script_extension()
        script_comment = OsPlatform.script_comment()
        datetime_utc_iso_string = datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            level = 0
            script_name = '{}_{:02d}.{}'.format(env_name, level, script_extension)
            with open(script_name, 'w') as single:
                single.write('{} {}\n'.format(script_comment, datetime_utc_iso_string))
                single.write('{} Level {} .. fix below !\n'.format(script_comment, level))
                single.write('{} conda create --name {}_XXX python={}\n'
                             .format(script_comment, env_name, python_version))
        except Exception as e:
            print('Error: {}'.format(e))
            return False
        script_all_name = '{}_all.{}'.format(env_name, script_extension)
        print('script: {}'.format(script_all_name))
        with open(script_all_name, 'w') as all:
            for level in range(1, 20):
                packs = db.packages_get_names_by_level(level=level)
                if packs is None or len(packs) < 1:
                    break
                script_name = '{}_{:02d}.{}'.format(env_name, level, script_extension)
                print('script: {:02d} {} .. {}'.format(level, len(packs), script_name))
                max_without_check = 10
                with open(script_name, 'w') as single:
                    out = '{} {}\n'.format(script_comment, datetime_utc_iso_string)
                    single.write(out)
                    if level == 1:
                        all.write(out)
                    out = '{} Level {}\n'.format(script_comment, level)
                    single.write(out)
                    all.write(out)
                    ii = 0
                    first_letter = ''
                    finish_check = True
                    for package in packs:
                        version = db.package_get_version_required(package)
                        if first_letter == '':
                            first_letter = package[0]
                        # fi
                        if first_letter != package[0]:
                            first_letter = ''
                            ii = 0
                            out = 'pip check\n'
                            single.write(out)
                            all.write(out)
                        elif ii >= max_without_check:
                            ii = 0
                            out = 'pip check\n'
                            single.write(out)
                            all.write(out)
                        # fi
                        ii += 1

                        # should be '==', but sometimes versions are not found
                        out = f'pip install "{package}>={version}"\n'
                        single.write(out)
                        all.write(out)

                    # for
                    if finish_check:
                        out = 'pip check\n'
                        single.write(out)
                        all.write(out)
                    out = '{} Level {}\n'.format(script_comment, level)
                    single.write(out)
                    all.write(out)
                # with
            # for
        # with
        db.close()
        return True
