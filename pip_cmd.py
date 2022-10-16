#
# -*- coding: utf-8 -*-
#
import sys
import subprocess
import typing
import itertools
import pkg_resources

# installed packages
from _vendor.pipdeptree import PackageDAG, conflicting_deps, render_conflicts_text, cyclic_deps

# own imports
from utils import Utils


class PipReturn:
    OK = 0
    ERROR = 1
    ROLLED_BACK = 2
    NO_ACTION = 3

    def __init__(self, package: str, installs: typing.List):
        self.package = package
        self.installs = installs
        self.return_code = PipReturn.OK
        self.installed = dict()
        self.uninstalled = dict()
        self.no_matching_distribution = dict()
        self.stdout_lines = list()
        self.stderr_lines = list()
        return

    def get_return_code(self) -> int:
        return self.return_code

    def set_return_code(self, return_code: int) -> 'PipReturn':
        self.return_code = return_code
        return self

    def add_no_matching_distribution(self, package, version) -> bool:
        self.no_matching_distribution[package] = version
        return True

    def get_installed(self) -> dict:
        return self.installed

    def add_installed(self, package, version) -> bool:
        self.installed[package] = version
        return True

    def get_uninstalled(self) -> dict:
        return self.uninstalled

    def add_uninstalled(self, package, version) -> bool:
        self.uninstalled[package] = version
        return True

    def add_stdout_line(self, line: str) -> bool:
        self.stdout_lines.append(line)
        return True

    def add_stderr_line(self, line: str) -> bool:
        self.stderr_lines.append(line)
        return True


