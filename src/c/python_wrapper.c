#define PY_SSIZE_T_CLEAN
#include <Python.h>

// PyMODINIT_FUNC handles the 'export' logic for different operating systems
PyMODINIT_FUNC PyInit__engine(void) {
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_engine",
        NULL,
        -1,
        NULL
    };
    return PyModule_Create(&moduledef);
}