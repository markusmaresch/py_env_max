#
# -*- coding: utf-8 -*-
#


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
        return True
