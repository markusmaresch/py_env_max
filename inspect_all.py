#
# -*- coding: utf-8 -*-
#
import sys
import importlib_metadata

class InspectAll:
    @staticmethod
    def run() -> bool:
        packages_sorted = 'packages_sorted.log'
        count = 0
        good = 0
        with open(packages_sorted, 'r') as f:
            lines = f.readlines()
            for line in lines:
                count += 1
                package = line.strip()

                try:
                    dist = importlib_metadata.distribution(package)
                    md = dist.metadata
                    version = md.json['version']
                    # print('{}=={}'.format(package, version))
                    good += 1
                    continue
                except:
                    print('Can\'t inspect {} !!'.format(package))

        if good > 0 and good >= count:
            print('all package inspections good: {}/{}'.format(good, count))
            return True
        print('some package inspections failed: {}/{}  .. fix in {}'
              .format(count-good, count, packages_sorted))
        return False


def main():
    ia = InspectAll()
    if not ia.run():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
