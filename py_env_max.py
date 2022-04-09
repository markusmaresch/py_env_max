#
# -*- coding: utf-8 -*-
#
import sys
import argparse
import os

# PIP imports
from pip._internal.commands.check import CheckCommand
from pip._internal.cli.status_codes import SUCCESS

# read before using pip
# https://pypi.org/project/packaging/

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
    def env_activate() -> bool:
        # don't try, will not work, needs to be called by hand in shell
        return False


class Pip:
    @staticmethod
    def available() -> bool:
        # check, if found in $PATH
        return True

    @staticmethod
    def pip_check() -> bool:
        #
        # reconsider: https://pip.pypa.io/en/stable/user_guide/#using-pip-from-your-program
        #
        cc = CheckCommand(name='check', summary='summary')
        result = cc.run(options=None, args=list())
        return True if result == SUCCESS else False

    @staticmethod
    def pip_install(args: [str]) -> bool:
        # build command line
        # execute with popen(cmd, 'r') and kill upon first "taking longer than expected"
        return False

    @staticmethod
    def pip_list() -> None:
        # fairly quick
        # skip first 2 entries
        # get list of
        #   package0 version0_installed
        #   packageN versionN_installed
        return None

    @staticmethod
    def pip_show(args: [str]) -> bool:
        # pip show numpy pandas ...
        #
        # Name: numpy
        # Version: 1.20.0
        # Summary: NumPy is the fundamental package for array computing with Python.
        # Requires: [ some, some2 ]
        # Required-by: [ many, many2]

        # see implementation in pip_show_all.py

        return False


class OsPlatform:
    @staticmethod
    def get() -> str:
        is_win: bool = (os.name == 'nt')
        is_posix = (os.name == 'posix')
        is_darwin = (os.name == 'darwin')
        platforms = {
            'linux1': 'linux',
            'linux2': 'linux',
            'darwin': 'osx',
            'win32': 'windows'
        }
        if sys.platform not in platforms:
            return sys.platform
        return platforms[sys.platform]


class PyEnvMax:
    @staticmethod
    def check_executables() -> bool:
        #
        # check conda, pip in $PATH
        #
        return True

    @staticmethod
    def check_platform() -> bool:
        #
        # check linux, osx, windows
        #
        return True

    @staticmethod
    def check_conda() -> bool:
        #
        # check: conda env list
        #   if 'base' --> really, really check
        #   if not 'py_env_yyyymm -> check again
        #
        # if not good: print command: conda create --name $py_env_name python=${python_default_version}
        # else: use and update
        #
        return True

    @staticmethod
    def run() -> int:
        Pip.check()
        parser = argparse.ArgumentParser()
        return 0


def main():
    #
    # create
    #   py_env_name
    #   python_default_version
    #
    # check:
    #   check_executables
    #   check_platform
    #   check_conda
    #
    return PyEnvMax().run()


if __name__ == '__main__':
    sys.exit(main())
