#
# -*- coding: utf-8 -*-
#
import sys
import subprocess
import typing
import itertools

from pip._vendor import pkg_resources  # keep this as compromise. it is hard to work around this.

# installed packages
try:
    # attempt new version
    from _vendor.pipdeptree_2_11_0._models.dag import PackageDAG
    from _vendor.pipdeptree_2_11_0._validate import conflicting_deps, render_conflicts_text, cyclic_deps
except:
    # fallback to old one ..
    from _vendor.pipdeptree import PackageDAG, conflicting_deps, render_conflicts_text, cyclic_deps

# own imports
from utils import Utils


class PipReturn:
    OK = 0
    ERROR = 1
    ROLLED_BACK = 2
    NO_ACTION = 3

    def __init__(self):
        self.return_code = PipReturn.OK
        self.installed = dict()
        self.uninstalled = dict()
        self.would_install = dict()
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

    def get_would_install(self) -> dict:
        return self.would_install

    def add_would_install(self, package, version) -> bool:
        self.would_install[package] = version
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

        #
        # also derive pseudo requirements here, and keep it/return
        #

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
        #
        #
        for p in pkgs:
            pkg = p.render_as_root(frozen=False)
            line0 = '* {}'.format(pkg)
            lines.append(line0)
            for req in conflicts[p]:
                req_str = req.render_as_branch(frozen=False)
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
    def pip_install_commands(packages_with_versions: typing.List, dry_run: bool = False) -> PipReturn:
        def has_digit(s: str):
            return any(i.isdigit() for i in s)

        def split_package_version(package_with_version: str) -> (str, str):
            s = package_with_version.rsplit('-', maxsplit=1)
            if s is None or len(s) < 2:
                return '', ''
            pack = s[0]
            vers = s[1]
            if not has_digit(vers):
                print('pip_install_error: {}'.format(mingled))  # fatal internal error !!
            pack2 = Utils.canonicalize_name(pack)
            return pack2, vers

        pr = PipReturn()  # installs=packages_with_versions)
        try:
            error = False
            pip_args = [sys.executable, '-m', 'pip', '--verbose', 'install']
            attempt_ssl_fix = True
            if attempt_ssl_fix:
                pip_args += ['--trusted-host=pypi.python.org',
                             '--trusted-host=pypi.org',
                             '--trusted-host=files.pythonhosted.org']
            if dry_run:
                pip_args += ['--dry-run']
            pip_args += packages_with_versions
            cp = subprocess.run(pip_args, shell=False, capture_output=True)
            for line in cp.stdout.decode().split('\n'):
                if not line:
                    continue
                pr.add_stdout_line(line)
                v = line.split()
                if v is None or len(v) < 2:
                    continue
                show_stdout = False
                if v[0] == 'Successfully' and (v[1] == 'installed' or v[1] == 'uninstalled'):
                    show_stdout = True
                    for i in range(2, len(v)):
                        pack2, vers = split_package_version(v[i])
                        if v[1] == 'installed':
                            pr.add_installed(pack2, vers)
                            show_stdout = False
                        elif v[1] == 'uninstalled':
                            pr.add_uninstalled(pack2, vers)
                            show_stdout = False
                        # fi
                    # for
                elif v[0] == 'Would' and v[1] == 'install':
                    for i in range(2, len(v)):
                        pack2, vers = split_package_version(v[i])
                        pr.add_would_install(pack2, vers)
                    # for
                # fi
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
                    # Todo: Handle: 'ERROR: Could not install packages due to an OSError: HTTPSConnectionPool...'
                    #       in above case we basically need to stop and fix the SSL error first, none will succeed !!
                    # TODO: Handle: 'ERROR: No matching distribution found for box2d==2.3.10'
                    if len(v) >= 7 and v[1] == 'No' and v[2] == 'matching':
                        mingled = v[6]
                        s = mingled.split('==')
                        pack = s[0]
                        vers = s[1] if len(s) > 1 else ''
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
            print('Failed: pip install {}: {}'.format(packages_with_versions, e))
        return pr.set_return_code(PipReturn.ERROR)

    @staticmethod
    def pip_install_single(package_name: str, version: str, eq: str = '==') -> PipReturn:
        package_with_version = '{}{}{}'.format(package_name, eq, version)
        return PipCmd.pip_install_commands(packages_with_versions=[package_with_version])

    @staticmethod
    def pip_install_roll_back_single(package_name: str, version: str) -> PipReturn:
        pr = PipCmd.pip_install_single(package_name=package_name, version=version)
        if pr.get_return_code() == PipReturn.OK:
            return pr
        installed = pr.get_installed()
        uninstalled = pr.get_uninstalled()
        if len(installed) < 1 and len(uninstalled) < 1:
            pr.set_return_code(PipReturn.NO_ACTION)
            return pr
        #
        # immediate failure case
        packages_with_versions = list()
        for pack in uninstalled.keys():
            vers = uninstalled[pack]
            cmd = '{}=={}'.format(pack, vers)
            print('Uninstalled: {}'.format(cmd))
            packages_with_versions.append(cmd)
        # for
        for pack in installed.keys():
            # affected_set.add(pack)
            vers = installed[pack]
            print('Installed: {}=={}'.format(pack, vers))
        # for
        print('pip_install_roll_back: attempt to revert: {} to: {}'
              .format(package_name, packages_with_versions))
        #
        # for the rollback, there could be time out situations in pip, therefore try a few times
        #
        pr2 = None  # silence warning
        t_max = 3
        for t in range(1, t_max + 1):
            pr2 = PipCmd.pip_install_commands(packages_with_versions=packages_with_versions)
            if pr2.get_return_code() == PipReturn.OK:
                # repair succeeded, try next release_update, if any
                print('pip_install_roll_back: revert {}: succeeded: {}'
                      .format(package_name, packages_with_versions))
                # rolled back
                pr2.set_return_code(PipReturn.ROLLED_BACK)
                return pr2
            # fi
            # now what, we tried candidate and the repair failed
            print('pip_install_roll_back: revert {}: FAILED: {} .. {}/{}'
                  .format(package_name, packages_with_versions, t, t_max))
        # for
        pr2.set_return_code(PipReturn.ERROR)
        # failed roll back
        return pr2

    @staticmethod
    def pip_list(self) -> dict:

        # build a requirement from it in scripts export

        '''
        import subprocess
        import sys

        def pip_list():
            args = [sys.executable, "-m", "pip", "list"]
            p = subprocess.run(args, check=True, capture_output=True)
            return p.stdout.decode()

        print(pip_list())

        :return:
        '''
        return None

    @staticmethod
    def pip_freeze(output_path: str) -> bool:
        ok = True
        try:
            with open(output_path, 'w') as file:
                output = subprocess.check_output(['pip', 'freeze'])
                for line in output.splitlines():
                    file.write(line.decode() + '\n')
                # for
            # with
        except:
            ok = False
        if not ok:
            print('Failed: pip freeze')
        return ok

    @staticmethod
    def pip_selftest() -> bool:
        version = PipCmd.version()
        if not version:
            return False
        # PipCmd.pip_freeze('test_freeze.txt')

        check = True  # should be True
        if check:
            checked = PipCmd.pip_check()
            if not checked:
                return False
        else:
            pass
        return True


def main():
    if not PipCmd.pip_selftest():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
