#
# -*- coding: utf-8 -*-
#
import re
import enum


@enum.unique
class ReleaseFilter(enum.IntFlag):
    # sequence of acceptable releases - order matters - top to down of acceptance
    REGULAR = 1
    A = 2
    B = 4
    DEV = 8
    RC = 16
    POST = 32
    PRE = 64

    @staticmethod
    def get_re_invalid_pattern(release_filter: int) -> re.Pattern:
        #
        # this could be cached !!
        #

        def app(r2: str, a: str) -> str:
            if r2:
                return r2 + '|' + a
            return a

        r = r""
        if not (release_filter & ReleaseFilter.A):
            r = app(r, r".+a[0-9]+$")
        if not (release_filter & ReleaseFilter.B):
            r = app(r, r".+b[0-9]+$")
        if not (release_filter & ReleaseFilter.POST):
            r = app(r, r".+post[0-9]+$")
        if not (release_filter & ReleaseFilter.PRE):
            r = app(r, r".+pre[0-9]+$")
        if not (release_filter & ReleaseFilter.RC):
            r = app(r, r".+rc[0-9]+$")
        if not (release_filter & ReleaseFilter.DEV):
            r = app(r, r".+dev[0-9]+$")
        if not (release_filter & ReleaseFilter.REGULAR):
            r = app(r, r".+[0-9][a-z]$")

        re_pattern = re.compile(r)
        return re_pattern

    @staticmethod
    def valid(release: str, re_invalid_pattern: re.Pattern) -> bool:
        if not re_invalid_pattern.match(release):
            return True
        return False
