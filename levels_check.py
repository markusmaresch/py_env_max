#
# -*- coding: utf-8 -*-
#
import sys
import json
import typing
from itertools import chain

#
# a bit akward - use pip and pipdeptree in order to get the currently
# installed package trees
#
from pip._internal.utils.misc import get_installed_distributions
from pipdeptree import PackageDAG


class LevelsCache:
    def __init__(self, levels_max: int):
        self.levels_max = levels_max
        self.xxx = [dict() for x in range(levels_max)]
        return

    def add(self, level: int, package: dict):
        d = self.xxx[level]
        key = package['key']
        d[key] = package
        return

    def find_below(self, level: int, package: dict) -> bool:
        key = package['key']
        for l in range(1, self.levels_max):
            d = self.xxx[l]
            if d.get(key):
                return True
        return False

    def show(self) -> bool:
        for l in range(1, self.levels_max):
            level_dict = self.xxx[l]
            if len(level_dict) < 1:
                continue
            for package_name in level_dict:
                package_full = level_dict[package_name]
                required_version = package_full['installed_version']  # not sure, if this is correct
                print('{}=={} # LEVEL_{:0=2d}'.format(package_name, required_version, l))
            print('=' * 8)
        return True


# flatten = chain.from_iterable


class LevelsCheck:
    json_full = 'pipdeptree.cache'
    requirements_txt = 'requirements_miniconda.txt'  # make this configurable
    levels_max = 10  # level 6 currently is realized maximum

    def __init__(self):
        self.levels_cache = LevelsCache(self.levels_max)

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
        branch_keys = set(r.key for r in chain.from_iterable(tree.values()))
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

    def parse_levels(self, pruned_list_of_dicts: typing.List[dict]):

        lod = pruned_list_of_dicts
        lc = self.levels_cache
        level = 0
        while True:
            level += 1
            if level >= self.levels_max:
                break
            print('Level {} .. {} packages'.format(level, len(lod)))
            if len(lod) < 1:
                break
            next_lod = list()
            for d in lod:
                package_name = d['key']
                required_version = d['required_version']
                dependencies = d['dependencies']
                if level == 1:
                    if len(dependencies) < 1:
                        lc.add(level, d)
                        #print('P: {} {} -> D: None .. Level 0'.format(package_name, required_version))
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
                        #print('P: {} {} -> Level {}  (found_all_below)'
                        #      .format(package_name, required_version, level))
                        # do not append to next
                    else:
                        next_lod.append(d)
                        #print('P: {} {} -> Level {}  (NOT found_all_below)'
                        #      .format(package_name, required_version, level))
                #print('-' * 8)
            del lod
            lod = next_lod
            print('=' * 8)
        print('=' * 72)
        lc.show()
        return

    def prune_dependencies2(self, full_list_of_dicts: typing.List[dict]) -> typing.List[dict]:
        for d in full_list_of_dicts:
            package_name = d['key']
            dependencies = d['dependencies']
            for dep in dependencies:
                # print('P: {} -> D: {}'.format(package_name, dep['key']))
                dependencies2 = dep['dependencies']
                if len(dependencies2) < 1:
                    continue
                del dep['dependencies']
                dep['dependencies'] = dict()
        return full_list_of_dicts

    def get_packages_installed(self) -> typing.List[dict]:
        try:
            with open(self.json_full) as f:
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
        tree = PackageDAG.from_pkgs(pkgs)
        json_string = self.render_json_tree(tree, indent=4)
        with open(self.json_full, 'w') as f:
            f.write(json_string)
        full_list_of_dicts = json.loads(json_string)
        pruned_list_of_dicts = self.prune_dependencies2(full_list_of_dicts)
        return pruned_list_of_dicts


def main():
    lc = LevelsCheck()
    pruned_list_of_dicts = lc.get_packages_installed()
    lc.parse_levels(pruned_list_of_dicts)
    return


if __name__ == '__main__':
    sys.exit(main())
