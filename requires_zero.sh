#!/bin/bash
#
# TODO: exclude miniconda_basic_packages ...
# TODO: check all installed packages for correct LEVEL_00 - and not
#
for package in $(pip list | grep -v -e "^Package " -e "^--------" | awk '{print $1 }' ); do
  pip_show=$(pip show $package)
  version=$(echo "$pip_show" | grep -e "^Version: " | sed -e "s/Version: //g" )
  requires=$(echo "$pip_show" | grep -e "^Requires: " | sed -e "s/Requires: //g" )
  #echo "Package: $package |${version}| -> |$requires|"
  #continue

  if [ -n "$requires" ]; then
    continue
    echo "Package: $package ${version} -> |$requires|"
  else
    echo "${package}==${version} # LEVEL_00"
  fi
  #break
done
