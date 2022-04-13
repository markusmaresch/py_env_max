#
# -*- coding: utf-8 -*-
#
import sys
import os


# from pip._internal.cli.main import main as pip_main


# pip_main(['list'])
# pip_main(['show', 'numpy', 'pandas', 'tensorflow'])

class PipShowAll:
    @staticmethod
    def run() -> int:

        # collect packages
        cmd_pip_list = 'pip list'
        print('Collecting packages with: {}'.format(cmd_pip_list))
        packages = []
        with os.popen(cmd_pip_list) as pipe:
            for line in pipe:
                package = line.split()[0]
                if package == 'Package' or package.startswith('----'):
                    continue
                # print(package)
                packages.append(package)

        #
        # replace with https://importlib-metadata.readthedocs.io/en/latest/using.html
        #

        cmd_pip_show = 'pip show'
        print('Querying with: {} <{} packages>'.format(cmd_pip_show, len(packages)))
        packs = ' '.join([str(elem) for elem in packages])
        cmd_pip_show = '{} {}'.format(cmd_pip_show, packs)
        pip_show_all = 'pip_show_all.log'
        with open(pip_show_all, 'w') as f:
            with os.popen(cmd_pip_show) as pipe:
                for line in pipe:
                    items = line.split(':')
                    key = items[0]
                    if key == 'Location':
                        # we drop this intentionally
                        continue
                    if key == 'Requires' or key == 'Required-by':
                        items.pop(0)
                        items_split = items[0].strip().split(',')
                        items_sorted = [str(e.strip()) for e in items_split]
                        items_sorted.sort()
                        items_str = ' '.join([e for e in items_sorted])
                        line = '{}: {}\n'.format(key, items_str)
                    f.write(line)
                # for line
            # pipe
        # write
        print('Created: {}'.format(pip_show_all))
        return 0


def main():
    return PipShowAll().run()


if __name__ == '__main__':
    sys.exit(main())
