import ctypes
import os
import sys

def _init_cdll():
    current_folder = os.getcwd()
    lib_folder = f"{current_folder}/lib"
    lib_name = "libPythonAPI"

    lib_extension = "so"
    if sys.platform == "win32" :
        lib_extension = "dll"

    path_to_lib = f'{lib_folder}/{lib_name}.{lib_extension}'
    global _CDLL
    _CDLL = ctypes.cdll.LoadLibrary(path_to_lib)

_CDLL = None
_init_cdll()

class CApi:
    @staticmethod
    def get_safety_ms(temp: float) -> int:
        return _CDLL.get_safety_ms(ctypes.c_float(temp))
    @staticmethod
    def get_safety_level(temp: float) -> int:
        return _CDLL.get_safety_level(ctypes.c_float(temp))


if __name__ == "__main__":
    print(CApi.get_safety_ms(50))
    print(CApi.get_safety_ms(39))
    print(CApi.get_safety_level(50))
    print(CApi.get_safety_level(39))
