#!/bin/bash

# shell version of installing packages interactively
# --> convert this to python conceptually

IFS=$'\n'
installed=".installed.txt"
pip list | awk '{print $1}' > $installed

left_over="left_over.txt"
rm -f $left_over

for p in `cat env_needed.txt`; do
  grep -q -e "^${p}$" $installed
  if [ $? -eq 0 ]; then
    echo "Already installed: $p"
    continue
  fi

  echo
  echo
  echo "Dry install: $p"
  pip install --dry-run $p
  if [ $? -ne 0 ]; then
    echo "Broken: $p ?"
    continue
  fi

  echo "Install $p ?"
  read key
  if [ "$key" == "y" ]; then
    pip install $p
    pip check
    if [ $? -ne 0 ]; then
      echo "pip check broken: $p"
      break
    fi
  else
    echo "Skipping: $p"
    echo "$p" >> $left_over
  fi
done

rm f $installed

exit 0