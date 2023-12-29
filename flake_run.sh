#!/bin/sh

r=$(command -v flake8)
if [ -z "$r" ]; then
    echo "flake8 ? .... pip install flake8"
else
    flake8 --ignore E127,E501,E722,W504 *.py
fi

r=$(command -v ruff)
if [ -z "$r" ]; then
    echo "ruff ? .... pip install ruff"
else
    ruff --ignore E501,E722 .
fi

