#!/bin/bash

if ! python levels_check.py; then
  exit 1
fi

if ! python pip_show_all.py; then
  exit 1
fi

./not_specified_packages.sh

exit 0
