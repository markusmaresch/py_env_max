#
# -*- coding: utf-8 -*-
#


class YmlCmd:
    @staticmethod
    def yml_export(env_name: str, force: bool = False) -> bool:
        # Export existing python environment to YML script
        print('yml_export: {} (force={})'.format(env_name, force))
        print('conda env export --no-builds')
        # call it really, read back output - update yml/template/<os>/conda_<os>_<py_version>.yml
        return True

    @staticmethod
    def yml_import(env_name: str, force: bool = False) -> bool:
        # Import conda YML script into internal database
        print('yml_import: {} (force={})'.format(env_name, force))
        return True
