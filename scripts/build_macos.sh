#!/bin/bash
set -e
set -u
mkdir -p build_macos
# automatically copied to lib directory
(cd build_macos && cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64" .. && make -j4)
# need to create pip package for each platform
python3 -mvenv venv
source venv/bin/activate
pip install wheel setuptools
python3 setup.py bdist_wheel;
mv dist/*.whl .
