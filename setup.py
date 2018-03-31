from distutils.core import setup
import py2exe
 
setup(
    windows=[{"script":"main.py"}],
    options={"py2exe": {"includes":["main_window","client_window","doctor_window","archive_window","PyQt5"]}},
    zipfile=None
)