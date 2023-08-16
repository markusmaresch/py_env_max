# Upgrading a complex python environment from Python 3.9 to Python 3.11

* Errors
  * cmake .. ERROR: CMake must be installed to build
  * fix: pip install cmake
  *
  * llvmlite==0.39.1 ... py<3.11 .. fix with 0.40.1
  * scipy==1.9.1 .. fix with 1.9.3
  * numba==0.56.4 .. fix with 0.57.1
  * openvino==2022.3.0 .. fix with 2023.0.1
  * qcore .. fix with 1.10.0
  * torch==1.11.0  .. fix with 2.0.1
  * pyarrow .. 12.0.1
  * asynq .. fix: 2.15.1
  * Link.exe from GIT .. change in PATH !! .. fix: C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin first in path
  * 
  * proto
  * torchaudio==0.11.0
  * tensorboard==2.9.1 .. protobuf .. fix: google-auth-oauthlib-1.0.0 tensorboard-2.14.0 tensorboard-data-server-0.7.1
  * catboost .. fix: 1.2

* Problems
  * onnx, onnxconverter-common onnxoptimizer onnx-simplifier, 
  * tensorflow-metadata, tensorflow-datasets


* Hard
  * hard to see failure in *00.bat .. too long 


* Ideas
  * in bat/sh .. replace '==' with '>=' 


* Old
  * Qt5 .. --> Qt6 


* TakeAway
  * make smaller steps, like 3.9 to 3.10, and THEN to 3.11
  * check each level separately