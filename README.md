# qbitUni — Quantum Universe Simulator

s/o Gemini....

# Installation

```bash
git clone https://github.com/imesh97/qbit-universe.git
```

# Setup

**Note:** _This project uses Python 3.13._

_Create and run a virtual environment_

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Tests

```bash
python3 tests/gates.py
python3 tests/melinda.py
```

## Running your first simulation

```python
from qbitUni import QbitUni

# ⚡ Initialize a 2-qubit Universe
# This allocates the state vector in C memory
univ = QbitUni(2)

# ⊹ Apply a Hadamard gate to Qubit 0
# This puts Qubit 0 into a 50/50 superposition of |0> and |1>
univ.h(0)

# 🎛️ Apply a CNOT (Controlled-NOT) gate
# Control: Qubit 0, Target: Qubit 1
# This 'links' the two qubits together (Entanglement)
univ.cnot(0, 1)

# 🧮 Peek at the Math
# Check the probability of the universe being in state |00> or |11>
print(f"Prob of |00>: {univ.get_prob(0):.2f}")
print(f"Prob of |11>: {univ.get_prob(3):.2f}")

# 🌊 Collapse the Wavefunction
# Measuring will force the universe into a single classical state
result = univ.measure()
print(f"Final Measurement: {result:02b}")
```
