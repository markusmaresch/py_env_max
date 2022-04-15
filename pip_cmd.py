#
# -*- coding: utf-8 -*-
#
import sys
# import argparse
# import os
import subprocess

from packaging.utils import canonicalize_name

# PIP imports
from pip._internal.commands.check import CheckCommand
from pip._internal.cli.status_codes import SUCCESS

from py_package import PyPackage


# read before using pip
# https://pypi.org/project/packaging/

class PipCmd:
    @staticmethod
    def c_name(name_raw: str) -> str:
        return canonicalize_name(name_raw)

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
    def pip_list() -> [str]:  # only the canonical names of the installed packages; could also provide version_installed
        # fairly quick
        #
        # rework to: json = pip list --format json
        #
        try:
            print('Executing: pip list')
            output = subprocess.check_output(['pip', 'list'])
        except:
            return None
        count = (-2)
        packages = list()
        for line in output.splitlines():
            count += 1
            if count <= 0:
                continue
            package = (line.split()[0]).decode()
            packages.append(package)
        # for
        packages_sorted = sorted(packages, key=str.casefold)
        return packages_sorted

    @staticmethod
    def pip_show() -> [PyPackage]:
        # return list of all installed packages

        packages_sorted = PipCmd.pip_list()
        if packages_sorted is None:
            return None

        arguments = ['pip', 'show'] + [str(elem) for elem in packages_sorted]
        try:
            print('Executing: pip show: of {}'.format(len(packages_sorted)))
            output = subprocess.check_output(arguments)
        except:
            return None
        py_packages = list()
        name = ''
        version = ''
        summary = ''
        requires = ''
        required_by = ''
        for line_b in output.splitlines():
            line = line_b.decode()
            # print(line)
            key, rest = (line.split(maxsplit=1) + [None])[:2]
            if key == 'Name:':
                name_raw = rest.strip()
                name = PipCmd.c_name(name_raw)
            elif key == 'Version:':
                version = rest.strip()
            elif key == 'Summary:':
                if rest is None:
                    summary = ''
                else:
                    summary = rest.strip()
                    if summary != 'UNKNOWN' and summary[-1] == '.':
                        summary = summary[:-1]
            elif key == 'Requires:' or key == 'Required-by:':
                if rest is None:
                    items = []
                else:
                    items_split = rest.strip().split(',')
                    items_sorted = [PipCmd.c_name(str(e.strip())) for e in items_split]
                    items_sorted.sort()
                    items = [e for e in items_sorted]
                if key == 'Requires:':
                    requires = items
                else:
                    required_by = items
            elif line.startswith('-'):
                if name:
                    py_package = PyPackage(name=name, version_installed=version,
                                           summary=summary, requires=requires,
                                           required_by=required_by)
                    del name
                    del version
                    del summary
                    del requires
                    del required_by
                    py_packages.append(py_package)
                continue
            # fi
        #
        test_consistency = True
        if test_consistency:
            print('Testing consistency of {} packages'.format(len(py_packages)))
            packages_needed = set()
            for pp in py_packages:
                needed = pp.get_requires() + pp.get_required_by()
                for n in needed:
                    packages_needed.add(n)
            # for
            print('Found {} depending packages'.format(len(packages_needed)))
            missing = 0
            for p in packages_needed:
                found = False
                for cp in py_packages:
                    if p == cp.get_name():
                        found = True
                        break
                    # fi
                # for
                if found:
                    continue

                print('  Not found: {} ?'.format(p))
                missing += 1
            # for
            print('Missing depending packages: {}'.format(missing))
        # fi

        # calculate level

        return py_packages

    @staticmethod
    def pip_outdated() -> (str, str, str, str):
        # pip list --outdated --format json
        # fairly slow .. up to one minute
        return None

    @staticmethod
    def pip_selftest() -> bool:
        packages = PipCmd().pip_show()
        if packages is None:
            return False
        packages = PipCmd().pip_list()
        if packages is None:
            return False

        return True


def main():
    if not PipCmd.pip_selftest():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
