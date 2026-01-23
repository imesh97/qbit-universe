from setuptools import setup, Extension, find_packages

qbit_extension = Extension(
    'qbitUni._engine',
    sources=[
        'src/qbitUni/engine.c',
        'src/qbitUni/gates.c',
        'src/qbitUni/gates_kernel.c',
        'src/qbitUni/thread.c',
        'src/qbitUni/utils.c',
        'src/qbitUni/science.c',
        'src/qbitUni/python_wrapper.c'
    ],
    include_dirs=['src/qbitUni'],
    # Standard optimization, no threading libraries linked
    extra_compile_args=['-O3'], 
)

setup(
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    ext_modules=[qbit_extension],
)