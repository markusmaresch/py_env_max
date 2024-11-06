import sys

from pip._internal.operations.freeze import freeze

for line in freeze():
    sys.stdout.write(line + "\n")
