import ctypes
from . import _engine

# 1. Define the C Structure in Python
# This must match the 'Universe' struct in your universe.h
class UniverseStruct(ctypes.Structure):
    _fields_ = [
        ("n_qubits", ctypes.c_int),
        ("dim", ctypes.c_longlong),
        ("psi", ctypes.POINTER(ctypes.c_double)) # Treated as a flat array of doubles
    ]

# 2. Load the C library
lib = ctypes.CDLL(_engine.__file__)

# 3. Setup Function Signatures
lib.init_universe.restype = ctypes.POINTER(UniverseStruct)
lib.init_universe.argtypes = [ctypes.c_int]

lib.destroy_universe.argtypes = [ctypes.POINTER(UniverseStruct)]

# Gate Argtypes: (Universe*, int target)
gate_args = [ctypes.POINTER(UniverseStruct), ctypes.c_int]
lib.apply_hadamard.argtypes = gate_args
lib.apply_z.argtypes = gate_args
lib.apply_s.argtypes = gate_args

# CNOT: (Universe*, int control, int target)
lib.apply_cnot.argtypes = [ctypes.POINTER(UniverseStruct), ctypes.c_int, ctypes.c_int]

# Probability: (Universe*, long long index)
lib.get_probability.restype = ctypes.c_double
lib.get_probability.argtypes = [ctypes.POINTER(UniverseStruct), ctypes.c_longlong]

# Measurement: (Universe*)
lib.measure_all.restype = ctypes.c_longlong
lib.measure_all.argtypes = [ctypes.POINTER(UniverseStruct)]

# 4. The Python Class Interface
class QbitUni:
    def __init__(self, n_qubits):
        self.u = lib.init_universe(n_qubits)
        if not self.u:
            raise MemoryError(f"Failed to allocate {1 << n_qubits} states in RAM!")
        self.n_qubits = n_qubits
        self.dim = 1 << n_qubits

    def h(self, target):
        lib.apply_hadamard(self.u, target)

    def cnot(self, control, target):
        lib.apply_cnot(self.u, control, target)

    def z(self, target):
        lib.apply_z(self.u, target)

    def s(self, target):
        lib.apply_s(self.u, target)

    def get_prob(self, index):
        """Returns the probability of the state at the given index."""
        return lib.get_probability(self.u, index)

    def measure(self):
        """Collapses the universe and returns the observed state index."""
        return lib.measure_all(self.u)

    def get_amplitude(self, index):
        """Returns the raw complex amplitude (real + imag*j)."""
        if index < 0 or index >= self.dim:
            raise IndexError("Index out of universe bounds")
        
        # In C, 'double complex' is stored as: [real0, imag0, real1, imag1...]
        # We access the flat double pointer (psi) at 2*index and 2*index + 1
        real = self.u.contents.psi[2 * index]
        imag = self.u.contents.psi[2 * index + 1]
        return complex(real, imag)