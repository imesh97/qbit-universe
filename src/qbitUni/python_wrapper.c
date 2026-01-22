#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <complex.h>
#include "universe.h"
#include "gates.h"

// 1. The Object Structure
typedef struct {
    PyObject_HEAD
    Universe *univ;
} PyQuantumUniverse;

// 2. Destructor (Automatic Memory Management)
static void PyQuantumUniverse_dealloc(PyQuantumUniverse *self) {
    if (self->univ) {
        destroy_universe(self->univ);
    }
    Py_TYPE(self)->tp_free((PyObject *) self);
}

// 3. Constructor: univ = QuantumUniverse(n_qubits)
static int PyQuantumUniverse_init(PyQuantumUniverse *self, PyObject *args, PyObject *kwds) {
    int n_qubits;
    if (!PyArg_ParseTuple(args, "i", &n_qubits)) return -1;
    
    self->univ = init_universe(n_qubits);
    if (!self->univ) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate Quantum Universe memory.");
        return -1;
    }
    return 0;
}

// 4. Gate Methods
static PyObject* Py_h(PyQuantumUniverse *self, PyObject *args) {
    int target;
    if (!PyArg_ParseTuple(args, "i", &target)) return NULL;
    apply_hadamard(self->univ, target);
    Py_RETURN_NONE;
}

static PyObject* Py_z(PyQuantumUniverse *self, PyObject *args) {
    int target;
    if (!PyArg_ParseTuple(args, "i", &target)) return NULL;
    apply_z(self->univ, target);
    Py_RETURN_NONE;
}

static PyObject* Py_s(PyQuantumUniverse *self, PyObject *args) {
    int target;
    if (!PyArg_ParseTuple(args, "i", &target)) return NULL;
    apply_s(self->univ, target);
    Py_RETURN_NONE;
}

static PyObject* Py_cnot(PyQuantumUniverse *self, PyObject *args) {
    int ctrl, targ;
    if (!PyArg_ParseTuple(args, "ii", &ctrl, &targ)) return NULL;
    apply_cnot(self->univ, ctrl, targ);
    Py_RETURN_NONE;
}

// 5. Data Retrieval Methods (Fixes your Test Error)
static PyObject* Py_get_amplitude(PyQuantumUniverse *self, PyObject *args) {
    long long index;
    if (!PyArg_ParseTuple(args, "L", &index)) return NULL;

    if (index < 0 || index >= self->univ->dim) {
        PyErr_SetString(PyExc_IndexError, "Index out of bounds");
        return NULL;
    }

    double complex amp = self->univ->psi[index];
    return PyComplex_FromDoubles(creal(amp), cimag(amp));
}

static PyObject* Py_get_prob(PyQuantumUniverse *self, PyObject *args) {
    long long index;
    if (!PyArg_ParseTuple(args, "L", &index)) return NULL;
    
    double p = get_probability(self->univ, index);
    return PyFloat_FromDouble(p);
}

static PyObject* Py_measure(PyQuantumUniverse *self) {
    long long res = measure_all(self->univ);
    return PyLong_FromLongLong(res);
}

// 6. Method Table
static PyMethodDef PyQuantumUniverse_methods[] = {
    {"h", (PyCFunction)Py_h, METH_VARARGS, "Apply Hadamard gate to target qubit"},
    {"z", (PyCFunction)Py_z, METH_VARARGS, "Apply Z (Phase Flip) gate"},
    {"s", (PyCFunction)Py_s, METH_VARARGS, "Apply S (PI/2 Phase) gate"},
    {"cnot", (PyCFunction)Py_cnot, METH_VARARGS, "Apply CNOT gate (control, target)"},
    {"get_amplitude", (PyCFunction)Py_get_amplitude, METH_VARARGS, "Get complex amplitude at index"},
    {"get_prob", (PyCFunction)Py_get_prob, METH_VARARGS, "Get probability at index"},
    {"measure", (PyCFunction)Py_measure, METH_NOARGS, "Collapse and measure the universe"},
    {NULL, NULL, 0, NULL}
};

// 7. Type Definition
static PyTypeObject PyQuantumUniverseType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "qbitUni.QuantumUniverse",
    .tp_doc = "Quantum Universe Object",
    .tp_basicsize = sizeof(PyQuantumUniverse),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc) PyQuantumUniverse_init,
    .tp_dealloc = (destructor) PyQuantumUniverse_dealloc,
    .tp_methods = PyQuantumUniverse_methods,
};

// 8. Module Definition
static struct PyModuleDef engine_module = {
    PyModuleDef_HEAD_INIT,
    "_engine",
    NULL,
    -1,
    NULL
};

PyMODINIT_FUNC PyInit__engine(void) {
    PyObject *m;
    if (PyType_Ready(&PyQuantumUniverseType) < 0) return NULL;

    m = PyModule_Create(&engine_module);
    if (m == NULL) return NULL;

    Py_INCREF(&PyQuantumUniverseType);
    PyModule_AddObject(m, "QuantumUniverse", (PyObject *) &PyQuantumUniverseType);
    return m;
}