#
# -*- coding: utf-8 -*-
#
import enum
# import os
import sys


@enum.unique
class OsPlatform(enum.IntFlag):
    UNKNOWN = -1
    ANY = 0
    LINUX = 1
    OSX = 2
    WINDOWS = 3
    MAX = 4

    @staticmethod
    def get() -> int:
        # is_win: bool = (os.name == 'nt')
        # is_posix = (os.name == 'posix')
        # is_darwin = (os.name == 'darwin')
        platforms = {
            'linux1': OsPlatform.LINUX,
            'linux2': OsPlatform.LINUX,
            'darwin': OsPlatform.OSX,
            'win32': OsPlatform.WINDOWS
        }
        if sys.platform not in platforms:
            return OsPlatform.UNKNOWN
        return platforms[sys.platform]