class PipCmd:

    @staticmethod
    def process_tree(tree: PackageDAG, truncate: bool = False) -> typing.List:
        """Converts the tree into a nested representation.
        """

        def aux(node, parent=None, chain=None):
            if chain is None:
                chain = [node.project_name]
            d = node.as_dict()
            if parent:
                if node.version_spec:
                    d['required_version'] = node.version_spec
                else:
                    d.pop('required_version')  # do not need 'Any'
            else:
                d['required_version'] = d['installed_version']
            requires = [
                aux(c, parent=node, chain=chain + [c.project_name])
                for c in tree.get_children(node.key)
                if c.project_name not in chain
            ]
            if len(requires) > 0:
                d['requires'] = requires
            # fi
            d['version_installed'] = d.pop('installed_version')  # rename
            if d.get('required_version') is not None:
                d['version_required'] = d.pop('required_version')  # rename
            d.pop('key')
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
        return out_nodes

    @staticmethod
    def get_tree_installed() -> typing.Union[PackageDAG, typing.Any]:
        print('Getting installed distributions ..')
        pkg_resources.working_set.__init__()
        pkgs = [d for d in pkg_resources.working_set]
        try:
            print('Converting installed distributions to tree ..')
            # this takes quite a while !!
            tree = PackageDAG.from_pkgs(pkgs)
        except Exception as e:
            print('Failed with tree: {}'.format(e))
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
        # test case for this, toggle:
        #     pip install charset-normalizer==1.4.1
        #     pip install charset-normalizer~=2.0.0
        try:
            cp = subprocess.run([sys.executable, '-m', 'pip', 'check'], shell=False, capture_output=True)
            for line in cp.stdout.decode().split('\n'):
                if not line:
                    continue
                v = line.split()
                if cp.returncode == 0:
                    # first and only line typically
                    if v[0] == 'No' and v[1] == 'broken':
                        return True
                else:
                    # could be multiple lines, need to investigate further, like
                    # 'requests 2.28.0 has requirement charset-normalizer~=2.0.0, but you have charset-normalizer 1.4.1.'
                    print('pip_check: {}'.format(line))
            # for
            if cp.returncode != 0:
                return False

        except Exception as e:
            print('Failed: pip check: {}'.format(e))
        return False

    @staticmethod
    def pip_install_commands(package: str, args: typing.List) -> PipReturn:
        def has_digit(s: str):
            return any(i.isdigit() for i in s)

        pr = PipReturn(package=package, installs=args)
        try:
            error = False
            pip_args = [sys.executable, '-m', 'pip', 'install'] + args
            cp = subprocess.run(pip_args, shell=False, capture_output=True)
            for line in cp.stdout.decode().split('\n'):
                if not line:
                    continue
                pr.add_stdout_line(line)
                v = line.split()
                if v is None or len(v) < 2:
                    continue
                if v[0] != 'Successfully' or (v[1] != 'installed' and v[1] != 'uninstalled'):
                    continue
                show_stdout = True
                for i in range(2, len(v)):
                    mingled = v[i]
                    s = mingled.rsplit('-', maxsplit=1)
                    if s is None or len(s) < 2:
                        continue
                    pack = s[0]
                    vers = s[1]
                    if not has_digit(vers):
                        print('pip_install_error: {}'.format(mingled))  # fatal internal error !!
                    pack2 = Utils.canonicalize_name(pack)
                    if v[1] == 'installed':
                        pr.add_installed(pack2, vers)
                        show_stdout = False
                    elif v[1] == 'uninstalled':
                        pr.add_uninstalled(pack2, vers)
                        show_stdout = False
                    # fi
                # for
                if show_stdout:
                    print('pip_install_stdout: {}'.format(line.lstrip()))
            # for stdout
            for line in cp.stderr.decode().split('\n'):
                if not line:
                    continue
                pr.add_stderr_line(line)
                v = line.split()
                if v is None or len(v) < 1:
                    continue
                if v[0] == 'ERROR:':
                    error = True
                    # TODO: Handle: 'ERROR: No matching distribution found for box2d==2.3.10'
                    if len(v) >= 7 and v[1] == 'No' and v[2] == 'matching':
                        mingled = v[6]
                        s = mingled.split('==')
                        pack = s[0]
                        vers = s[1]
                        pack2 = Utils.canonicalize_name(pack)
                        pr.add_no_matching_distribution(pack2, vers)
                    # fi
                # fi
                if len(v) > 2 and v[2] == 'requires':
                    error = True
                # also trace:
                # ERROR: Could not find a version that satisfies the requirement box2d==2.3.10 (from versions: 2.0.2b1, 2.3b0, 2.3.2)
                # ERROR: No matching distribution found for box2d==2.3.10
                # and FIX it !!
                print('pip_install_stderr: {}'.format(line))
            # for stderr
            if cp.returncode != 0 or error:
                return pr.set_return_code(PipReturn.ERROR)
            return pr.set_return_code(PipReturn.OK)

        except Exception as e:
            # typically a coding error above
            print('Failed: pip install {}: {}'.format(args, e))
        return pr.set_return_code(PipReturn.ERROR)

    @staticmethod
    def pip_install(package: str, version: str, eq: str = '==') -> PipReturn:
        arg = '{}{}{}'.format(package, eq, version)
        return PipCmd.pip_install_commands(package, [arg])

    @staticmethod
    def pip_install_roll_back(package: str, version: str) -> PipReturn:
        pr = PipCmd.pip_install(package=package, version=version)
        # installed = pr.get_installed()
        if pr.get_return_code() == PipReturn.OK:
            return pr
        installed = pr.get_installed()
        uninstalled = pr.get_uninstalled()
        if len(installed) < 1 and len(uninstalled) < 1:
            pr.set_return_code(PipReturn.NO_ACTION)
            return pr
        #
        # immediate failure case
        for pack in installed.keys():
            # affected_set.add(pack)
            vers = installed[pack]
            print('Installed: {}=={}'.format(pack, vers))
        # for
        pip_cmds = list()
        for pack in uninstalled.keys():
            vers = uninstalled[pack]
            cmd = '{}=={}'.format(pack, vers)
            print('Uninstalled: {}'.format(cmd))
            pip_cmds.append(cmd)
        # for
        print('pip_install_roll_back: attempt to revert: {} to: {}'
              .format(package, pip_cmds))
        pr2 = PipCmd.pip_install_commands(package, pip_cmds)
        if pr2.get_return_code() == PipReturn.OK:
            # repair succeeded, try next release_update, if any
            print('pip_install_roll_back: revert {}: succeeded: {}'
                  .format(package, pip_cmds))
            # rolled back
            pr2.set_return_code(PipReturn.ROLLED_BACK)
            return pr2
        # fi
        # now what, we tried candidate and the repair failed
        print('pip_install_roll_back: revert {}: FAILED: {}'
              .format(package, pip_cmds))
        pr2.set_return_code(PipReturn.ERROR)
        # failed roll back
        return pr2

    @staticmethod
    def pip_test_install() -> bool:
        #
        # hand crafted example, which WILL CHANGE over time - use with care !!
        #
        # bad command first
        return False  # needs to be reworked below
        ok = PipCmd.pip_install(package='charset-normalizer', version='1.4.1')
        if ok:
            return False
        if PipCmd.pip_check():
            return False
        # good command next
        ok = PipCmd.pip_install(package='charset-normalizer', eq='~=', version='2.0.0')
        if not ok:
            return False
        if not PipCmd.pip_check():
            return False
        return True

    @staticmethod
    def pip_selftest() -> bool:
        version = PipCmd.version()
        if not version:
            return False

        check = True  # should be True
        if check:
            checked = PipCmd.pip_check()
            if not checked:
                return False
        else:
            # use with care !!
            if not PipCmd.pip_test_install():
                return False

        return True


def main():
    if not PipCmd.pip_selftest():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
