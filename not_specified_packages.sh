#!/bin/bash
#
# list installed packages, that are NOT in requirements
#
requirements="requirements_miniconda.txt"
cc_tmp="conda_created.tmp"

grep CONDA_CREATE $requirements | \
  awk '{print $1}' | sed -e "s/^#//g" > $cc_tmp

(
  echo "Package"
  echo "-----------------------------"
  echo "dask"
  #echo "ruamel.yaml"
  #echo "ruamel.yaml.clib"
) >> $cc_tmp

for p in $(pip list | awk '{print $1}'); do
  grep -q -i "^${p}==" $requirements
  if [ $? -ne 0 ]; then
    #echo "Possible: $p"
    grep -q -i "^${p}$" $cc_tmp
    if [ $? -ne 0 ]; then
      version=$(pip show $p | grep -e "^Version: " | awk '{print $2}')
      echo "Not specified: ${p}==${version}"
    fi
  fi
done

rm -f $cc_tmp