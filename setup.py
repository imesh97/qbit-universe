from setuptools import setup, Extension
import sys

qbit_extension = Extension(
    'qbitUni._engine',
    sources=[
        'src/c/engine.c', 
        'src/c/gates.c', 
        'src/c/python_wrapper.c'
    ],
    # This tells the compiler to look in src/c for universe.h
    include_dirs=['src/c'], 
    extra_compile_args=['-O3', '-Xpreprocessor', '-fopenmp', '-I/opt/homebrew/opt/libomp/include'] if sys.platform == 'darwin' else ['-O3', '-fopenmp'],
    extra_link_args=['-L/opt/homebrew/opt/libomp/lib', '-lomp'] if sys.platform == 'darwin' else ['-lgomp'],
)

setup(
    ext_modules=[qbit_extension],
)