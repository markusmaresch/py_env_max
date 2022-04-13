#
# -*- coding: utf-8 -*-
#
import requests


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
    def get_versions(name: str, latestN: int = 10) -> [str]:
        js = PyPiCmd.get_pypi_json(name)
        releases = js['releases']
        rs = [r for r in releases]  # add checks against 'rc0' and similar
        return rs[-latestN:]
