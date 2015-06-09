#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys as _sys

def start():
    print("{0}  starting PySaved  {0}".format('*'*15))
    
    pyMajor, pyMinor, pyMicro = __test_Python()
    pyInstaller = __test_PyInstaller()
    __test_wxPython()
    
    print("using Python {}.{}.{} and PyInstaller {}\n".format(pyMajor, pyMinor, pyMicro, pyInstaller))
    
    from frame import start_frame
    start_frame()

def __error(msg):
    print("\n{0}  {1}  {0}\nQuit...".format('*'*3, msg))
    _sys.exit(1)

def __test_PyInstaller():
    try:
        from PyInstaller import get_version
        return get_version()
    except ImportError:
        __error("cannot import PyInstaller")

def __test_Python():
    v = _sys.version_info
    if not (v.major == 2 and v.minor in [6,7]):
        __error("you need Python 2.6-2.7 - Python {}.{}.{} found".format(v.major, v.minor, v.micro))
    return v.major, v.minor, v.micro

def __test_wxPython():
    try:
        import wx as _
    except ImportError:
        __error("you need wxPython to run PySaved")

if __name__ == "__main__":
    start()