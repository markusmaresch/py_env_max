#
# -*- coding: utf-8 -*-
#
import sys
import argparse
import datetime
import typing

from env_cmd import EnvCmd
from req_cmd import ReqCmd
from yml_cmd import YmlCmd
from conda_cmd import CondaCmd
from pip_cmd import PipCmd
from scripts_cmd import ScriptsCmd
from os_platform import OsPlatform
from stat_cmd import StatCmd
from version import Version


class PyEnvMax:
    def __init__(self):
        self.environment_name = None
        self.environment_default = self.get_environment_default()
        self.python_version_default = '3.9'
        self.conda_version_minimum = '4.10.3'
        return

    def get_environment_default(self) -> str:
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        py_env_name = 'py_env_{}{:0=2d}'.format(year, month)
        return py_env_name

    def set_activated_environment(self, activated: str):
        self.environment_name = activated
        return

    def get_activated_environment(self) -> str:
        return self.environment_name

    @staticmethod
    def check_executables() -> bool:
        version = PipCmd.version()
        if not version:
            return False
        # print('Using: pip=={}'.format(version))
        return True

    def check_os_platform(self) -> bool:
        op = OsPlatform.get()
        if not OsPlatform.valid(op):
            return False
        # print('Using: {}'.format(op.__repr__()))
        return True

    def check_conda_basic(self) -> bool:
        version = CondaCmd.version()
        if version is None or not version:
            print('Error: conda not working; is miniconda installed ?')
            print('See: https://docs.conda.io/en/latest/miniconda.html')
            return False
        print('Using: conda=={}'.format(version))

        vh = Version.normalized(version)
        vm = Version.normalized(self.conda_version_minimum)
        if vh < vm:
            print('Warning: conda too old ({} < {}), consider updating conda itself or miniconda'.format(vh, vm))
            # return False
        return True

    def check_conda_environment(self, env_override: str, force: bool) -> typing.Union[str, object]:
        activated = CondaCmd.env_activated() if env_override is None else env_override
        if not activated:
            print('Error: cannot determine activated conda environment')
            print('Check: conda env list')
            return None
        if activated == 'base':
            default = self.get_environment_default()
            print('Error: do not use \'base\' conda environment')
            print()
            print('Consider creating a new environment:')
            print('\tconda create --name {} python={}'
                  .format(default, self.python_version_default))
            print('\tconda activate {}'.format(default))
            # here go boot strapping packages .. UNLESS those can be found in pip._vendor !!
            print()
            return None
        self.set_activated_environment(activated)
        print('Using: {}  .. as activated environment'.format(activated))
        return activated

    def run(self) -> int:
        env_default = self.get_environment_default()
        parser = argparse.ArgumentParser(prog='py_env_max',
                                         description='Maintain and maximize one python environment',
                                         epilog='Maximize you python environment !')

        parser.add_argument('-f', '--force', action='store_true', help='force creation/overwriting of files')
        parser.add_argument('-p', '--packages', action='store_true', help='packages to install')
        parser.add_argument('-e', '--env', action='store',
                            help='environment name, overriding \'{}\''.format(env_default))

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--stat', action='store_true',
                            help='Show statistics of existing python environment')

        group.add_argument('--env_import', action='store_true',
                           help='Import existing python environment into internal database')

        group.add_argument('-ip', '--install_packages', action='extend', nargs='+', type=str,
                            help='Attempt to install packages to existing python environment')

        group.add_argument('-ua', '--upd_all', action='store_true',
                            help='Attempt to update all of existing python environment')

        group.add_argument('-ri', '--req_import', action='store_true',
                           help='Import \'requirements.txt\' into internal database')
        group.add_argument('-re', '--req_export', action='store_true',
                           help='Create \'requirements.txt\' from existing python environment')
        group.add_argument('-yi', '--yml_import', action='store_true',
                           help='Import conda YML script into internal database')
        group.add_argument('-ye', '--yml_export', action='store_true',
                           help='Create conda YML script from existing python environment')
        group.add_argument('-se', '--scripts_export', action='store_true',
                           help='Create scripts for recreating existing python environment')
        args = parser.parse_args()
        # print(args)
        force = args.force
        env_name = self.check_conda_environment(args.env, force)
        if env_name is None:
            return False

        env_name = self.get_activated_environment() if env_name is None else env_name
        if args.stat:
            StatCmd.statistics(env_name=env_name, force=force)
        elif args.env_import:
            EnvCmd.env_import(env_name=env_name, force=force)
        elif args.yml_import:
            YmlCmd.yml_import(env_name=env_name, force=force)
        elif args.yml_export:
            YmlCmd.yml_export(env_name=env_name, force=force)
        elif args.req_import:
            ReqCmd.req_import(env_name=env_name, force=force)
        elif args.req_export:
            ReqCmd.req_export(env_name=env_name, force=force)
        elif args.upd_all:
            EnvCmd.upd_all(env_name=env_name, force=force)
        elif args.install_packages:
            packages = args.install_packages
            EnvCmd.install_packages(env_name=env_name, packages=packages, force=force)
        elif args.scripts_export:
            ScriptsCmd.scripts_export(env_name=env_name, python_version=self.python_version_default, force=force)
        else:
            print('? internal switch missing ?')
            parser.print_help()
        return 0


def main():
    #
    # create
    #   py_env_name .. py_env_yyyymm
    #   python_default_version .. 3.9
    #
    # check:
    #   check_executables
    #   check_platform
    #
    pem = PyEnvMax()
    if not pem.check_os_platform():
        return 1
    if not pem.check_executables():
        return 1
    if not pem.check_conda_basic():
        return 1
    return pem.run()


if __name__ == '__main__':
    sys.exit(main())
