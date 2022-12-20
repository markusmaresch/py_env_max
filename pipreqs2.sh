#!/bin/bash
pipreqs --mode no-pin --debug --clean requirements.txt
exit $?
