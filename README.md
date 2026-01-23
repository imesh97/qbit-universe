# qbitUni — Quantum Universe Simulator

_s/o Gemini...._

# About

qbitUni (qu) is a quantum simulator that allows you to simulate a quantum environment locally -- with operations. We use a C engine to perform the quantum operations and a Python wrapper to interface.

We have a test suite in `tests/`. Try the OpenQASM parser too!

## 🚀 Features

- **Core Engine:** Written in C with multithreading.
- **Universality:** Supports all standard gates (H, X, Y, Z, S, T, CNOT, CZ, Toffoli, RX, Phase).
- **Scientific Tools:** Expectation Value `<Z>` calculation and Noise Simulation for VQE. Benchmarks, too.
- **Compatibility:** Includes an OpenQASM 2.0 parser.
- **Visualization:** Built-in ASCII Bloch Spheres and Histograms.

# Installation

```bash
git clone https://github.com/imesh97/qbit-universe.git
```

# Setup

**Note:** _This project uses Python 3.13._

Create and run a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

# Test Suite

```bash
python3 tests/gates.py
python3 tests/melinda.py
python3 tests/xy.py
python3 tests/parallel.py
python3 tests/universality.py
python3 tests/teleport.py
python3 tests/grover.py
python3 tests/science.py
python3 tests/visuals.py
python3 tests/energy.py
python3 tests/qasm/run.py

python3 tests/benchmark.py
```

## Running your first simulation

### 1. Code

Create `script.py` file for this test.

```python
# 📚 Import the Quantum Universe from Qbit
import qbitUni as qu

# ⚡ Initialize a 2-qubit Universe
# This allocates the state vector in C memory
univ = qu.QuantumUniverse(2)
univ.print_state() # Print initial state
# (Notice the |00> state only -- as the other |01>, |10>, |11> are all 0 -- we only print probabilities > 0.01%)

# ⊹ Apply a Hadamard gate to Qubit 0
# This puts Qubit 0 into a 50/50 superposition of |0> and |1>
univ.h(0)
univ.print_state() # Print state after Hadamard

# 🎛️ Apply a CNOT (Controlled-NOT) gate
# Control: Qubit 0, Target: Qubit 1
# This 'links' the two qubits together (Entanglement)
univ.cnot(0, 1)
univ.print_state() # Print state after CNOT

# 🧮 Peek at the Math
# Check the probability of the universe being in state |00> or |11>
print(f"Prob of |00>: {univ.get_prob(0):.2f}")
print(f"Prob of |11>: {univ.get_prob(3):.2f}")

# 🌊 Collapse the Wavefunction
# Measuring will force the universe into a single classical state
result = univ.measure_all()
print(f"Final Measurement: {result:02b}")

univ.print_state() # Print state after collapse
```

### 2. Execute

```bash
python3 script.py
```
