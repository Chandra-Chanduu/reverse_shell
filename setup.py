import sys
from cx_Freeze import  setup, Executable

include_files=["autorun.inf"]
base=None

if sys.platform=="win32":
    base="Win32GUI"

setup(name="connect",version="0.1",options={"build.exe":{"include_files":include_files}},
      executables=[Executable("m_client.py",base=base)])