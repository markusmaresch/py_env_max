#!/bin/bash
#pipreqs --mode no-pin --debug --clean requirements.txt
pipreqs --mode no-pin --debug --force .
exit $?
