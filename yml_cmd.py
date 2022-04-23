#
# -*- coding: utf-8 -*-
#


class YmlCmd:
    @staticmethod
    def yml_export(env_name: str) -> bool:
        # Export existing python environment to YML script
        print('yml_export')
        return True

    @staticmethod
    def yml_import(env_name: str) -> bool:
        # Import conda YML script into internal database
        print('yml_import')
        return True
