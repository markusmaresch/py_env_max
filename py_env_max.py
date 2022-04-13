#
# -*- coding: utf-8 -*-
#
import sys
# import argparse
# import os

from pip_cmd import PipCmd


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
        PipCmd.pip_selftest()
        # parser = argparse.ArgumentParser()
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
