#
# -*- coding: utf-8 -*-
#
import os.path
import sys
import subprocess
import datetime

from functools import lru_cache


# REMOVE: conda remove --name py_env_XXX --all

class CondaCmd:
    @staticmethod
    def version() -> str:
        version = ''
        try:
            output = subprocess.check_output(['conda', '-V'])
            for line in output.splitlines():
                v = line.decode().split()
                if v[0] != 'conda':
                    continue
                version = v[1]
                break
            # for
        except Exception as e:
            print('Failed: conda -V .. {}'.format(e))
        if not version:
            print('Failed: conda -V')
        return version

    @staticmethod
    def conda_list(destination_path: str) -> bool:
        try:
            output = subprocess.check_output(args=['conda', 'list'], text=True).rstrip()
            with open(destination_path, 'w', newline='') as f:
                for line in output.splitlines():
                    if line.startswith('\x1b'):
                        continue
                    f.write(line + '\n')
                # for
            # with
        except Exception as e:
            print('Failed: conda list .. {}'.format(e))
        return True

    @staticmethod
    def conda_env_export(destination_path: str) -> bool:
        try:
            output = subprocess.check_output(args=['conda', 'env', 'export'], text=True).rstrip()
            with open(destination_path, 'w', newline='') as f:
                for line in output.splitlines():
                    if line.startswith('\x1b'):
                        continue
                    f.write(line + '\n')
                # for
            # with
        except Exception as e:
            print('Failed: conda env export .. {}'.format(e))
        return True

    @staticmethod
    def env_list() -> [str]:
        # call: conda env list | awk '{print $1}' # more or less
        return None

    @staticmethod
    @lru_cache(maxsize=1)  # it does not change during runtime
    def _env_activated() -> (str, str):
        # conda env list | grep -e ' \* ' | awk '{print $1 $3}'
        try:
            output = subprocess.check_output(['conda', 'env', 'list'])
            for line in output.splitlines():
                v = line.decode().split()
                if v[0][0] == '#':
                    continue
                if len(v) < 2:
                    continue
                if v[1] != '*':
                    continue
                return v[0], v[2]
            # for
        except:
            pass
        print('Failed: conda env list')
        return '', ''

    @staticmethod
    def env_most_recent_change() -> int:
        # get directory of activated environment
        # find most recent file in it (excluding __pycache__ ..)

        def newest_file_in_tree() -> str:
            return max(
                (os.path.join(dirname, filename)
                 for dirname, dirnames, filenames in os.walk(env_root)
                 for filename in filenames
                 # if filename.endswith(extension)
                 ),
                key=lambda fn: os.stat(fn).st_mtime)

        env_name, env_root = CondaCmd._env_activated()
        if not env_root:
            print('Failed: env_most_recent_change')
            return -1
        if not os.path.exists(env_root):
            return -1
        file_name_newest = newest_file_in_tree()
        t = int(os.stat(file_name_newest).st_mtime)
        modified = datetime.datetime.fromtimestamp(t)  # , tz=datetime.timezone.utc)
        print('most recent in {}: {} .. {}'.format(env_name, modified, file_name_newest))
        return t

    @staticmethod
    def env_activated() -> str:
        activated, _ = CondaCmd._env_activated()
        if not activated:
            print('Failed: env_activated')
        return activated

    @staticmethod
    def env_activate(env_name: str) -> bool:
        # don't try, will not work, needs to be called by hand in shell
        return False

    @staticmethod
    def selftest() -> bool:
        CondaCmd.conda_list('test.yml')
        version = CondaCmd.version()
        if version is None or not version:
            return False
        if not CondaCmd.env_activated():
            return False
        if CondaCmd.env_activate('any_env_name'):
            return False
        t = CondaCmd.env_most_recent_change()
        if t < 0:
            return False
        return True


def main():
    if not CondaCmd.selftest():
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
