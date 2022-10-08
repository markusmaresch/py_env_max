#
# -*- coding: utf-8 -*-
#
import sys
import random
import threading
import typing
import time

from version import Version
from database import Database

# from pip
from pip._vendor import requests  # get pip's request, so we do not have to install it


class PyPiCmd:

    @staticmethod
    def get_pypi_json(package: str) -> typing.Union[dict, object]:
        t_max = 3
        s = 0.1
        for t in range(t_max):
            try:
                response = requests.get(f'https://pypi.org/pypi/{package}/json', timeout=s)
                js = response.json()
                return js
            except:
                time.sleep(s)
                s *= 2
        # for
        return None

    @staticmethod
    def get_releases(name: str, keep: int = 40) -> typing.Union[typing.Dict, object]:
        js = PyPiCmd.get_pypi_json(name)
        if js is None:
            return None
        releases = js.get('releases')
        if releases is None:
            return None
        keys = releases.keys()
        releases = [r for r in keys]
        sorted_releases = Version.sort(releases=releases, reverse=True)
        latest_releases = sorted_releases[:keep]
        d = {Database.RELEASES_RECENT: latest_releases}
        info = js.get('info')
        if info is not None:
            summary = info.get('summary')
            if summary is not None and summary:
                summary = summary.strip()
                if summary != 'UNKNOWN' and summary[-1] == '.':
                    summary = summary[:-1]
                d[Database.SUMMARY] = summary
        return d

    @staticmethod
    def get_release_one(name: str, index: int, result: [typing.Dict]):
        rd = PyPiCmd.get_releases(name=name)
        c = 'x' if rd is None else '.'
        result[index] = rd
        print(c, end='' if random.random() > 1.0 / 20.0 else '\n', flush=True)
        return

    @staticmethod
    def get_release_many(packages: [str]) -> [typing.Dict]:

        def fix_releases(rf: typing.List) -> typing.Union[typing.List[typing.List], object]:
            """
            The above may have crashed, therefore we may have to clean up invalid versions
            """
            if rf is None:
                return None
            delete = set()
            for ii in range(0, len(rf)):
                ra = rf[ii]
                if ra is None:
                    continue
                rr = ra.get(Database.RELEASES_RECENT)
                if rr is None:
                    continue
                for r in rr:
                    try:
                        v = Version.convert(r)
                        del v
                    except:
                        delete.add(r)
                # for
                if len(delete) > 0:
                    rn = [r for r in rr if r not in delete]
                    rf[ii][Database.RELEASES_RECENT] = rn
                    delete.clear()
            # for
            return rf

        N = len(packages)
        threads = [None] * N
        releases = [None] * N
        done = [False] * N
        still_open = 0
        t_max = 7
        for t in range(t_max):
            for i in range(N):
                if done[i]:
                    continue
                package_name = packages[i]
                threads[i] = threading.Thread(target=PyPiCmd.get_release_one,
                                              args=(package_name, i, releases))
                threads[i].start()
                time.sleep(0.05)
                if threading.active_count() > 10:
                    time.sleep(0.5)
                if threading.active_count() > 15:
                    time.sleep(0.5)
                if threading.active_count() > 20:
                    time.sleep(0.5)
                if threading.active_count() > 25:
                    time.sleep(0.5)
                # print('ac: {}: {}'.format(i, threading.active_count()))
            # for
            for i in range(N):
                if done[i]:
                    continue
                threads[i].join()
                if releases[i] is None:
                    # retry in next iteration
                    continue
                done[i] = True
            # for
            still_open = N - sum(done)
            if still_open < 1:
                if t > 0:
                    print('\nInfo: releases ok after {}/{}'.format(t, t_max - 1))
                break
            print('\nWarning: releases {}/{} .. {}/{} still open'.format(t, t_max - 1, still_open, N))
        # for
        print()
        if still_open > 0:
            print('Error: releases {}/{} still open'.format(still_open, N))
        del threads
        releases_dict = fix_releases(releases)
        return releases_dict

    @staticmethod
    def test_releases_many() -> bool:
        # grep -e '"key"' pipdeptree.json | sed -e "s/ //g"  -e "s/\"/'/g" | sort -u | cut -c7-999
        packages = [
            'phik', 'stack-data', 'stumpy', 'grpcio-status',
            'googleauthentication', 'wcwidth', 'memory-profiler', 'icu',
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
        releases_dict = PyPiCmd.get_release_many(packages)
        if releases_dict is None or len(releases_dict) != len(packages):
            return False
        return True

    @staticmethod
    def test_releases_one() -> bool:
        releases_dict = PyPiCmd().get_releases('tensorflow')
        if releases_dict is None:
            return False
        return True

    @staticmethod
    def pip_selftest() -> bool:
        if not PyPiCmd.test_releases_one():
            return False
        if not PyPiCmd.test_releases_many():
            return False
        return True


def main():
    if not PyPiCmd.pip_selftest():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
