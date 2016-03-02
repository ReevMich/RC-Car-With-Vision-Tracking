# setup.py

from distutils.core import setup, Extension

setup(name="controller",
      py_modules=['ControllerModule'], 
      ext_modules=[Extension("_ControllerModule",
                     ["controller.i","controller.c"],
                  )]
      
)
