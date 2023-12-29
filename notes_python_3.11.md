# Upgrading a complex python environment from Python 3.9 to Python 3.11

* Errors
  * cmake .. ERROR: CMake must be installed to build
  * fix: pip install cmake


* Problems
  * onnx, onnxconverter-common onnxoptimizer onnx-simplifier, 
  * tensorflow-metadata, tensorflow-datasets


* Hard
  * hard to see failure in *00.bat .. too long 


* TakeAway
  * make smaller steps, like 3.9 to 3.10, and THEN to 3.11
  * check each level separately