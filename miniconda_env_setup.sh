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
  conda create --name $py_env_name python=${python_default_version}
else
  echo "Have Env: $env_dir .. use/update (Y/CTRL-C) ??"
  read ans
fi

echo "Activate $py_env_name .."
. $HOME/miniconda3/bin/activate $py_env_name
conda env list

requirements_all="requirements_miniconda.txt" # could be more, but this is not good to manage
#requirements_all="requirements_tmp.txt" # !!!!!!!!!!!!

cmd="pip install -r $requirements_all"
echo "Ready for: $cmd ... (Y/CTRL-C) ??"
read ans

if [ 1 -eq 1 ]; then
  # numpy .. PRE_INSTALL_00
  # independant .. LEVEL_00
  # LEVEL_01
  # LEVEL_02
  # TA-lib .. NO_CACHE_DIR  # needs to be rebuilt
  # pystan .. POST_INSTALL_00
  tags="PRE_INSTALL_00 LEVEL_00 LEVEL_01 LEVEL_02 NO_CACHE_DIR POST_INSTALL_00"
  for tag in $tags; do
    echo "Pre Install Tag: $tag"
    requirements_tmp="requirements_${tag}.txt"
    grep -e "${tag}" $requirements_all > $requirements_tmp
    echo "Pre-Installing $requirements_tmp .."
    if [ "$tag" == "NO_CACHE_DIR" ]; then
      ncd="--no-cache-dir"
    else
      ncd=""
    fi
    pip install $ncd -r $requirements_tmp
    pip_check_exit
    echo "Done"
    rm -f $requirements_tmp
  done
fi

#exit 0

if [ 0 -eq 1 ]; then
  #
  # migrate this to ordered list of installs .. before everything else AND observe dependencies
  #
  pip_list="pip.list.tmp"
  pip list > $pip_list
  pres="numpy Cython six Pillow pystan pandas convertdate LunarCalendar holidays tqdm" # pandas here ????
  pres="numpy Cython" # six Pillow pystan pandas convertdate LunarCalendar holidays tqdm" # pandas here ????
  for pre in $pres; do
    vrsn=$(cat $pip_list | grep -e "^${pre} " | xargs)
    lines=$(echo $vrsn | wc -l | xargs)
    if [ -n "$vrsn" -a $lines -eq 1 ]; then
      echo "Appears we have $pre .. $vrsn"
      continue
    fi
    requirements_tmp="requirements_${pre}.txt"
    grep -e ^${pre} $requirements_all > $requirements_tmp
    echo "Pre-Installing $requirements_tmp .."
    pip install -r $requirements_tmp
    pip_check_exit
    echo "Done"
    rm -f $requirements_tmp
    pip list > $pip_list # update, it could have changed
  done
  rm -f $pip_list
fi

for requirements_one in $requirements_all; do
  cmd="pip install -r $requirements_one"
  $cmd
  echo
  echo "Done: $?: $cmd  ... now checking"
  pip_check_exit
done
exit 0
