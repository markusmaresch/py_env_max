#
# -*- coding: utf-8 -*-
#
import sys

print('\nimport_some start')

try:
    import iso8601
    print('iso8601=={}'.format(iso8601.UTC))

    import python_socks
    print('python_socks=={}'.format(python_socks.__version__))

    import tiledb
    print('tiledb=={}'.format(tiledb.__version__))

    import tinycss2
    print('tinycss2=={}'.format(tinycss2.__version__))

    import zarr
    print('zarr=={}'.format(zarr.__version__))

    import clang
    print('clang=={}'.format(clang))

    import six
    print('six=={}'.format(six.__version__))

    import gast
    print('gast=={}'.format(gast))

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
