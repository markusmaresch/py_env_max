#
# -*- coding: utf-8 -*-
#
import os
import sys
import subprocess
import datetime
import typing
import platform
from pathlib import Path

from functools import lru_cache


# REMOVE: conda remove --name py_env_XXX --all

class CondaCmd:

    @staticmethod
    def _is_conda_root(path: Path) -> bool:
        """Checks if a given path looks like a conda installation root."""
        return (path / "conda-meta").is_dir() and \
            (path / "envs").is_dir() and \
            (path / "pkgs").is_dir()

    @staticmethod
    @lru_cache(maxsize=1)
    def _find_conda_root() -> typing.Optional[Path]:
        """
        Attempts to find the root directory of the conda installation.
        This is typically the directory containing 'envs', 'pkgs', and 'conda-meta'.
        """
        # 1. Check CONDA_ROOT environment variable (if set by some installations)
        conda_root_env = os.environ.get('CONDA_ROOT')
        if conda_root_env and CondaCmd._is_conda_root(Path(conda_root_env)):
            return Path(conda_root_env)

        # 2. Check CONDA_PREFIX environment variable (points to current activated env)
        conda_prefix_env = os.environ.get('CONDA_PREFIX')
        if conda_prefix_env:
            env_path = Path(conda_prefix_env)
            # If CONDA_PREFIX is the root itself
            if CondaCmd._is_conda_root(env_path):
                return env_path
            # If CONDA_PREFIX is an environment within a root
            if CondaCmd._is_conda_root(env_path.parent):
                return env_path.parent

        # 3. Derive from sys.prefix (current Python environment's prefix)
        current_prefix = Path(sys.prefix)
        if CondaCmd._is_conda_root(current_prefix):
            return current_prefix
        if CondaCmd._is_conda_root(current_prefix.parent):
            return current_prefix.parent

        # 4. Search up from sys.executable's directory
        path_to_check = Path(sys.executable).parent
        for _ in range(5):  # Go up a few levels to find the root
            if CondaCmd._is_conda_root(path_to_check):
                return path_to_check
            if path_to_check == path_to_check.parent:  # Reached filesystem root
                break
            path_to_check = path_to_check.parent

        return None

    @staticmethod
    @lru_cache(maxsize=1)
    def find_conda_executable() -> str:
        """
        Find the conda binary reliably for Windows and Linux, considering multiple environments.
        Prioritizes CONDA_EXE, then searches common installation paths, then falls back to PATH.
        """
        # 1. Check CONDA_EXE environment variable (most reliable if set)
        conda_exe_env = os.environ.get('CONDA_EXE')
        if conda_exe_env and Path(conda_exe_env).is_file():
            return conda_exe_env

        # Determine OS specific executable name
        is_windows = platform.system() == 'Windows'
        conda_exec_name = 'conda.exe' if is_windows else 'conda'
        conda_bat_name = 'conda.bat'  # Specific to Windows

        potential_paths = []

        # 2. Search relative to the detected conda root
        conda_root = CondaCmd._find_conda_root()
        if conda_root:
            if is_windows:
                potential_paths.append(conda_root / "Scripts" / conda_exec_name)
                potential_paths.append(conda_root / "condabin" / conda_exec_name)
                potential_paths.append(conda_root / "condabin" / conda_bat_name)
            else:  # Linux/macOS
                potential_paths.append(conda_root / "bin" / conda_exec_name)
                potential_paths.append(conda_root / "condabin" / conda_exec_name)

        # 3. Search relative to sys.prefix (current Python environment)
        # This covers cases where conda might be installed directly in the environment
        # or if _find_conda_root failed for some reason.
        current_env_prefix = Path(sys.prefix)
        if is_windows:
            potential_paths.append(current_env_prefix / "Scripts" / conda_exec_name)
            potential_paths.append(current_env_prefix / "condabin" / conda_exec_name)
            potential_paths.append(current_env_prefix / "condabin" / conda_bat_name)
        else:  # Linux/macOS
            potential_paths.append(current_env_prefix / "bin" / conda_exec_name)
            potential_paths.append(current_env_prefix / "condabin" / conda_exec_name)

        # Remove duplicates and check existence
        # Using dict.fromkeys to preserve order and remove duplicates (Python 3.7+)
        for p in list(dict.fromkeys(potential_paths)):
            if p.is_file():
                return str(p)

        # 4. Fallback: Assume 'conda' is in PATH
        return 'conda'

    @staticmethod
    def version() -> str:
        version = ''
        conda_exe = CondaCmd.find_conda_executable()
        try:
            output = subprocess.check_output([conda_exe, '-V'], text=True)
            for line in output.splitlines():
                v = line.split()
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
        conda_exe = CondaCmd.find_conda_executable()
        try:
            output = subprocess.check_output(args=[conda_exe, 'list'], text=True).rstrip()
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
        conda_exe = CondaCmd.find_conda_executable()
        try:
            output = subprocess.check_output(args=[conda_exe, 'env', 'export'], text=True).rstrip()
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
    @lru_cache(maxsize=1)  # it does not change during runtime
    def _env_activated() -> typing.Tuple[str, str]:
        # conda env list | grep -e ' \* ' | awk '{print $1 $3}'
        conda_exe = CondaCmd.find_conda_executable()
        try:
            output = subprocess.check_output([conda_exe, 'env', 'list'], text=True)
            for line in output.splitlines():
                v = line.split()
                if len(v) < 2:
                    continue
                if v[0][0] == '#':
                    continue
                if v[1] != '*':
                    continue
                return v[0], v[2]
            # for
        except Exception as e:
            print(f'Failed: conda env list .. {e}')
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
