#!/bin/bash

conda --version > conda_version.txt

if ! python pip_show_all.py; then
  exit 1
fi

rm -f /tmp/pipdeptree.cache

if ! python levels_check.py; then
  echo "Fix errors above, before continuing"
  exit 1
fi

./not_specified_packages.sh
if [ $? -ne 0 ]; then
  echo "Fix not specified packages first"
  exit 1
fi

rm -f /tmp/pipdeptree.cache

git diff
git status

exit 0
