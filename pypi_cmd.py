#
# -*- coding: utf-8 -*-
#
import sys
import requests


# from distutils.version import StrictVersion


class PyPiCmd:

    @staticmethod
    def get_pypi_json(name: str) -> str:
        package = name
        response = requests.get(f'https://pypi.org/pypi/{package}/json')
        js = response.json()
        return js

    @staticmethod
    def get_release_latest(name: str) -> str:
        js = PyPiCmd.get_pypi_json(name)
        info = js['info']
        latest_version = info['version']
        return latest_version

    @staticmethod
    def get_releases(name: str, latestN: int = 10) -> [str]:
        js = PyPiCmd.get_pypi_json(name)
        releases = js["releases"].keys()
        # versions.sort(key=StrictVersion)
        rs = [r for r in releases]  # add checks against 'rc0' and similar
        return rs[-latestN:]
        # releases = js['releases'].sort(key=StrictVersion)
        # rs = [r for r in releases]  # add checks against 'rc0' and similar
        # return rs[-latestN:]

    @staticmethod
    def pip_selftest() -> bool:
        releases = PyPiCmd().get_releases('pandas')
        if releases is None:
            return False
        return True


def main():
    if not PyPiCmd.pip_selftest():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
