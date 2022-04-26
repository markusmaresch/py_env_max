#
# -*- coding: utf-8 -*-
#
import sys
import subprocess
import typing
import json
import itertools

# PIP imports
from pip._internal.commands.check import CheckCommand
from pip._internal.cli.status_codes import SUCCESS
from pip._internal.utils.misc import get_installed_distributions
from pip._vendor.packaging.utils import canonicalize_name

# installed packages
from _vendor.pipdeptree import PackageDAG, conflicting_deps, render_conflicts_text, \
    cyclic_deps  # needs to be installed (only depends on pip)

# own imports
from database import Database


class PipCmd:

    @staticmethod
    def render_json_tree(tree: PackageDAG, indent: int, truncate: bool = False):
        """Converts the tree into a nested json representation.
        """

        def aux(node, parent=None, chain=None):
            if chain is None:
                chain = [node.project_name]
            d = node.as_dict()
            if parent:
                d['required_version'] = node.version_spec if node.version_spec else 'Any'
            else:
                d['required_version'] = d['installed_version']
            deps = [
                aux(c, parent=node, chain=chain + [c.project_name])
                for c in tree.get_children(node.key)
                if c.project_name not in chain
            ]
            if len(deps) > 0:
                d['requires'] = deps
            return d

        # def aux()

        tree = tree.sort()
        if truncate:
            # at outer level, discard node, if it is included as sub tree somewhere
            # plus: shorter
            # minus: not all at outer level
            branch_keys = set(r.key for r in itertools.chain.from_iterable(tree.values()))
            nodes = [p for p in tree.keys() if p.key not in branch_keys]
        else:
            # all trees at outer level, even if those are sub trees somewhere
            # plus: complete at outer level
            nodes = [p for p in tree.keys()]
        # fi
        out_nodes = [aux(p) for p in nodes]
        return json.dumps(out_nodes, indent=indent)

    @staticmethod
    def get_tree_installed() -> typing.Union[PackageDAG, typing.Any]:
        local_only = False
        user_only = False
        print('Getting installed distributions ..')
        pkgs = get_installed_distributions(local_only=local_only, user_only=user_only)
        try:
            print('Converting installed distributions to tree ..')
            tree = PackageDAG.from_pkgs(pkgs)
        except:
            return None
        print('Done with tree ..')
        return tree

    @staticmethod
    def get_conflicts(tree: PackageDAG, verbose: bool = False) -> [str]:
        if verbose:
            print('Checking conflicts ..')
        conflicts = conflicting_deps(tree)
        if len(conflicts) < 1:
            if verbose:
                print('No conflicts')
            return []
        # this did not happen, but we should not continue here
        if verbose:
            print('Conflicts:')
            render_conflicts_text(conflicts)

        # prepare return list
        lines = list()
        pkgs = sorted(conflicts.keys())
        #
        # not tested below - we had no use case so far !!
        #
        for p in pkgs:
            pkg = p.render_as_root(False)
            line0 = '* {}'.format(pkg)
            lines.append(line0)
            for req in conflicts[p]:
                req_str = req.render_as_branch(False)
                line1 = ' - {}'.format(req_str)
                lines.append(line1)
        return lines

    @staticmethod
    def get_cycles(tree: PackageDAG, verbose: bool = False) -> [str]:
        if verbose:
            print('Checking cycles ..')
        cycles_packages = cyclic_deps(tree)
        if len(cycles_packages) < 1:
            if verbose:
                print('No cycles')
            return []
        cycles_strings = list()
        cycles_tuples = sorted(cycles_packages, key=lambda xs: xs[1].key)
        if verbose:
            print('Cycles:')
        for a, b, c in cycles_tuples:
            cycles_strings.append(a.project_name)
            if verbose:
                print('  {} => {}'.format(a.project_name, b.project_name))
        # for
        return cycles_strings

    @staticmethod
    def c_name(name_raw: str) -> str:
        return canonicalize_name(name_raw)

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
        db.packages_clear()
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
            if name is not None and version is not None and summary is not None \
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
        packages_installed_list_of_dicts = PipCmd.get_packages_installed()
        if packages_installed_list_of_dicts is None:
            return False
        version = PipCmd.version()
        if not version:
            return False
        checked = PipCmd.pip_check()
        if not checked:
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
