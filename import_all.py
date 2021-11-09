#
# -*- coding: utf-8 -*-
#
import sys
from importlib import import_module


class ImportAll:
    @staticmethod
    def run() -> bool:
        packages_sorted = 'packages_sorted.log'
        with open(packages_sorted, 'r') as f:
            lines = f.readlines()
            for line in lines:
                package = line.strip()

                #
                # does not work in such a generic way :-(
                #

                try:
                    mdl = import_module(package)
                    # print('{} imported'.format(package))
                    continue
                except:
                    pass  # print('Can\'t import {} !!'.format(package))
                    # fails.append(mod)

                package2 = package.replace('-', '_')
                try:
                    mdl = import_module(package2)
                    # print('{} imported2'.format(package2))
                    continue
                except:
                    print('Can\'t import2 {} !!'.format(package2))

            print('all imports done')
        return True


def main():
    ia = ImportAll()
    if not ia.run():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
