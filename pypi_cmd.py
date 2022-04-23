#
# -*- coding: utf-8 -*-
#
import sys
import requests


class PyPiCmd:

    @staticmethod
    def get_pypi_json(package: str) -> dict:
        try:
            response = requests.get(f'https://pypi.org/pypi/{package}/json')
            js = response.json()
            return js
        except:
            return None

    @staticmethod
    def get_release_latest(package: str) -> str:
        js = PyPiCmd.get_pypi_json(package=package)
        if js is None:
            return None
        info = js.get('info')
        if info is None:
            return None
        latest_version = info.get('version')
        if latest_version is None:
            return None
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
