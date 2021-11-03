#!/bin/bash
#
# creates/updates conda environment based on requirements
#
py_env_name="py_env_202111"  # change/count up
python_default_version="3.9"

pip_check_exit() {
  pip_check_tmp="/tmp/pip_check.$$.tmp"
  pip check | tee $pip_check_tmp
  ret=$?
  echo "pip check ret: $ret"
  if [ $ret != 0 ]; then
    other_errors=$(grep -v -e ", which is not installed.$" $pip_check_tmp | wc -l | xargs)
    echo "other_errors: $other_errors"
    if [ $other_errors -gt 0 ]; then
      echo
      echo "pip check failed: ret=$ret"
      echo
      rm -f $pip_check_tmp
      exit $ret
    fi
    echo "Ignoring not installed warnings .."
  fi
  rm -f $pip_check_tmp
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
  echo "Have Env: $env_dir ..."
  #echo "Have Env: $env_dir .. use/update (Y/CTRL-C) ??"
  #read ans
fi

echo "Activate $py_env_name .."
. $HOME/miniconda3/bin/activate $py_env_name
conda env list

requirements_all="requirements_miniconda.txt" # could be more, but this is not good to manage
#requirements_all="requirements_tmp.txt" # !!!!!!!!!!!!

lines_no_label=$(grep -v -e "^#" $requirements_all | grep -v -e '^$' | grep -v -e " LEVEL_[0-9][0-9]" | sort)
if [ -n "$lines_no_label" ]; then
  num_no_label=$(echo "$lines_no_label" | wc -l | xargs)
  echo "Unlabeled: LABEL's: $num_no_label .. need to fix first (may add as LEVEL_09)"
  echo "--------"
  echo "$lines_no_label"
  echo "^^^^^^^^"
  exit 1
fi

cmd="pip install -r $requirements_all"
echo "Ready for: $cmd ... (Y/CTRL-C) ??"
read ans

if [ 1 -eq 1 ]; then
  # PRE_INSTALL_00 .. like numpy
  # NO_CACHE_DIR # needs to be rebuilt, like: ta-lib
  # LEVEL_01 .. like: pipdeptree
  # LEVEL_02 .. like: convertdate
  # LEVEL_03 .. like: pandas
  # ...
  tags="PRE_INSTALL_00 NO_CACHE_DIR"
  for i in $(seq 1 1 19); do
    num=$(printf "%02d" $i)
    level_xx="LEVEL_$num"
    tags="$tags $level_xx"
  done
  for tag in $tags; do
    requirements_tmp="/tmp/requirements_${tag}.$$.txt"
    if [ "${tag:0:6}" = "LEVEL_" ]; then
      num=$(echo ${tag:6:7} | bc -l)
      echo "LEVEL $num"
      rm -f $requirements_tmp
      for i in $(seq $num -1 0); do
        num2=$(printf "%02d" $i)
        level_xx="LEVEL_$num2"
        grep -e "${level_xx}" $requirements_all >> $requirements_tmp
        if [ $i -eq $num ]; then
          num_lines=$(cat $requirements_tmp | wc -l | xargs)
        fi
        #cho "Adding ${level_xx} .. $num_lines"
      done
    else
      grep -e "${tag}" $requirements_all > $requirements_tmp
      num_lines=$(cat $requirements_tmp | wc -l | xargs)
    fi
    if [ $num_lines -lt 1 ]; then
      echo "Ignoring $requirements_tmp .. no more packages ..."
      echo
      rm -f $requirements_tmp
      break
    fi
    echo "Installing $requirements_tmp .. $num_lines packages"
    if [ "$tag" == "NO_CACHE_DIR" ]; then
      ncd="--no-cache-dir"
    else
      ncd=""
    fi
    pip install $ncd -r $requirements_tmp | grep -v -e "^Requirement already satisfied: "
    ret=${PIPESTATUS[0]}
    if [ $ret != 0 ]; then
      echo "pip install $ncd -r $requirements_tmp .. ret: $ret"
      exit 1
    fi
    pip_check_exit
    rm -f $requirements_tmp
    echo "Done: $tag"
    echo
  done
fi

exit 0
