#!/bin/bash

conda --version > conda_version.txt

rm -f pipdeptree.cache

if ! python levels_check.py; then
  exit 1
fi

if ! python pip_show_all.py; then
  exit 1
fi

./not_specified_packages.sh

rm -f pipdeptree.cache
exit 0
