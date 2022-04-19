#
# -*- coding: utf-8 -*-
#
import sys
import subprocess


class CondaCmd:
    @staticmethod
    def version() -> str:
        version = ''
        try:
            print('Executing: conda -V')
            output = subprocess.check_output(['conda', '-V'])
            for line in output.splitlines():
                v = line.decode().split()
                if v[0] != 'conda':
                    continue
                version = v[1]
                break
            # for
        except:
            pass
        return version

    @staticmethod
    def env_export() -> bool:
        # call: conda env export --no-builds
        # takes long
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

    @staticmethod
    def selftest() -> bool:
        version = CondaCmd.version()
        if version is None or not version:
            return False
        if CondaCmd.env_activate('any_env_name'):
            return False
        return True


def main():
    if not CondaCmd.selftest():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
