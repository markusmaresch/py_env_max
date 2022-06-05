#!/bin/bash
#
# only works for non minimal environments with gprof2dot and dot
#
cmd="py_env_max.py -ei"
#
cprof="cProfile.cprof"
png="cProfile.png"
python -m cProfile -o $cprof $cmd
gprof2dot -f pstats $cprof | dot -Tpng -o $png
echo
ls -al $cprof $png
echo
echo "Type: open $png"
exit 0