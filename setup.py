from cx_Freeze import setup, Executable
import sys
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["pyqt5"]}

# GUI applications require a different base on Windows
# (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "환자상담관리",
        version = "0.1",
        description = "CRM",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])