#!/bin/bash

req="requirements_miniconda.txt"

grep -v -e "^#" $req | sed -e 's/#.*$//' | sed 's/^$/#/'  > req_problem.txt