#!/bin/bash

r=$(command -v flake8)
if [ -z "$r" ]; then
    echo "flake8 ? .... pip install flake8"
else
    args="-v --ignore E127,E501,E722,W504,E203"
    echo "FLAKE8 $args"
    flake8 $args
    ret=$?
    #echo
    if [ $ret -eq 0 ]; then
      echo "FLAKE8 all good"
    else
      echo "FLAKE8: $ret .. ERROR"
      exit $ret
    fi
fi

echo
r=$(command -v ruff)
if [ -z "$r" ]; then
    echo "ruff ? .... pip install ruff"
else
    echo "RUFF"
    #ruff --ignore E501,E722 .
    # E722 .. bare except
    ruff --ignore E722 .
    ret=$?
    #echo
    if [ $ret -eq 0 ]; then
      echo "RUFF all good"
    else
      echo "RUFF: $ret .. ERROR"
      exit $ret
    fi
fi
exit 0

#### example of .flake8 below

[flake8]
ignore = E302, E501, F401, F403
max-line-length = 100
max-complexity = 18