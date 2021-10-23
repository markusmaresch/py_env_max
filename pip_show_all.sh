#!/bin/bash
#
# create pip_show_all.txt ... takes a while
#
pip_show_all="pip_show_all.txt"

echo "Recreate/Update ${pip_show_all} ? (will take a while) (Y/CTRL-C)"
read ans

rm -f $pip_show_all
for p in $(pip list | awk '{print $1}' | grep -v -e "Package" -e "^--------"); do
  echo "======== ${p} BELOW"
  pip show $p
  echo "======== ${p} ABOVE"
done | tee -a $pip_show_all

