#
# -*- coding: utf-8 -*-
#
import sys
import re
import random
import requests
from threading import Thread


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
    def get_releases(name: str, latestN: int = 20) -> [str]:
        invalid = re.compile(r".+rc[0-9]+$|.+a[0-9]+$|.+b[0-9]+$|.+dev[0-9]+$|.+post[0-9]+$")

        def valid(release: str) -> bool:
            if invalid.match(release):
                return False
            return True

        js = PyPiCmd.get_pypi_json(name)
        if js is None:
            return None
        releases = js.get('releases')
        if releases is None:
            return None
        keys = releases.keys()
        rs = [r for r in keys if valid(r)]
        return rs[-latestN:]

    @staticmethod
    def get_release_one(name: str, index: int, result: [str]):
        # print('Start: {} {}'.format(name, index))
        rs = PyPiCmd.get_releases(name=name, latestN=10)
        result[index] = rs
        print('.', end='' if random.random() > 1.0/40.0 else '\n')
        return

    @staticmethod
    def get_release_many(packages: [str]) -> [str]:
        N = len(packages)
        threads = [None] * N
        releases = [None] * N
        i = 0
        for package_name in packages:
            threads[i] = Thread(target=PyPiCmd.get_release_one,
                                args=(package_name, i, releases))
            threads[i].start()
            i += 1
        # for
        for i in range(N):
            threads[i].join()
        # for
        print()
        del threads
        return releases

    @staticmethod
    def test_releases_many() -> bool:
        # grep -e '"key"' pipdeptree.json | sed -e "s/ //g"  -e "s/\"/'/g" | sort -u | cut -c7-999
        packages = [
            'absl-py', 'aenum', 'affinegap', 'agate', 'aiodns', 'aiohttp',
            'aiohttp-cors', 'aiohttp-socks', 'aioredis', 'aiosignal',
            'alabaster', 'alembic', 'alpha-vantage', 'altair', 'altgraph',
            'amqp', 'analytics-python', 'ansi2html', 'antlr4-python3-runtime',
            'anyio', 'appdirs', 'appnope', 'argcomplete', 'argon2-cffi',
            'argon2-cffi-bindings', 'arrow', 'asciitree', 'asgiref',
            'asn1crypto', 'ast-decompiler', 'astor', 'asttokens',
            'astunparse', 'async-generator', 'async-timeout', 'asynq', 'atari-py',
            'attrs', 'authlib', 'autopep8', 'axial-positional-embedding',
            'azure-common', 'azure-core', 'azure-eventhub', 'azure-storage-blob',
            'babel', 'backcall', 'backoff', 'base58', 'bcrypt', 'beautifulsoup4',
            'bert-for-tf2', 'bertviz', 'billiard', 'biopython', 'black',
            'bleach', 'blessings', 'blinker', 'blis', 'blurhash', 'bokeh',
            'boltons', 'boost', 'boto', 'boto3', 'botocore',
            'bottleneck', 'box2d', 'box2d-py', 'brotli', 'brotlipy', 'btrees'
        ]
        releases = PyPiCmd.get_release_many(packages)
        if releases is None or len(releases) != len(packages):
            return False
        return True

    @staticmethod
    def test_releases_one() -> bool:
        releases = PyPiCmd().get_releases('altair')
        if releases is None:
            return False
        releases = PyPiCmd().get_releases('tensorflow')
        if releases is None:
            return False
        return True

    @staticmethod
    def pip_selftest() -> bool:
        r = random.random()
        if not PyPiCmd.test_releases_many():
            return False
        if not PyPiCmd.test_releases_one():
            return False
        return True


def main():
    if not PyPiCmd.pip_selftest():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
