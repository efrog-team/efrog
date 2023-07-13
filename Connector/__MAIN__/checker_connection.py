from ctypes import CDLL, c_int, c_char_p, Structure, POINTER
import os

def compile_lib() -> None:
    if not os.path.exists(os.path.dirname(__file__).replace('\\', '/') + "/checker_files"):
        os.mkdir(os.path.dirname(__file__).replace('\\', '/') + "/checker_files")
    os.system("gcc-11 -fPIC -shared -o checker_main.so ../../Checker/main.c")

class Result(Structure):
    _fields_ = [('status', c_int),
                   ('time', c_int),
                   ('memory', c_int),
                   ('output', c_char_p),
                   ('description', c_char_p)]

def get_lib() -> CDLL:
    lib = CDLL("./checker_main.so")
    lib.create_files.argtypes = [c_int, c_char_p, c_char_p]
    lib.create_files.restype = c_int
    lib.check_test_case.argtypes = [c_int, c_int, c_char_p, c_char_p, c_char_p]
    lib.check_test_case.restype = POINTER(Result)
    lib.delete_files.argtypes = [c_int]
    lib.delete_files.restype = c_int
    return lib

if __name__ == "__main__":
    compile_lib()