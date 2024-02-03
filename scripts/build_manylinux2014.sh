#!/bin/bash
set -e
set -u
yum install -y bison flex
mkdir -p build_macos
# automatically copied to lib directory
(cd build_macos && cmake -DCMAKE_BUILD_TYPE=RELEASE .. && make -j4)
# need to create pip package for each platform
export PYTHON3_BIN=python3.7
export PIP_BIN=/opt/python/cp37-cp37m/bin/pip
${PIP_BIN} install wheel auditwheel setuptools
${PIP_BIN} wheel .
for i in *.whl; do auditwheel repair ${i}; done
rm *.whl
mv wheelhouse/*.whl .
