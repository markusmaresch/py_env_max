#
# -*- coding: utf-8 -*-
#
import sys
import json
import typing

#
# a bit akward - use pip and pipdeptree in order to get the currently
# installed package trees
#
from pip._internal.utils.misc import get_installed_distributions
from pipdeptree import render_json_tree, PackageDAG


class LevelsCache:
    def __init__(self):
        pass

    def add(self, level: int, package: dict):
        return

    def find(self, package: dict) -> bool:
        return False


class LevelsCheck:
    json_full = 'pipdeptree.cache'

    def __init__(self):
        pass

    def parse_levels(self, pruned_list_of_dicts: typing.List[dict]):

        level = (-1)
        while True:
            level += 1
            if level > 10:
                break
            print('Level {}'.format(level))
            for d in pruned_list_of_dicts:
                dependencies = d['dependencies']

                package_name = d['key']
                required_version = d['required_version']
                for dep in dependencies:
                    dependency_name = dep['key']
                    print('P: {} {} -> D: {}'.format(package_name, required_version, dependency_name))
                print('-' * 8)
            print('=' * 8)
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
        json_string = render_json_tree(tree, indent=4)
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
