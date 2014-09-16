import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages":
                     "PyQt4,sip,encodings.utf_8,pystache,modcommon,mod,rdflib".split(","),
                     "include_files": [("mod-ui/html", "html"), ("mod-host/mod-host", "mod-host/mod-host")],
                     "excludes": ['Tkinter',],
                    }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "MOD UI",
        version = "0.1",
        description = "MOD UI",
        options = {"build_exe": build_exe_options},
        executables = [Executable("mod-lv2-host.py", base=base)])
