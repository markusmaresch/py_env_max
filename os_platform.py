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
    def valid(op: int) -> bool:
        if OsPlatform.LINUX <= op <= OsPlatform.WINDOWS:
            return True
        return False

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

    @staticmethod
    def script_extension() -> str:
        os = OsPlatform.get()
        if os == OsPlatform.WINDOWS:
            return "bat"  # or "cmd"
        return "sh"

    @staticmethod
    def script_comment() -> str:
        os = OsPlatform.get()
        if os == OsPlatform.WINDOWS:
            return "rem"  # or "cmd"
        return "#"

    @staticmethod
    def selftest() -> bool:
        op = OsPlatform.get()
        if not OsPlatform.valid(op):
            return False
        return True


def main():
    if not OsPlatform.selftest():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
