""" Setup file"""
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
BUILD_EXE_OPTIONS = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
BASE = None
if sys.platform == "win32":
    BASE = "Win32GUI"

setup(name="hp_tilastotyokalu",
      version="0.1",
      description="My GUI application!",
      options={"build_exe": BUILD_EXE_OPTIONS},
      executables=[Executable("main.py", base=BASE)])
