# setup.py

from distutils.core import setup, Extension

setup(name="controller",
      py_modules=['controller'], 
      ext_modules=[Extension("_controller",
                     ["controller.i","controller.c"],
                  )]
      
)
