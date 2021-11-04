#!/bin/bash

conda --version > conda_version.txt

rm -f /tmp/pipdeptree.cache

if ! python levels_check.py; then
  exit 1
fi

if ! python pip_show_all.py; then
  exit 1
fi

./not_specified_packages.sh

rm -f /tmp/pipdeptree.cache

git status
git diff

exit 0
