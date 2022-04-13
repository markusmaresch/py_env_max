#
# -*- coding: utf-8 -*-
#

class Conda:
    @staticmethod
    def available() -> bool:
        # check, if found in $PATH
        return True

    @staticmethod
    def env_export() -> bool:
        # call: conda env export --no-builds
        return True

    @staticmethod
    def env_list() -> [str]:
        # call: conda env list | awk '{print $1}' # more or less
        return None

    @staticmethod
    def env_activated() -> str:
        # conda env list | grep -e ' \* ' | awk '{print $1}'
        return None

    @staticmethod
    def env_activate(env_name: str) -> bool:
        # don't try, will not work, needs to be called by hand in shell
        return False
