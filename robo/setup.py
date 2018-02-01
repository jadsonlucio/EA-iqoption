from cx_Freeze import setup, Executable
import sys
import os


os.environ['TCL_LIBRARY'] = r'C:\Users\Pain panda\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Pain panda\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

includes = ['tkinter']
include_files = [r"C:\Users\Pain panda\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll", \
                 r"C:\Users\Pain panda\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll","files","Tesseract-OCR"]
base = 'Win32GUI' if sys.platform == 'win32' else None


setup(name='RoboIQ', version='0.9', description='Robo para operações IQ',
      options={"build_exe": {"includes": includes, "include_files": include_files}},
      executables=[Executable('main.py', base=None,icon="iqoptionicon.ico")])