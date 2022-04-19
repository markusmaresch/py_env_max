#
# -*- coding: utf-8 -*-
#


class EnvCmd:
    @staticmethod
    def environment_import() -> bool:
        # read existing environment and store in internal database
        print('environment_import')
        return True

    @staticmethod
    def environment_update() -> bool:
        # Attempt to update existing python environment
        print('environment_update')
        return True
