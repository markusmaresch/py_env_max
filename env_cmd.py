#
# -*- coding: utf-8 -*-
#
import time
import typing

from database import Database, PyPi
from release_filter import ReleaseFilter
from pip_cmd import PipCmd, PipReturn
from pypi_cmd import PyPiCmd
from utils import Utils
from version import Version


class PackageStack:
    def __init__(self):
        self.stack = list()
        return

    def len(self) -> int:
        return len(self.stack)

    def format_full(self, tup: typing.Tuple) -> str:
        if not tup[1]:
            return tup[0]
        return '{}=={}'.format(tup[0], tup[1])

    def __repr__(self) -> str:
        ll = self.len()
        if ll < 1:
            return 'empty'
        s = ''
        for tup in self.stack:
            add = self.format_full(tup)
            if not s:
                s = (str(ll) + ' ' + add)
            else:
                s += (' ' + add)
        return s

    def append(self, package_name: str, version: str) -> bool:
        if self.len() > 0:
            i = (-1)
            for opn, ov in self.stack:
                i += 1
                if opn != package_name:
                    continue
                if ov == version:
                    # print('stack: ignore identical: ', package_name, version)
                    return True
                if not ov and version:
                    # print('stack: version update: ', package_name, version)
                    self.stack[i] = (package_name, version)
                    return True
                # fi
                # what to do ??
                print('stack: ', package_name, ov, version)
                break
            # for
        # fi
        tup = (package_name, version)
        self.stack.append(tup)
        return True

    def has_package(self, package_name: str) -> bool:
        for pn, v in self.stack:
            if pn == package_name:
                return True
        return False

    @staticmethod
    def get_components(pwv: str) -> typing.Tuple[str, str]:
        s = pwv.split('==')
        if s is None:
            return '', ''
        package_name = s[0]
        version = s[1] if len(s) > 1 else ''
        return package_name, version

    @staticmethod
    def get_package_name(pwv: str) -> str:
        package_name, _ = PackageStack.get_components(pwv)
        return package_name

    def extend_full(self, packages_with_versions: typing.List[str]) -> bool:
        for pwv in packages_with_versions:
            package_name, version = PackageStack.get_components(pwv)
            if not self.append(package_name, version):
                return False
            print('extend_full', package_name, self.len())
        # for
        return True

    def pop_full(self) -> str:
        tup = self.stack.pop()
        return self.format_full(tup)

    def pop_discard(self):
        self.stack.pop()


