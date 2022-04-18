#
# -*- coding: utf-8 -*-
#
import sys
import argparse

from env_cmd import EnvCmd
from req_cmd import ReqCmd
from yml_cmd import YmlCmd


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
        parser = argparse.ArgumentParser(prog='py_env_max',
                                         description='Maintain and maximize a python environment',
                                         epilog='Maximize you python environment !')

        parser.add_argument('--force', action='store_true', help='force creation/overwriting of files')
        parser.add_argument('--env', action='store', help='environment name')

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--env_import', action='store_true',
                           help='Import existing python environment into internal database')
        group.add_argument('--env_update', action='store_true',
                           help='Attempt to carefully update an existing python environment')
        group.add_argument('--req_import', action='store_true',
                           help='Import \'requirements.txt\' into internal database')
        group.add_argument('--req_export', action='store_true',
                           help='Create \'requirements.txt\' from existing python environment')
        group.add_argument('--yml_import', action='store_true',
                           help='Import conda YML script into internal database')
        group.add_argument('--yml_export', action='store_true',
                           help='Create conda YML script from existing python environment')
        args = parser.parse_args()
        print(args)

        if args.env_import:
            EnvCmd.environment_import()
        elif args.env_update:
            EnvCmd.environment_update()
        elif args.yml_import:
            YmlCmd.yml_import()
        elif args.yml_export:
            YmlCmd.yml_export()
        elif args.req_import:
            ReqCmd.req_import()
        elif args.req_export:
            ReqCmd.req_export()
        else:
            print('? internal switch ?')
            parser.print_help()
        return 0

    @staticmethod
    def run_try1() -> int:
        parser = argparse.ArgumentParser(prog='py_env_max',
                                         description='Maintain and maximize a python environment',
                                         epilog='Max you python env !')
        subparsers = parser.add_subparsers(help='commands', dest='action')
        env_parser = subparsers.add_parser('--env', help='manipulate python environment ...')
        yml_parser = subparsers.add_parser('--yml', help='manipulate YML script ...')

        env_parser.add_argument('--import', action='store',
                                help='Import existing python environment into internal database')
        env_parser.add_argument('--update', action='store',
                                help='Attempt to carefully update an existing python environment')

        yml_parser.add_argument('--export', action='store',
                                help='Create YML script from existing python environment')

        args = parser.parse_args()
        print(args)
        print(args.action)
        return 0
        if args.env:
            EnvCmd.environment_import()
            EnvCmd.environment_update()
        elif args.yml:
            print('yml')
        else:
            print('? internal switch ?')
            parser.print_help()
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
