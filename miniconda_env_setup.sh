#!/bin/bash
#
# creates/updates conda environment based on requirements
#
py_env_name="py_env_202201"  # change/count up
python_default_version="3.9"

requirements_all="requirements_miniconda.txt"

only_check=0
only_export=0

packages_check_specified() {
  #
  # list installed packages, that are NOT in requirements
  #
  cc_tmp="/tmp/conda_created.$$.tmp"

  grep CONDA_CREATE $requirements_all | \
    awk '{print $1}' | sed -e "s/^#//g" > $cc_tmp

  (
    echo "Package"
    echo "-----------------------------"
    echo "dask"
    echo "sliderepl"
  ) >> $cc_tmp

  ret=0
  for p in $(pip list | awk '{print $1}'); do
    grep -q -i "^${p}==" $requirements_all
    if [ $? -ne 0 ]; then
      #echo "Possible: $p"
      grep -q -i "^${p}$" $cc_tmp
      if [ $? -ne 0 ]; then
        version=$(pip show $p | grep -e "^Version: " | awk '{print $2}')
        echo "Not specified: ${p}==${version}"
        ret=1
      fi
    fi
  done
  rm -f $cc_tmp
  return $ret
}

post_check_exit() {
  conda --version > conda_version.txt
  if ! python inspect_all.py; then
    exit 1
  fi
  if ! python pip_show_all.py; then
    exit 1
  fi
  if ! python levels_check.py; then
    echo "Fix errors above, before continuing"
    exit 1
  fi

  packages_check_specified
  if [ $? -ne 0 ]; then
    echo "Fix not specified packages first"
    #exit 1
  fi
  git diff
  git status
}

pip_check_exit() {
  pip_check_tmp="/tmp/pip_check.$$.tmp"
  pip check | tee $pip_check_tmp
  ret=${PIPESTATUS[0]}
  echo "pip check ret: $ret"
  ret=0 # hmm .. how to treat intermediate 'pip check' errors that get resolved with this run
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

conda_env_export() {
  yml=${py_env_name}.yml
  yml2=${py_env_name}_linux.yml
  yml_windows=${py_env_name}_windows.yml
  echo "Exporting ${yml}"
  conda env export --no-builds > ${yml}

  if [ 1 -eq 1 ]; then
    echo "Formatting for Windows"
    cat $yml | \
      grep -v \
        -e "- libffi=" \
        -e "- ncurses=" \
        -e "- readline=" \
        \
        -e "- geopandas=" \
        -e "- fiona=" \
        -e "- gensim=" \
        -e "- pybullet=" \
        -e "- netifaces=" \
        -e "- zstd=" \
        -e "- pystan=" -e "- cmdstanpy=" \
        -e "- cytools=" \
        -e "- pytype=" \
        -e "- wordcloud=" \
        -e "- pycocotools=" \
        \
        -e "- libcxx=" \
        -e "- krb5=" \
        -e "- ta-lib=" \
        -e "- python-graphviz=" \
        -e "- graphviz=" \
        \
        -e "- tbb==" \
        \
        -e "- pyodbc==" \
        \
        -e "- elegantrl==" \
        -e "- box2d=" \
        -e "- box2d-py=" \
        \
        > $yml_windows

    ls -al $yml $yml_windows
    #diff $yml $yml_windows

  fi

  if [ 1 -eq 1 ]; then
    echo "Formatting for Linux"

    # libcxx .. only osx, not in linux

    # elegantrl .. depeends on box2d*
    # box2d .. depends on swig, # fix with ONLY_OSX
    # box2d-py .. depends on swig, # fix with ONLY_OSX
    # krb5 ... depends on krb5-config, fix with ONLY_OSX
    # ta-lib .. depends on lower level C library, fix with ONLY_OSX

    # graphviz .. issue with latest version on pypi.org, fix with ONLY_OSX

    # Temporary ?
    #   prophet .. depends on numpy, could be temporary

    # Dependency missing
    #   pyodbc .. sql.h ?

    # wrong pypi version
    #   tbb .. conflicting versions

    cat $yml | \
      grep -v \
        -e "- libcxx=" \
        -e "- krb5=" \
        -e "- ta-lib=" \
        -e "- python-graphviz=" \
        -e "- graphviz=" \
        \
        -e "- tbb==" \
        \
        -e "- pyodbc==" \
        \
        -e "- elegantrl==" \
        -e "- box2d=" \
        -e "- box2d-py=" \
        \
        > $yml2

    ls -al $yml $yml2
    #diff $yml $yml2
    #mv $yml2 $yml
  fi
}

requirements_export_bare_bone() {
  req="requirements_miniconda.txt"
  grep -v -e "^#" $req | sed -e 's/#.*$//' | sed 's/^$/#/'  > req_bare_bone.txt
}


while [ "$1" != "" ]; do
  if [ "$1" == "-tmp" ]; then
    py_env_name="${py_env_name}.tmp"
    shift
    continue
  fi
  if [ "$1" == "-only-check" ]; then
    only_check=1
    shift
    continue
  fi
  if [ "$1" == "-only-export" ]; then
    only_export=1
    shift
    continue
  fi
  echo "What is: ${1} ?"
  exit 1
done

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

if [ ${only_check} -ne 0 ]; then
  post_check_exit
  exit 0
fi

if [ ${only_export} -ne 0 ]; then
  conda_env_export
  exit 0
fi


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
  sequence=$(seq 1 1 19)
  #sequence=$(seq 1 1 4; seq 5 5 15)
  for i in $sequence; do
    num=$(printf "%02d" $i)
    level_xx="LEVEL_$num"
    tags="$tags $level_xx"
  done
  #echo "Tags: $tags"
  #exit 0
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
      ncd="--no-cache-dir --no-binary :all:"
    else
      ncd=""
    fi
    #
    # issue with pip install below: need to fork off and parse for "This could take a while"
    # if found, stop/kill pip and error out
    # need to find correct implementation
    #
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

if [ 1 -eq 0 ]; then
  conda_env_export
fi
if [ 1 -eq 1 ]; then
  post_check_exit
fi

exit 0
