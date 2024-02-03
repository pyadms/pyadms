call conda create -y -n pyadms_build python cmake
call conda activate pyadms_build
mkdir build
cd build
cmake -G "Visual Studio 17 2022" -A "x64" ..
cmake --build . --config Release -- /m /nologo /verbosity:minimal
pip install wheel
pip wheel .
