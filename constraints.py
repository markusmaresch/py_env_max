#
# -*- coding: utf-8 -*-
#
import enum

from version import Version, NormalizedVersion


@enum.unique
class Comparator(enum.IntFlag):
    # INVALID = (-1)
    GT = 0
    GE = 1
    EQ = 2
    NEQ = 3
    APE = 4
    LE = 5
    LT = 6


class Constraints:
    def __init__(self, package: str):
        self.package = package
        self.comparator = [list() for c in Comparator if c >= 0]
        return

    def __str__(self):
        s0 = 'constraints: {} :'.format(self.package)
        s = ''
        for comp in Comparator:
            comparator = self.comparator[comp]
            if len(comparator) < 1:
                continue
            s += ' {}'.format(comp.name)
            for c in sorted(comparator):  # only visually sorted !!
                s = s + ' {}'.format(c)
            s = s + ' '
        # for
        if not s:
            return s0 + ' None'
        return s0 + s

    def no_constraints(self) -> bool:
        for comp in Comparator:
            comparator = self.comparator[comp]
            if len(comparator) < 1:
                continue
            return False
        # for
        return True

    def optimize(self) -> bool:
        debug = False
        for comp in Comparator:
            comparator = self.comparator[comp]
            if len(comparator) <= 1:
                continue
            if comp in (Comparator.GE, Comparator.GT):
                reverse = True
            elif comp in (Comparator.LE, Comparator.LT):
                reverse = False
            elif comp == Comparator.EQ:
                print('optimize: {} {}: {} !!!'.format(self.package, comp.name, comparator))
                continue
            else:
                continue
            comparator2 = Version.sort(comparator, reverse)
            compacted = [comparator2[0]]
            if debug:
                print('optimize: {} {}: {} -> {}'.format(self.package, comp.name, comparator, compacted))
            self.comparator[comp] = compacted
        # for
        return True

    def append2(self, vr: str) -> bool:
        comp = Comparator.EQ
        version = None
        if vr[0] == '>':
            if vr[1] == '=':
                comp = Comparator.GE
                version = vr[2:]
            else:
                comp = Comparator.GT
                version = vr[1:]
            # fi
        elif vr[0] == '<':
            if vr[1] == '=':
                comp = Comparator.LE
                version = vr[2:]
            else:
                comp = Comparator.LT
                version = vr[1:]
            # fi
        elif vr[1] == '=':
            if vr[0] == '!':
                comp = Comparator.NEQ
                version = vr[2:]
            elif vr[0] == '=':
                comp = Comparator.EQ
                version = vr[2:]
            elif vr[0] == '~':
                comp = Comparator.APE
                version = vr[2:]
            # fi
        # fi
        if version is None:
            return False
        comparator = self.comparator[comp]
        if version in comparator:
            return True
        comparator.append(version)
        return True

    def append(self, version_required: str) -> bool:
        if version_required.find(',') > 0:
            vrs = version_required.split(',')
            for vs in vrs:
                self.append2(vs)
            # for
        else:
            self.append2(version_required)
        return True

    def accept(self, comp: int, release: NormalizedVersion, version: NormalizedVersion):
        if comp == Comparator.GE:
            if release >= version:
                return True
        elif comp == Comparator.GT:
            if release > version:
                return True
        elif comp == Comparator.LE:
            if release <= version:
                return True
        elif comp == Comparator.LT:
            if release < version:
                return True
        elif comp == Comparator.EQ:
            if release == version:
                return True
        elif comp == Comparator.NEQ:
            if release != version:
                return True
        else:
            return False

        return False

    def match_possible_releases(self, package: str, releases: [str]) -> [str]:
        # reduce the list of release, according to constraints
        if self.no_constraints():
            return [releases[0]]
        m = []
        for r in releases:
            # print('Testing: {} {}'.format(package, r))
            release = Version.normalized(r)
            good = True
            for comp in Comparator:
                comparator = self.comparator[comp]
                if len(comparator) < 1:
                    continue
                # print('  Compare: {} .. {}'.format(comp.name, comparator))
                for v in comparator:
                    version = Version.normalized(str(v))
                    if not self.accept(comp, release, version):
                        good = False
                        break
                    # fi
                # for
                if not good:
                    break
            # for comp
            if good:
                m.append(r)
        # for releases
        return m
