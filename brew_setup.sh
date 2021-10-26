#!/bin/bash

install_ta_lib() {

  # TA-LIB OsX
  brew install ta-lib # https://ta-lib.org #Technical Analysis Library

  # TA-LIB Ubuntu - not fixed yet

  # sudo apt-get update
  # sudo apt-get install build-essential
  # sudo apt install build-essential wget -y
  # sudo apt-get install python-dev
  # wget https://artiya4u.keybase.pub/TA-lib/ta-lib-0.4.0-src.tar.gz
  # tar -xvf ta-lib-0.4.0-src.tar.gz
  # cd ta-lib/
  # ./configure --prefix=/usr
  # make
  # sudo make install

  #####

  # sudo pip install -U setuptools
  # fails for lack of memory .. needs 2GBs, 0.5GBs not enough

  # https://stackoverflow.com/questions/44757678/python-ta-lib-install-error-how-solve-it

  #########
}

other_installs_jupyter() {
  #
  # not working ..
  #
  # https://nodejs.org/en/download ..
  # for Node.js and npm
  jupyter labextension install @jupyter-widgets/jupyterlab-manager
  jupyter labextension install @bokeh/jupyter_bokeh
}

brew install libomp   # for xgboost

brew install graphviz # needed to get 'dot' working
# brew install gprof2dot # not tried

# docker for kafka
brew install docker ## was: brew cask install docker

# ffmpeg for udemy-dl
brew install ffmpeg

# for box2d-py
brew install swig
