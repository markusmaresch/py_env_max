#
# -*- coding: utf-8 -*-
#
import sys
import os
import time
import json
import typing
import difflib

#
# a bit akward - use pip and pipdeptree in order to get the currently
# installed package trees
#
from pip._internal.utils.misc import get_installed_distributions
from pipdeptree import PackageDAG


class LevelsCache:
    def __init__(self, levels_max: int):
        self.levels_max = levels_max
        self.level_dicts = [dict() for x in range(levels_max)]
        return

    def add(self, level: int, package: dict):
        d = self.level_dicts[level]
        key_lower = package['key'].lower()
        d[key_lower] = package
        return

    def find_below(self, level: int, package: dict) -> bool:
        key = package['key']
        for l in range(1, level):  # we should NOT search ALL levels
            d = self.level_dicts[l]
            if d.get(key):
                return True
        return False

    def find_level(self, key: str) -> int:
        key_lower = key.lower()
        for level in range(1, self.levels_max):
            d = self.level_dicts[level]
            if d.get(key_lower):
                return level
        return -1

    def show(self) -> bool:
        for l in range(1, self.levels_max):
            level_dict = self.level_dicts[l]
            if len(level_dict) < 1:
                continue
            for package_name in level_dict:
                package_full = level_dict[package_name]
                required_version = package_full['installed_version']  # not sure, if this is correct
                print('{}=={} # LEVEL_{:0=2d}'.format(package_name, required_version, l))
            print('=' * 8)
        return True


class PackageInfo:
    package_info_name = 'pip_show_all.log'

    def __init__(self):
        self.pi_dict = self.get_dictionary(log_name=self.package_info_name)
        t = self.get_summary('numpy')
        return

    def get_dictionary(self, log_name: str) -> dict:
        d = dict()
        with open(log_name, 'r') as f:
            package = None
            for line in f:
                items = line.split(':')
                key = items[0]
                if key == 'Name':
                    items.pop(0)
                    package = items[0].strip()
                    continue
                if key == 'Summary':
                    items.pop(0)
                    summary = line.replace('Summary:', '').strip()
                    # print('Summary: \'{}\' -> \'{}\''.format(package, summary))
                    d[package] = summary
                    del summary
                    del package  # in order to trigger an error and avoid wrong assignments..
            # for
        # with
        print('Summaries: {}'.format(len(d)))
        return d

    def get_summary(self, package: str) -> typing.Union[str, object]:
        if package is None or not isinstance(package, str):
            return None
        summary = self.pi_dict.get(package)
        if summary is not None:
            return summary
        # lower_package = package#.lower()
        # summary = self.pi_dict.get(lower_package)
        # if summary is not None:
        #    return summary
        package2 = package.replace('_', '.')  # Mastodon_py
        summary = self.pi_dict.get(package2)
        if summary is None:
            print('get_summary({},{}) ?'.format(package, package2))
        return summary


