#
# -*- coding: utf-8 -*-
#
import time
import os

from database import Database, PyPi
from release_filter import ReleaseFilter
from pip_cmd import PipCmd, PipReturn
from pypi_cmd import PyPiCmd
from utils import Utils
from version import Version


class EnvCmd:

    @staticmethod
    def env_calc_levels(db: Database, cycles: [str]) -> bool:
        keys = db.packages_get_names_all()
        print('Check levels for {} packages'.format(len(keys)))
        levels_max = 15
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
                    # if d == 'dedupe':
                    #    if needed_below >= 14 and found_below == needed_below - 1:
                    #        # nasty hack for cyclical dependencies, which are otherwise hard to detect
                    #        cyclical = True
                #
                # need for fix
                #
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
            return False
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
        print('Get releases for {} packages'.format(len(packages_needed)))
        releases_dict = PyPiCmd.get_release_many(packages_needed)
        if releases_dict is None:
            return False
        # ok = True
        i = 0
        for package_name in packages_needed:
            release_dict = releases_dict[i]
            if release_dict is None:
                print('Error: No release_dict for {}'.format(package_name))
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

            self_check = True
            if self_check:
                rr = db.package_get_releases_recent(package_name, release_filter=ReleaseFilter.REGULAR)
                if rr is None:
                    return False  # not sure, if this really should be fatal ...
            i += 1
        return True  # should be: ok

    @staticmethod
    def env_check_consistency(db: Database) -> bool:
        keys = db.packages_get_names_all()
        print('Testing consistency of {} packages'.format(len(keys)))
        packages_needed = set()
        for name in keys:
            needed = db.package_get_requires(name) + db.package_get_required_by(name)
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
        required_by = dict()
        for package in packages_installed_list_of_dicts:
            requires = package.get(Database.REQUIRES)
            if requires is None:
                continue
            package_name = package.get(PyPi.PACKAGE_NAME)
            key_name = Utils.canonicalize_name(package_name)
            for req in requires:
                required = req.get(PyPi.PACKAGE_NAME)
                # print(key_name, ' -> ', required)
                s = required_by.get(required)
                if s is None:
                    s = required_by[required] = set()
                s.add(key_name)
            # for
        # for
        # print(required_by)
        for package in packages_installed_list_of_dicts:
            package_name = package.get('package_name')
            key_name = Utils.canonicalize_name(package_name)
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
        conflicts = PipCmd.get_conflicts(tree, verbose=True)
        cycles = PipCmd.get_cycles(tree, verbose=True)
        if len(conflicts) > 0:
            if not force:
                return False
            # continue despite conflicts !!!
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
            installed_packages = [Utils.canonicalize_name(p.get('package_name')) for p in
                                  packages_installed_list_of_dicts]
            for p in packages:
                if p not in installed_packages:
                    print('Deleting orphan: {}'.format(p))
                    if not db.package_remove(p):
                        return False

        for p in packages:
            # probably not needed any more !!
            level = db.package_get_level(p)
            if level >= 0:
                continue
            rr = db.package_get_releases_recent(p, release_filter=ReleaseFilter.REGULAR)
            if rr is not None:
                continue
            if not db.package_remove(p):
                return False
        # for

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
        develop = True
        if develop and os.path.exists(db_name):
            db.load(db_name)

        # the following is needed upon package updates
        if not EnvCmd.env_packages_tree(db=db):
            return False

        # this only affects the releases on PYPI - is needed, but could lag hours or a day
        if not EnvCmd.env_get_releases(db, force):  # could be done in parallel to other work
            return False

        ok = True if db.dump(json_path=db_name) else False
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
        debug_helper = False
        debug_already_latest = False
        updated = dict()

        for it in range(1, max_iterations + 1):
            print('upd_all: {} .. {}/{}: start'.format(env_name, it, max_iterations))
            level = 0
            stop = False
            while level < 100:
                level += 1
                pip_checked = False
                print('upd_all: {} .. {}/{}: {}: start'.format(env_name, it, max_iterations, level))
                packages = db.packages_get_names_by_level(level=level, less_then=False)
                if packages is None or len(packages) < 1:
                    break
                update_command = False
                for package in packages:
                    # for package, collect all the constraints in tree, try to improve to most recent
                    if debug_helper and package != 'numpy':  # only debug catch
                        continue
                    version_required = db.package_get_version_required(package)
                    releases_recent = None
                    for rf in ReleaseFilter:
                        releases_recent = db.package_get_releases_recent(package, release_filter=rf)
                        if releases_recent and len(releases_recent) > 0:
                            break
                    # for

                    if releases_recent is None or len(releases_recent) < 1:
                        print('upd_all: {} .. {}/{}: {}: {}: {} no recent releases ?? (error !!)'
                              .format(env_name, it, max_iterations, level, package, version_required))
                        # this really is an error condition
                        continue
                    release_recent = releases_recent[0]

                    v_required = Version.convert(version_required)
                    v_recent = Version.convert(release_recent)

                    if v_required >= v_recent:
                        # if package already uptodate, ignore it
                        if debug_already_latest:
                            print('upd_all: {} .. {}/{}: {}: {}: {} already latest'
                                  .format(env_name, it, max_iterations, level, package, version_required))
                        continue
                    # fi
                    releases_more = [r for r in releases_recent if Version.convert(r) > v_required]
                    releases_newer = releases_more[:releases_max]
                    constraints = db.packages_get_contraints(package=package)
                    # take releases, and check all conditions, sub-conditions on them, then take newest
                    releases_update = constraints.match_possible_releases(package, releases_newer)
                    if releases_update is None:
                        continue  # error
                    if len(releases_update) < 1:
                        # constraints prohibit update of package
                        print('upd_all: {} .. {}/{}: {}: {}: {} .. {} not for: {}'
                              .format(env_name, it, max_iterations, level, package, version_required,
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
                    if ruN > 2:  # simulate divide and conquer
                        releases_update = [releases_update[int(ruN / 2)]]

                    print('upd_all: {} .. {}/{}: {}: {}: {} .. update candidates: {}'
                          .format(env_name, it, max_iterations, level, package, version_required, releases_update))
                    for release_best in releases_update:
                        print('upd_all: {} .. {}/{}: {}: {}: {} .. {} -> {}'
                              .format(env_name, it, max_iterations, level, package, version_required,
                                      constraints, release_best))
                        print('upd_all: {} .. {}/{}: {}: {}: {} .. attempt to update (from {})'
                              .format(env_name, it, max_iterations, level, package, release_best, version_required))
                        pr = PipCmd.pip_install(package=package, version=release_best)
                        installed = pr.get_installed()
                        if pr.get_return_code() == PipReturn.OK:
                            # first try succeeded !   if more than current package was installed, update db !!
                            for pack in installed.keys():
                                # affected_set.add(pack)
                                vers = installed[pack]
                                updated[pack] = vers
                                print('Installed: {}=={}'.format(pack, vers))
                            # for
                            break
                        uninstalled = pr.get_uninstalled()
                        if len(installed) < 1 and len(uninstalled) < 1:
                            # nothing happened - we could not install - TODO: lock it or take note
                            print('nothing installed, nothing uninstalled ..')
                            continue
                        # failure case
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
                        print('upd_all: {} .. {}/{}: {}: {}: attempt to revert to: {}'
                              .format(env_name, it, max_iterations, level, package, pip_cmds))
                        pr2 = PipCmd.pip_install_commands(package, pip_cmds)
                        if pr2.get_return_code() == PipReturn.OK:
                            # repair succeeded, try next release_update, if any
                            print('upd_all: {} .. {}/{}: {}: {}: revert succeeded: {}'
                                  .format(env_name, it, max_iterations, level, package, pip_cmds))
                            continue
                        # fi
                        # now what, we tried candidate and the repair failed
                        print('upd_all: {} .. {}/{}: {}: {}: revert FAILED: {}'
                              .format(env_name, it, max_iterations, level, package, pip_cmds))
                        stop = True
                        break
                    # for best
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

            print('upd_all: {} .. {}/{}: end'.format(env_name, it, max_iterations))
            if stop:
                print('upd_all: {} .. {}/{}: stop !'.format(env_name, it, max_iterations))
                break
            # fi
        # for iteration
        items = updated.items()
        if len(items) > 0:
            for pack, vers in items:
                print('Updated: {}=={}'.format(pack, vers))
        else:
            print('No updates')
        ok = True if db.dump(json_path=db_name) else False
        db.close()
        return ok
