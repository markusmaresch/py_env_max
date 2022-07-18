#
# -*- coding: utf-8 -*-
#
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
            return False
        script_extension = OsPlatform.script_extension()
        script_comment = OsPlatform.script_comment()
        try:
            level = 0
            script_name = '{}_{:02d}.{}'.format(env_name, level, script_extension)
            with open(script_name, 'w') as s:
                s.write('{} Level {} .. fix below !\n'.format(script_comment, level))
                s.write('{} conda create --name {}_XXX python={}\n'
                        .format(script_comment, env_name, python_version))
        except Exception as e:
            print('Error: {}'.format(e))

        script_all_name = '{}_all.{}'.format(env_name, script_extension)
        print('script: {}'.format(script_all_name))
        with open(script_all_name, 'w') as a:
            for level in range(1, 20):
                packs = db.packages_get_names_by_level(level=level)
                if packs is None or len(packs) < 1:
                    break
                script_name = '{}_{:02d}.{}'.format(env_name, level, script_extension)
                print('script: {:02d} {} .. {}'.format(level, len(packs), script_name))
                max_per_line = 8
                with open(script_name, 'w') as s:
                    out = '{} Level {}\n'.format(script_comment, level)
                    s.write(out)
                    a.write(out)
                    ii = 0
                    for package in packs:
                        if ii == 0:
                            out = 'pip install'
                            s.write(out)
                            a.write(out)
                        version = db.package_get_version_required(package)
                        out =' {}=={}'.format(package, version)
                        s.write(out)
                        a.write(out)
                        ii += 1
                        if ii >= max_per_line:
                            out = '\npip check\n'
                            s.write(out)
                            a.write(out)
                            ii = 0
                    # for
                    if ii != 0:
                        out = '\npip check\n'
                        s.write(out)
                        a.write(out)
                    out = '{} Level {}\n'.format(script_comment, level)
                    s.write(out)
                    a.write(out)
                # with
            # for
        # with
        db.close()
        return True
