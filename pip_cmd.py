#
# -*- coding: utf-8 -*-
#
import sys
import subprocess

from packaging.utils import canonicalize_name

# PIP imports
from pip._internal.commands.check import CheckCommand
from pip._internal.cli.status_codes import SUCCESS

from database import Database


# from database import Database


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
    def version() -> str:
        version = ''
        try:
            output = subprocess.check_output(['pip', '-V'])
            for line in output.splitlines():
                v = line.decode().split()
                if v[0] != 'pip':
                    continue
                version = v[1]
                break
            # for
        except:
            pass
        if not version:
            print('Failed: pip -V')
        return version

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
    def pip_list() -> [str]:
        # only the canonical names of the installed packages; could also provide version_installed
        # fairly quick
        # pip list .. not very useful by itself !
        # rework to: json = pip list --format json
        #
        try:
            print('Executing: pip list')
            output = subprocess.check_output(['pip', 'list'])
        except:
            print('Error: pip list')
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
        packages_set = set(packages)
        packages_sorted = sorted(packages_set, key=str.casefold)
        return packages_sorted

    @staticmethod
    def pip_show(db: Database, packages: [str]) -> bool:
        # return list of all installed packages
        arguments = ['pip', 'show'] + [str(elem) for elem in packages]
        try:
            print('Executing: pip show: of {}'.format(len(packages)))
            output = subprocess.check_output(arguments)
        except:
            print('Error: pip show: of {}'.format(len(packages)))
            return False
        name = None
        version = None
        summary = None
        requires = None
        required_by = None
        for line_b in output.splitlines():
            line = line_b.decode()
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
                # fi
            elif key == 'Home-page:' or key == 'Author:' \
                    or key == 'Author-email:' or key == 'License:' \
                    or key == 'Location:':
                continue
            elif line.startswith('-'):
                continue
            # fi
            if name is not None and version is not None and summary is not None\
                    and requires is not None and required_by is not None:
                if not db.package_add(name=name, version_installed=version,
                                      summary=summary, requires=requires,
                                      required_by=required_by):
                    print('Error: db.package_add({})'.format(name))
                    return False
                name = None
                version = None
                summary = None
                requires = None
                required_by = None
                continue
            else:
                continue
            # fi
        # for
        return True

    @staticmethod
    def pip_outdated() -> (str, str, str, str):
        # pip list --outdated --format json
        # fairly slow .. up to one minute
        return None

    @staticmethod
    def pip_selftest() -> bool:
        version = PipCmd.version()
        if not version:
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