class EnvCmd:

    @staticmethod
    def env_calc_levels(db: Database, cycles: typing.List[str]) -> bool:
        keys = db.packages_get_names_all()
        print('Check levels for {} packages'.format(len(keys)))
        levels_max = 20
        level = 0
        lod = keys
        while True:
            level += 1
            if level >= levels_max:
                break
            if len(lod) < 1:
                break
            next_lod = list()
            for d in lod:
                dependencies = db.package_get_requires(name=d)
                if level == 1:
                    if len(dependencies) < 1:
                        db.package_set_level(name=d, level=level)
                        continue
                    # fi
                    next_lod.append(d)
                    continue
                # fi
                # level > 1
                found_below = 0
                needed_below = len(dependencies)
                for dep in dependencies:
                    ll = db.package_get_level(dep)
                    if ll < 0:
                        continue
                    if ll < level:
                        found_below += 1
                # for
                #
                # need for fix .. have cyclicals already
                #
                cyclical = False
                satisfied = (found_below >= needed_below)
                if not satisfied:
                    if cycles is not None and d in cycles:
                        cyclical = True

                if satisfied or cyclical:
                    db.package_set_level(name=d, level=level)
                else:
                    next_lod.append(d)
            # for
            del lod
            lod = next_lod
        # while
        if len(lod) > 0:
            print('')
            print('Did NOT resolve all packages below')
            for p in lod:
                # not entirely correct !!
                dependencies = db.package_get_requires(p)
                print('  {} {}'.format(p, dependencies))
            print('Did NOT resolve all packages above (could be cyclical behavior)')
            print('')
            # return False # this can happen for os/system crossing attempts, should not be fatal
        return True

    @staticmethod
    def env_get_releases(db: Database, force: bool = False) -> bool:
        uptodate_minutes = 10 * 60  # was 5 minutes, can be an hour at least, or a day
        uptodate_seconds = uptodate_minutes * 60
        keys = db.packages_get_names_all()
        print('Check releases for {} packages (force={})'.format(len(keys), force))
        now = int(time.time())
        packages_needed = list()
        oldest = 0
        p_oldest = None
        for package_name in keys:
            t = db.package_get_releases_checked_time(package_name)
            diff = (now - t) if t > 0 else 9999999
            if oldest < diff:
                p_oldest = package_name
                oldest = diff
            if force or diff > uptodate_seconds:
                packages_needed.append(package_name)
        # for
        if len(packages_needed) < 1:
            print('All packages uptodate ({} within {} of {} seconds) for releases ...'
                  .format(p_oldest, oldest, uptodate_seconds))
            return True
        ok = True
        packages_resolved = set()
        t_max = 5
        for t in range(t_max):
            print('Get releases for {} packages'.format(len(packages_needed)))
            releases_dict = PyPiCmd.get_release_many(packages_needed)
            if releases_dict is None:
                return False
            # could have still open releases
            ok = True
            i = (-1)
            for package_name in packages_needed:
                i += 1
                release_dict = releases_dict[i]
                if release_dict is None:
                    #
                    # conceptual bug for wheel installed packages, that are not on pypi.org
                    # TODO: need to fix release resolution otherwise - right now band aid it with 'force'
                    #
                    print('Error: No release_dict for {}'.format(package_name))
                    ok = False
                    continue
                releases = release_dict.get(Database.RELEASES_RECENT)
                if releases is None:
                    print('Error: No releases for {}'.format(package_name))
                    continue
                if not db.package_set_releases_recent(package_name, releases, now):
                    return False
                summary = release_dict.get(Database.SUMMARY)
                if summary is not None:
                    if not db.package_set_summary(package_name, summary):
                        return False

                pypi_package = release_dict.get(Database.PYPI_PACKAGE)
                if pypi_package is not None and not pypi_package:
                    # no testing for now ..
                    if not db.pypi_package_set(package_name, False):
                        return False
                else:
                    if not db.pypi_package_set(package_name, True):
                        return False
                    self_check = True
                    if self_check:
                        rr = db.package_get_releases_recent(package_name, release_filter=ReleaseFilter.REGULAR)
                        if rr is None:
                            return False  # not sure, if this really should be fatal ...
                packages_resolved.add(package_name)
            # for
            if ok:
                if t > 0:
                    print('Finally worked ..')
                break
            packages_needed = [p for p in packages_needed if p not in packages_resolved]
            print('Packages resolved: {}'.format(len(packages_resolved)))
            print('Packages needed:   {}'.format(len(packages_needed)))
            print('Need to try again ..')
        # for t
        return ok

    @staticmethod
    def env_check_consistency(db: Database) -> bool:
        keys = db.packages_get_names_all()
        print('Testing consistency of {} packages'.format(len(keys)))
        packages_needed = set()
        for name in keys:
            needed = db.package_get_requires(name)  # + db.package_get_required_by(name)
            if needed is None:
                continue
            for package_raw in needed:
                package = Utils.canonicalize_name(package_raw)
                if package != package_raw:
                    print('Canonicalize2 before: {}'.format(package_raw))
                    return False
                packages_needed.add(package)
        # for
        print('Found {} depending packages'.format(len(packages_needed)))
        missing = 0
        for name in packages_needed:
            if name in keys:
                continue
            print('  Not found: {} ?'.format(name))
            missing += 1
        # for
        print('Missing depending packages: {}'.format(missing))
        return True

    @staticmethod
    def calc_required_by(db: Database, packages_installed_list_of_dicts) -> bool:
        #
        # from requires, reverse the pointer logic and calculate required_by efficiently
        #
        print('Calculating required_by ..')
        installed_packages_list = [Utils.canonicalize_name(p.get(PyPi.PACKAGE_NAME)) for p in
                                   packages_installed_list_of_dicts]
        installed_packages_set = set(installed_packages_list)  # set is better than list !
        required_by = dict()
        for package in packages_installed_list_of_dicts:
            requires = package.get(Database.REQUIRES)
            if requires is None:
                continue
            package_name = package.get(PyPi.PACKAGE_NAME)
            key_name = Utils.canonicalize_name(package_name)
            if key_name not in installed_packages_set:
                continue  # does not seem to trigger, even if we had orphans
            for req in requires:
                required = req.get(PyPi.PACKAGE_NAME)
                # print(key_name, ' -> ', required)
                s = required_by.get(required)
                if s is None:
                    required_by[required] = set()
                    s = required_by[required]
                s.add(key_name)
            # for
        # for
        # print(required_by)
        for package in packages_installed_list_of_dicts:
            package_name = package.get(PyPi.PACKAGE_NAME)
            key_name = Utils.canonicalize_name(package_name)
            if key_name not in installed_packages_set:
                continue  # does not seem to trigger, even if we had orphans
            rb_set = required_by.get(key_name)
            if rb_set is None:
                continue
            rb_sorted_list = list(sorted(rb_set))
            if not db.package_set_required_by(key_name, rb_sorted_list):
                return False
        # for
        return True

    @staticmethod
    def env_packages_tree(db: Database, force: bool = False) -> bool:
        tree = PipCmd.get_tree_installed()
        if tree is None:
            return False
        conflicts = PipCmd.get_conflicts(tree, verbose=True)
        if len(conflicts) > 0:
            # could also indicate a broken environment
            print('pip check, because we had cycles')
            ok = PipCmd.pip_check()
            if not ok:
                if not force:
                    print('Fix issues first !!')
                    return False
                print('continue despite conflicts !!!')
            else:
                print('pip check: ok')
            # fi
        # fi
        cycles = PipCmd.get_cycles(tree, verbose=True)
        if len(cycles) > 0:
            # have a list of known cycles, and ignore them
            pass

        packages_installed_list_of_dicts = PipCmd.process_tree(tree)
        del tree
        if not db.packages_set(packages_installed_list_of_dicts):
            return False

        # need to check for orphaned packages: no recent_releases, no level
        packages = db.packages_get_names_all()
        if len(packages_installed_list_of_dicts) < len(packages):
            installed_packages = [Utils.canonicalize_name(p.get(PyPi.PACKAGE_NAME)) for p in
                                  packages_installed_list_of_dicts]
            had_orphans = False
            for p in packages:
                if p in installed_packages:
                    continue
                #
                # this could indicate, that the json is ahead and the current env
                # does not contain all the packages
                #
                print('Deleting orphan: {}'.format(p))
                if not db.package_remove(p):
                    return False
                had_orphans = True
            # for
            if had_orphans:
                print('Might have to install packages above .. ??')
            # fi
        # fi

        if not EnvCmd.calc_required_by(db, packages_installed_list_of_dicts):
            return False
        if not EnvCmd.env_check_consistency(db):
            return False
        if not EnvCmd.env_calc_levels(db, cycles=cycles):
            return False
        return True

    @staticmethod
    def env_import(env_name: str, force: bool = False) -> bool:
        # read existing environment and store in internal database
        db_name = '{}.json'.format(env_name)
        print('env_import: {} (force={})'.format(env_name, force))
        db = Database()

        load_db = True  # set to False only for init db bug hunting
        if load_db:
            db.load(db_name, verbose=False)  # could fail

        # the following is needed upon package updates
        if not EnvCmd.env_packages_tree(db=db, force=force):
            print('env_import: {} (force={}) .. env_packages_tree failed'.format(env_name, force))
            return False

        # this only affects the releases on PYPI - is needed, but could lag hours or a day
        if not EnvCmd.env_get_releases(db, force):  # could be done in parallel to other work
            print('env_import: {} (force={}) .. env_get_releases failed'.format(env_name, force))
            if not force:
                return False

        ok = True if db.dump(json_path=db_name) else False
        db.close()
        return ok

    @staticmethod
    def install_stack(env_name: str, packages_with_versions: typing.List[str]) -> dict:
        updated_all = dict()
        stack = PackageStack()
        stack.extend_full(packages_with_versions)
        pip_checked = True  # set to False !!!!
        first = True
        while True:
            print('{}: stack: {}'.format(env_name, stack))
            if stack.len() < 1:
                break
            if first:
                pwvs = packages_with_versions
                current_package_name = ''
            else:
                popped_full = stack.pop_full()
                pwvs = [popped_full]
                current_package_name = PackageStack.get_package_name(popped_full)
            print('{}: pip install dry-run: {}'.format(env_name, pwvs))
            pip_error = PipReturn.OK
            pr = None
            for t in range(2):
                pr = PipCmd.pip_install_commands(packages_with_versions=pwvs, dry_run=True)
                pip_error = pr.get_return_code()
                if pip_error == PipReturn.OK:
                    break
            # for
            if pip_error == PipReturn.ERROR:
                print('pip error')
                # ok = False
                break
            # fi

            would_install = pr.get_would_install()
            if len(would_install) == 0:
                print('{}: nothing to do... {}'.format(env_name, current_package_name))
                # break
            elif len(would_install) == 1:
                package_name = next(iter(would_install))
                version = would_install[package_name]
                if not pip_checked:
                    print('{}: pip check'.format(env_name))
                    ok = PipCmd.pip_check()
                    if not ok:
                        break
                    pip_checked = True
                # fi
                print('{}: pip install should work: {} {}'.format(env_name, package_name, version))
                pr = PipCmd.pip_install_roll_back_single(package_name=package_name, version=version)
                if pr.get_return_code() == PipReturn.NO_ACTION:
                    print('{}: {} {} .. nothing installed, nothing uninstalled'
                          .format(env_name, package_name, version))
                else:
                    if pr.get_return_code() == PipReturn.OK:
                        installed = pr.get_installed()
                        # first try succeeded !   if more than current package was installed, update db !!
                        for pack in installed.keys():
                            vers = installed[pack]
                            updated_all[pack] = vers
                            print('{}: installed: {}=={}'.format(env_name, pack, vers))
                        # for
                    #
                #
                if pr.get_return_code() == PipReturn.ERROR:
                    ok = False
                    break
                # fi

                if first:
                    stack.pop_discard()
            else:
                # > 1
                print('{}: stack extend raw: {}'.format(env_name, would_install))
                for k in would_install.keys():
                    if k == current_package_name:
                        continue
                    print('{}: stack append: {} {}'.format(env_name, k, would_install[k]))
                    stack.append(k, would_install[k])
                # for
            # fi
            first = False
        # while
        return updated_all

    @staticmethod
    def unwrap_packages(packages_file_list: typing.List[str]) -> typing.Optional[typing.List[str]]:
        print(f'unwrap_packages: {packages_file_list})')
        try:
            #
            # this should be split by levels, so we do not incur dependencies (at least try)
            # turn this into a generator
            # or slower - do this one by one
            #
            lines = list()
            last0 = 'a'
            for i in range(len(packages_file_list)):
                with open(packages_file_list[i], 'r') as file:
                    for line in file:
                        line_stripped = line.strip()
                        if not line_stripped or line_stripped == 'end':
                            break
                        c0 = line_stripped[0]
                        if c0 < last0:
                            print(f'detected change level - call again: {c0} < {last0}')
                            # break
                        last0 = c0
                        lines.append(line_stripped)
                    # for
                # with
            # for

            # because of the stack logic below !!
            inverted = list(reversed(lines))
            return inverted
        except:
            return None

    @staticmethod
    def install_packages(env_name: str,
                         packages_with_versions: typing.List[str],
                         packages_file_list: typing.List[str],
                         force: bool = False) -> bool:
        print('install_packages: {} (force={})'.format(env_name, force))
        flag_direct = (packages_with_versions is not None and len(packages_with_versions) > 0)
        flag_indirect = (packages_file_list is not None and len(packages_file_list) > 0)
        if not flag_direct and not flag_indirect:
            return False
        if force or True:
            # really, this should always be done
            if not EnvCmd.env_import(env_name=env_name, force=False):
                return False
        db_name = '{}.json'.format(env_name)
        db = Database()
        if not db.load(db_name):
            # alternatively could call env_import and continue
            return False
        # fi

        if flag_indirect:
            #
            # some logic cleanup needed here
            #
            packages_with_versions = EnvCmd.unwrap_packages(packages_file_list)
            if packages_with_versions is None or len(packages_with_versions) < 1:
                return False
        # fi

        ok = True
        updated_all = EnvCmd.install_stack(env_name, packages_with_versions)
        items = updated_all.items()
        if len(items) > 0:
            print()
            for pack, vers in items:
                print('{}: updated: {}=={}'.format(env_name, pack, vers))
            print()
            if not db.dump(json_path=db_name):
                ok = False
            #
            # this is a bit hacky - open db, import again, but not force ?
            #
            if not EnvCmd.env_import(env_name=env_name, force=False):
                ok = False
        else:
            print('{}: NO updates'.format(env_name))
        # fi

        ok = ok if db.dump(json_path=db_name) else False
        db.close()
        return ok

    @staticmethod
    def upd_all(env_name: str, force: bool = False) -> bool:
        # Attempt to update existing python environment
        max_iterations = 1
        print('upd_all: {} (force={}, max_iterations={})'.format(env_name, force, max_iterations))
        if not EnvCmd.env_import(env_name=env_name, force=False):
            return False

        db_name = '{}.json'.format(env_name)
        db = Database()
        if not db.load(db_name):
            # alternatively could call env_import and continue
            return False

        releases_max = 50  # no limit
        debug_already_latest = False
        updated_all = dict()
        stop = False

        for it in range(1, max_iterations + 1):
            print('upd_all: {} .. {}/{}: start'.format(env_name, it, max_iterations))
            level = 0
            # stop = False
            updated_iter = dict()
            while level < 100:
                if stop:
                    break
                level += 1
                pip_checked = False
                print('upd_all: {} .. {}/{}: {}: start'.format(env_name, it, max_iterations, level))
                packages = db.packages_get_names_by_level(level=level, less_then=False)
                if packages is None or len(packages) < 1:
                    break
                update_command = False
                for package_name in packages:
                    if stop:
                        break
                    #
                    version_required = db.package_get_version_required(package_name)
                    if package_name.startswith('torch'):  # only debug catch
                        pattern = '+cu1'
                        if pattern in version_required:
                            print('upd_all: {} .. {}/{}: {}: {}: {} NOT updating, pattern: {}'
                                  .format(env_name, it, max_iterations, level,
                                          package_name, version_required, pattern))
                            continue
                        # fi
                    # fi
                    releases_recent = None
                    for rf in ReleaseFilter:
                        releases_recent = db.package_get_releases_recent(package_name, release_filter=rf)
                        if releases_recent and len(releases_recent) > 0:
                            break
                        print('upd_all: {} .. {}/{}: {}: {}: {} need to open release filter after {}'
                              .format(env_name, it, max_iterations, level, package_name, version_required, rf.name))
                        continue
                    # for

                    if releases_recent is None or len(releases_recent) < 1:
                        print('upd_all: {} .. {}/{}: {}: {}: {} no recent releases ?? (error !!)'
                              .format(env_name, it, max_iterations, level, package_name, version_required))
                        # this really is an error condition
                        continue
                    release_recent = releases_recent[0]

                    v_required = Version.convert(version_required)
                    v_recent = Version.convert(release_recent)

                    if v_required >= v_recent:
                        # if package already uptodate, ignore it
                        if debug_already_latest:
                            print('upd_all: {} .. {}/{}: {}: {}: {} already latest'
                                  .format(env_name, it, max_iterations, level, package_name, version_required))
                        continue
                    # fi
                    releases_more = [r for r in releases_recent if Version.convert(r) > v_required]
                    releases_newer = releases_more[:releases_max]
                    constraints = db.packages_get_contraints(package_name=package_name)
                    # take releases, and check all conditions, sub-conditions on them, then take newest
                    releases_update = constraints.match_possible_releases(package_name, releases_newer)
                    if releases_update is None:
                        continue  # error
                    if len(releases_update) < 1:
                        # constraints prohibit update of package
                        print('upd_all: {} .. {}/{}: {}: {}: {} .. {} not for: {}'
                              .format(env_name, it, max_iterations, level,
                                      package_name, version_required,
                                      constraints, releases_newer[:8]))
                        continue
                    # fi

                    if not pip_checked:
                        # do this on demand, only if needed
                        print('upd_all: {} .. {}/{}: {}: pip check'
                              .format(env_name, it, max_iterations, level))
                        ok = PipCmd.pip_check()
                        if not ok:
                            break
                        pip_checked = True
                    # fi

                    ruN = len(releases_update)
                    st = 0  # (it - 1) % 2
                    if ruN > 24:  # simulate divide and conquer, do not thin too much !!
                        release_candidates = releases_update[st::4]
                    elif ruN > 16:
                        release_candidates = releases_update[st::3]
                    elif ruN > 8:
                        release_candidates = releases_update[st::2]
                    else:
                        release_candidates = releases_update

                    print('upd_all: {} .. {}/{}: {}: {}: {} .. update candidates: {}'
                          .format(env_name, it, max_iterations, level, package_name, version_required,
                                  release_candidates))
                    for release_best in release_candidates:
                        print('upd_all: {} .. {}/{}: {}: {}: {} .. {} -> {}'
                              .format(env_name, it, max_iterations, level, package_name, version_required,
                                      constraints, release_best))
                        print('upd_all: {} .. {}/{}: {}: {}: {} .. attempt to update (from {})'
                              .format(env_name, it, max_iterations, level, package_name, release_best,
                                      version_required))
                        pr = PipCmd.pip_install_roll_back_single(package_name=package_name, version=release_best)
                        if pr.get_return_code() == PipReturn.NO_ACTION:
                            # nothing happened - we could not install - TODO: lock it or take note
                            print('upd_all: {} .. {}/{}: {}: {}: {} .. nothing installed, nothing uninstalled'
                                  .format(env_name, it, max_iterations, level, package_name, release_best))
                            continue
                        if pr.get_return_code() == PipReturn.OK:
                            installed = pr.get_installed()
                            # first try succeeded !   if more than current package was installed, update db !!
                            for pack in installed.keys():
                                vers = installed[pack]
                                updated_all[pack] = vers
                                updated_iter[pack] = vers
                                print('upd_all: {} .. {}/{}: {}: {}: {} .. installed: {}=={}'
                                      .format(env_name, it, max_iterations, level,
                                              package_name, release_best, pack, vers))
                            # for
                            #
                            # this also stops upon the first success, could be more aggressive and try to get the latest
                            #
                            break
                        #
                        if pr.get_return_code() == PipReturn.ERROR:
                            print('upd_all: {} .. {}/{}: {}: {}: {} .. roll back failed !'
                                  .format(env_name, it, max_iterations, level,
                                          package_name, release_best))

                            stop = True
                            break
                        # fi
                        #
                        # could be ROLLED_BACK, that succeeded
                        #
                        # break
                    # for release_best
                    update_command = True
                # for packages

                # now have all updates for this level, if at all
                if not update_command:
                    print('upd_all: {} .. {}/{}: {}: done with possible updates'
                          .format(env_name, it, max_iterations, level))
                    if not stop:
                        continue

                if not stop and not PipCmd.pip_check():
                    stop = True  # what to do here, really ??
                    break

                if not EnvCmd.env_packages_tree(db=db, force=True):
                    stop = True
                    break
                if not db.dump(json_path=db_name):
                    stop = True

                print('upd_all: {} .. {}/{}: {}: end'.format(env_name, it, max_iterations, level))
                if stop:
                    print('upd_all: {} .. {}/{}: {}: stop !'.format(env_name, it, max_iterations, level))
                    break
                # fi
            # for level

            iter_updated = len(updated_iter.items())
            if iter_updated < 1:
                print('upd_all: {} .. {}/{}: no updates ..'.format(env_name, it, max_iterations))
                stop = True
            else:
                print('upd_all: {} .. {}/{}: {} updates'.format(env_name, it, max_iterations, iter_updated))

            print('upd_all: {} .. {}/{}: end'.format(env_name, it, max_iterations))
            if stop:
                print('upd_all: {} .. {}/{}: stop !'.format(env_name, it, max_iterations))
                break
            # fi

        # for iteration
        items = updated_all.items()
        if len(items) > 0:
            print()
            for pack, vers in items:
                print('Updated: {}=={}'.format(pack, vers))
            print()
        else:
            print('No updates')
        ok = True if db.dump(json_path=db_name) else False
        db.close()
        return ok
