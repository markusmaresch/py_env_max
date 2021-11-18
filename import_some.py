#
# -*- coding: utf-8 -*-
#
import sys

print('\nimport_some start')

try:
    import openvino
    print('openvino=={}'.format(openvino))

    import tensorflow
    print('tensorflow=={}'.format(tensorflow.__version__))
    tensorflow.cos(1.0)

    import talib
    print('talib=={}'.format(talib.__version__))

    import numpy
    print('numpy=={}'.format(numpy.__version__))

except:
    print('import_some failed\n')
    sys.exit(1)

print('import_some succeeded\n')
sys.exit(0)

