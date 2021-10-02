#!/bin/bash
#
# creates/updates conda environment based on requirements
#
python_default_version="3.9"
py_env_name="py_env_202110"  # change/count up

pip_check_exit() {
  pip check
  ret=$?
  if [ $ret != 0 ]; then
    echo
    echo "pip check failed: ret=$ret"
    echo
    exit $ret
  fi
}

env_dir="$HOME/miniconda3/envs/${py_env_name}"
if [ ! -d ${env_dir} ]; then
  echo "No Env: $env_dir .. create ?"
  read ans
  conda_create_tmp_log="conda_create_tmp.log"
  conda create --name $py_env_name python=${python_default_version} | tee $conda_create_tmp_log
  echo
  echo "New Packages:"
  grep -A100 -e "NEW packages" $conda_create_tmp_log | \
    grep -B100 -e "^Proceed" | grep -e "^  " | grep -e "::" | awk '{print $1}'
  echo
  # check above with 'CONDA_CREATE' in requirements*.txt
  rm -f $conda_create_tmp_log
else
  echo "Have Env: $env_dir .. use/update (Y/CTRL-C) ??"
  read ans
fi

echo "Activate $py_env_name .."
. $HOME/miniconda3/bin/activate $py_env_name
conda env list

requirements_all="requirements_miniconda.txt" # could be more, but this is not good to manage
#requirements_all="requirements_tmp.txt" # !!!!!!!!!!!!

lines_no_label=$(grep -v -e "^#" $requirements_all | grep -v -e '^$' | grep -v -e " LEVEL_[0-9][0-9]" | sort)
if [ -n "$lines_no_label" ]; then
  num_no_label=$(echo "$lines_no_label" | wc -l | xargs)
  echo "Unlabeled: LABEL's: $num_no_label .. need to fix first (may add the highest level used)"
  echo "--------"
  echo "$lines_no_label"
  echo "^^^^^^^^"
  exit 1
fi

cmd="pip install -r $requirements_all"
echo "Ready for: $cmd ... (Y/CTRL-C) ??"
read ans

if [ 1 -eq 1 ]; then
  # CONDA_CREATE (also LEVEL_00) .. directly from conda create, like: certifi, tk, pip ...
  # PRE_INSTALL_00 .. like numpy
  # NO_CACHE_DIR # needs to be rebuilt, like: ta-lib
  # LEVEL_01 .. like: pipdeptree
  # LEVEL_02 .. like: convertdate
  # LEVEL_03 .. like: pandas
  ##POST_INSTALL_00 # NOT_USED: after everything else, like: pystan
  tags="PRE_INSTALL_00 NO_CACHE_DIR LEVEL_01 LEVEL_02 LEVEL_03 LEVEL_04 LEVEL_05 LEVEL_06 LEVEL_07"
  for tag in $tags; do
    echo "Pre Install Tag: $tag"
    requirements_tmp="requirements_${tag}.txt"
    grep -e "${tag}" $requirements_all > $requirements_tmp
    num_lines=$(cat $requirements_tmp | wc -l | xargs)
    if [ $num_lines -lt 1 ]; then
      echo "Ignoring $requirements_tmp .. no packages !"
      rm -f $requirements_tmp
      continue
    fi
    echo "Pre-Installing $requirements_tmp .. $num_lines packages"
    if [ "$tag" == "NO_CACHE_DIR" ]; then
      ncd="--no-cache-dir"
    else
      ncd=""
    fi
    pip install $ncd -r $requirements_tmp
    pip_check_exit
    rm -f $requirements_tmp
    echo "Done: $tag"
    echo
  done
fi

#exit 0

for requirements_one in $requirements_all; do
  if [ 1 -eq 1 ]; then
    break # NOT NEEDED ANY MORE ?!
  fi
  cmd="pip install -r $requirements_one"
  $cmd
  echo
  echo "Done: $?: $cmd  ... now checking"
  pip_check_exit
done

exit 0
