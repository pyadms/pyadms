#!/bin/bash
set -e
set -u
mkdir -p build_macos
# automatically copied to lib directory
(cd build_macos && cmake -DCMAKE_BUILD_TYPE=RELEASE .. && make -j4)
# need to create pip package for each platform
export PYTHON3_BIN=python
export PIP_BIN=pip
${PIP_BIN} install wheel auditwheel setuptools
${PIP_BIN} wheel .
