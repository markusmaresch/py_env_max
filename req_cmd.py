#
# -*- coding: utf-8 -*-
#
from database import Database


class ReqCmd:
    @staticmethod
    def req_import(env_name: str, force: bool = False) -> bool:
        # Import 'requirements.txt' into internal database
        # also import own tags and hints
        print('req_import: {} (force={})'.format(env_name, force))
        return True

    @staticmethod
    def req_export(env_name: str, force: bool = False) -> bool:
        # Export existing python environment to 'requirements.txt' script
        print('req_export: {} (force={})'.format(env_name, force))
        db_name = '{}.json'.format(env_name)
        db = Database()
        if not db.load(db_name):
            # alternatively could call env_import and continue
            return False

        old_len = (-1)
        for level in range(1, 100):
            packs = db.packages_get_names_by_level(level=level, less_then=True)
            if packs is None:
                break
            new_len = len(packs)
            if old_len == new_len:
                break
            req_name = 'requirements_{}_{:02d}.txt'.format(env_name, level)
            with open(req_name, 'w') as r:
                r.write('#\n# requirements for {} .. levels {} -> {}\n#\n'
                        .format(env_name, 1, level))
                print('req: {} {} .. {}'.format(level, new_len, req_name))
                old_len = new_len
                ll = 0
                while ll < level:
                    ll += 1
                    pack_level = db.packages_get_names_by_level(level=ll)
                    if pack_level is None:
                        break
                    if len(pack_level) < 1:
                        break
                    # print('\treq2: {} {}'.format(ll, pack_level))
                    for p in pack_level:
                        version_required = db.package_get_version_required(p)
                        # print('\t\t{}=={}'.format(p, version_required))
                        r.write('{}=={}\n'.format(p, version_required))
                    # for
                    r.write('#\n')
                # while
                r.write('#\n')
            # with
        # for
        db.close()
        return True
