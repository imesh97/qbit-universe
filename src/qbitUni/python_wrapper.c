#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <complex.h>
#include "universe.h"
#include "science.h"
#include "gates.h"
#include "utils.h"

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

static PyObject* Py_x(PyQuantumUniverse *self, PyObject *args) {
    int target;
    if (!PyArg_ParseTuple(args, "i", &target)) return NULL;
    apply_x(self->univ, target);
    Py_RETURN_NONE;
}

static PyObject* Py_y(PyQuantumUniverse *self, PyObject *args) {
    int target;
    if (!PyArg_ParseTuple(args, "i", &target)) return NULL;
    apply_y(self->univ, target);
    Py_RETURN_NONE;
}

static PyObject* Py_t(PyQuantumUniverse *self, PyObject *args) {
    int target;
    if (!PyArg_ParseTuple(args, "i", &target)) return NULL;
    apply_t(self->univ, target);
    Py_RETURN_NONE;
}

static PyObject* Py_phase(PyQuantumUniverse *self, PyObject *args) {
    int target;
    double angle;
    // Parse "id" = Integer (target), Double (angle)
    if (!PyArg_ParseTuple(args, "id", &target, &angle)) return NULL;
    
    apply_phase(self->univ, target, angle);
    Py_RETURN_NONE;
}

static PyObject* Py_swap(PyQuantumUniverse *self, PyObject *args) {
    int q1, q2;
    if (!PyArg_ParseTuple(args, "ii", &q1, &q2)) return NULL;
    apply_swap(self->univ, q1, q2);
    Py_RETURN_NONE;
}

static PyObject* Py_cz(PyQuantumUniverse *self, PyObject *args) {
    int c, t;
    if (!PyArg_ParseTuple(args, "ii", &c, &t)) return NULL;
    apply_cz(self->univ, c, t);
    Py_RETURN_NONE;
}

static PyObject* Py_toffoli(PyQuantumUniverse *self, PyObject *args) {
    int c1, c2, t;
    if (!PyArg_ParseTuple(args, "iii", &c1, &c2, &t)) return NULL;
    apply_toffoli(self->univ, c1, c2, t);
    Py_RETURN_NONE;
}

// 5. Data Retrieval Methods
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

static PyObject* Py_measure_all(PyQuantumUniverse *self) {
    long long res = measure_all(self->univ);
    return PyLong_FromLongLong(res);
}

static PyObject* Py_measure_qubit(PyQuantumUniverse *self, PyObject *args) {
    int target;
    if (!PyArg_ParseTuple(args, "i", &target)) return NULL;

    if (target < 0 || target >= self->univ->n_qubits) {
        PyErr_SetString(PyExc_ValueError, "Target qubit index out of range");
        return NULL;
    }

    int result = measure_qubit(self->univ, target);
    return PyLong_FromLong(result);
}

static PyObject* Py_apply_noise(PyQuantumUniverse *self, PyObject *args) {
    int target;
    double prob;
    if (!PyArg_ParseTuple(args, "id", &target, &prob)) return NULL;
    
    apply_noise(self->univ, target, prob);
    Py_RETURN_NONE;
}

static PyObject* Py_get_expectation(PyQuantumUniverse *self, PyObject *args) {
    int target;
    if (!PyArg_ParseTuple(args, "i", &target)) return NULL;
    
    double val = get_expectation(self->univ, target);
    return Py_BuildValue("d", val);
}

static PyObject* Py_print_state(PyQuantumUniverse *self) {
    print_state(self->univ);
    Py_RETURN_NONE;
}

// 6. Method Table
static PyMethodDef PyQuantumUniverse_methods[] = {
    {"h", (PyCFunction)Py_h, METH_VARARGS, "Apply Hadamard gate (Superposition)"},
    {"z", (PyCFunction)Py_z, METH_VARARGS, "Apply Pauli-Z gate (Phase Flip)"},
    {"s", (PyCFunction)Py_s, METH_VARARGS, "Apply S gate (PI/2 Phase)"},
    {"t", (PyCFunction)Py_t, METH_VARARGS, "Apply T gate (PI/4 Phase)"},
    {"cnot", (PyCFunction)Py_cnot, METH_VARARGS, "Apply CNOT gate (control, target)"},
    {"x", (PyCFunction)Py_x, METH_VARARGS, "Apply Pauli-X gate (NOT)"},
    {"y", (PyCFunction)Py_y, METH_VARARGS, "Apply Pauli-Y gate (Complex Swap)"},
    {"phase", (PyCFunction)Py_phase, METH_VARARGS, "Apply Phase gate (radians)"},
    {"swap", (PyCFunction)Py_swap, METH_VARARGS, "Apply Swap gate (control, target)"},
    {"cz", (PyCFunction)Py_cz, METH_VARARGS, "Apply CZ gate (control, target)"},
    {"toffoli", (PyCFunction)Py_toffoli, METH_VARARGS, "Apply Toffoli gate (control1, control2, target)"},
    {"get_amplitude", (PyCFunction)Py_get_amplitude, METH_VARARGS, "Get complex amplitude at index"},
    {"get_prob", (PyCFunction)Py_get_prob, METH_VARARGS, "Get probability at index"},
    {"measure_all", (PyCFunction)Py_measure_all, METH_NOARGS, "Collapse and measure the universe"},
    {"measure_qubit", (PyCFunction)Py_measure_qubit, METH_VARARGS, "Collapse and measure a single qubit"},
    {"apply_noise", (PyCFunction)Py_apply_noise, METH_VARARGS, "Apply depolarizing noise to a qubit"},
    {"get_expectation", (PyCFunction)Py_get_expectation, METH_VARARGS, "Get <Z> expectation value of a qubit"},
    {"print_state", (PyCFunction)Py_print_state, METH_NOARGS, "Print the state of the universe"},
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