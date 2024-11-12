# C API for Medoc Python API 

This API wraps some functionality of the Python API in a C dll.

## Building

The C library builds using CMake, to build run the following commands:

``` bash
mkdir build
cd build

cmake ..
cmake --build .
```

*You can specify release/debug builds as such:*
``` bash
# Debug
cmake .. DCMAKE_BUILD_TYPE=Debug
# Release:
cmake .. DCMAKE_BUILD_TYPE=Release
```

The library file will be in `build/libPythonAPI.so` on Windows or `build/libPythonAPI.so` on unix platforms.
To use the library copy it to the `Python-Api` repository's `lib/` folder.
