#!/bin/bash
#
# need to look at: pip, setuptools, wheel ...
#
for p in $(pip list | awk '{print $1}'); do
  grep -q -i "^${p}==" requirements_miniconda.txt
  if [ $? -ne 0 ]; then
    echo $p
  fi
done