class LevelsCheck:
    json_full = '/tmp/pipdeptree.cache'
    requirements_txt = 'requirements_miniconda.txt'  # make this configurable

    def __init__(self):
        self.levels_max = 12  # level 9 currently is realized maximum
        self.cache_max_seconds = 5.0 * 60.0
        self.levels_cache = LevelsCache(self.levels_max)
        self.package_info = PackageInfo()

    def get_summary(self, package: str) -> typing.Union[str, object]:
        return self.package_info.get_summary(package=package)

    def render_json_tree(self, tree: PackageDAG, indent: int):
        """Converts the tree into a nested json representation.

        The json repr will be a list of hashes, each hash having the following fields:
          - package_name
          - key
          - required_version
          - installed_version
          - dependencies: list of dependencies

        :param dict tree: dependency tree
        :param int indent: no. of spaces to indent json
        :returns: json representation of the tree
        :rtype: str

        """
        tree = tree.sort()
        # branch_keys = set(r.key for r in chain.from_iterable(tree.values()))
        nodes = [p for p in tree.keys()]  # if p.key not in branch_keys]

        def aux(node, parent=None, chain=None):
            if chain is None:
                chain = [node.project_name]
            d = node.as_dict()
            if parent:
                d['required_version'] = node.version_spec if node.version_spec else 'Any'
            else:
                d['required_version'] = d['installed_version']
            d['dependencies'] = [
                aux(c, parent=node, chain=chain + [c.project_name])
                for c in tree.get_children(node.key)
                if c.project_name not in chain
            ]
            return d

        return json.dumps([aux(p) for p in nodes], indent=indent)

    def parse_levels(self, pruned_list_of_dicts: typing.List[dict]) -> bool:
        lod = pruned_list_of_dicts
        lc = self.levels_cache
        level = 0
        old_len_lod = 999

        packages_sorted = 'packages_sorted.log'
        with open(packages_sorted, 'w') as ps_file:
            while True:
                level += 1
                if level >= self.levels_max:
                    break
                if old_len_lod == len(lod) == 1:
                    break
                if len(lod) < 1:
                    break
                # print('Level {} .. {} packages'.format(level, len(lod)))
                next_lod = list()
                for d in lod:
                    package_name = d['key']
                    required_version = d['required_version']
                    dependencies = d['dependencies']
                    if level == 1:
                        if len(dependencies) < 1:
                            lc.add(level, d)
                            ps_file.write('{}\n'.format(package_name))
                            # print('P: {} {} -> D: None .. Level 0'.format(package_name, required_version))
                            # do not append to next
                        else:
                            next_lod.append(d)
                    else:
                        found_all_below = True
                        for dep in dependencies:
                            dependency_name = dep['key']
                            if not lc.find_below(level, dep):
                                found_all_below = False
                            # print('P: {} {} -> D: {} .. {}'
                            #      .format(package_name, required_version, dependency_name, found_all_below))
                        if found_all_below:
                            lc.add(level, d)
                            ps_file.write('{}\n'.format(package_name))
                            # print('P: {} {} -> Level {}  (found_all_below)'
                            #      .format(package_name, required_version, level))
                            # do not append to next
                        else:
                            next_lod.append(d)
                            # print('P: {} {} -> Level {}  (NOT found_all_below)'
                            #      .format(package_name, required_version, level))
                    # print('-' * 8)
                old_len_lod = len(lod)
                del lod
                lod = next_lod
                # print('=' * 8)
            # print('=' * 72)
            # lc.show()
        # with
        return True

    def modify_requirements(self) -> bool:
        req_src = self.requirements_txt
        if not os.path.exists(req_src):
            return False
        with open(req_src, 'r') as f:
            lines_org = f.readlines()
        req_dst = req_src.replace('.txt', '.tmp')
        if os.path.exists(req_dst):
            os.remove(req_dst)

        changes = 0
        changes2 = 0
        fatal = False
        seps = ['=', '>', '<', '~', '[']
        underline = '_'
        lc = self.levels_cache
        lines_new = []
        for line_org in lines_org:
            # print('{}'.format(line_org), end='')
            if line_org[0] == '#' or line_org[0] == '\n':
                lines_new.append(line_org)
                continue
            level = (-1)
            package = None
            for sep in seps:
                parts = line_org.split(sep)
                package = parts[0]
                level = lc.find_level(key=package)
                if level > 0:
                    break
                # for packages, like Mastodon.py ..
                if package.find(underline) < 0:
                    continue
                package2 = package.replace(underline, '.')
                level = lc.find_level(key=package2)
                if level > 0:
                    break
                package3 = package.replace('_', '-')  # typing_extensions ..
                level = lc.find_level(key=package3)
                if level > 0:
                    break
                # print('package: {} {}'.format(package, sep))
            if level <= 0:  # might have to remove the cache file !! (or typos in packages !)
                lines_new.append(line_org)
                print('No package found in: {}'.format(line_org), end='')
                fatal = True
                continue

            level_needed = 'LEVEL_{:0=2d}'.format(level)
            if line_org.find(level_needed) >= 0:
                # LEVEL_xy is correct
                line_new = line_org
            else:
                changes += 1
                # replace LEVEL_?? with level_needed
                level_wrong = None
                lev = 0
                levels_max = self.levels_max * 2
                for lev in range(levels_max):
                    level_wrong = 'LEVEL_{:0=2d}'.format(lev)
                    if line_org.find(level_wrong) > 0:
                        break
                if lev == levels_max - 1:
                    print('No LEVEL_?? found for \'{}\' in \'{}\''.format(level_needed, line_org), end='')
                    line_new = line_org
                    fatal = True
                else:
                    line_new = line_org.replace(level_wrong, level_needed)
                # fi
            # fi

            summary = self.get_summary(package=package)
            if summary is not None and summary and summary != 'UNKNOWN':
                if summary[-1] == '.':
                    summary = summary[:-1]
                summary_needed = ' # {}\n'.format(summary.strip())
                i = line_new.find(summary_needed)
                if i < 0:
                    changes2 += 1
                    line_new2 = line_new[:-1] + summary_needed
                else:
                    line_new2 = line_new
            else:
                line_new2 = line_new

            lines_new.append(line_new2)
            del line_new
            del line_new2
        # for

        if fatal:
            return False
        if changes > 0 or changes2 > 0:
            print('Writing: {} with {}/{} changes'.format(req_dst, changes, changes2))
            with open(req_dst, 'w') as f:
                f.writelines(lines_new)
            with open(req_src) as file_1, open(req_dst) as file_2:
                differ = difflib.Differ()
                for line in differ.compare(file_1.readlines(), file_2.readlines()):
                    if line.startswith(' ') or line.startswith('?') or line[0] == '\n':
                        continue
                    print(line, end='')
            return False
        else:
            print('All levels correct: {}'.format(req_src))
        return True

    def prune_dependencies2(self, full_list_of_dicts: typing.List[dict]) -> typing.List[dict]:
        key_dependencies = 'dependencies'
        for d in full_list_of_dicts:
            dependencies = d[key_dependencies]
            for dep in dependencies:
                # print('P: {} -> D: {}'.format(package_name, dep['key']))
                dependencies2 = dep[key_dependencies]
                if len(dependencies2) < 1:
                    continue
                del dep[key_dependencies]
                dep[key_dependencies] = dict()
        return full_list_of_dicts

    def get_packages_installed(self) -> typing.Union[typing.List[dict], typing.Any]:
        max_seconds = self.cache_max_seconds
        now = time.time()
        try:
            with open(self.json_full) as f:
                stamp = os.path.getmtime(self.json_full)
                delta_seconds = (now - stamp)
                if delta_seconds > max_seconds:
                    print('Ignoring cache: {} too old: {} > {}'
                          .format(os.path.basename(self.json_full), delta_seconds, max_seconds))
                else:
                    json_string = f.read()
                    full_list_of_dicts = json.loads(json_string)
                    pruned_list_of_dicts = self.prune_dependencies2(full_list_of_dicts)
                    print('Using cache: {} ..'.format(self.json_full))
                    return pruned_list_of_dicts
        except:
            print('No cache: {} ..'.format(self.json_full))

        local_only = False
        user_only = False
        pkgs = get_installed_distributions(local_only=local_only, user_only=user_only)
        try:
            tree = PackageDAG.from_pkgs(pkgs)
        except:
            return None
        json_string = self.render_json_tree(tree, indent=4)
        with open(self.json_full, 'w') as f:
            f.write(json_string)
        full_list_of_dicts = json.loads(json_string)
        pruned_list_of_dicts = self.prune_dependencies2(full_list_of_dicts)
        return pruned_list_of_dicts


def main():
    lc = LevelsCheck()
    pruned_list_of_dicts = lc.get_packages_installed()
    if pruned_list_of_dicts is None:
        return 1
    if not lc.parse_levels(pruned_list_of_dicts):
        return 1
    if not lc.modify_requirements():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
