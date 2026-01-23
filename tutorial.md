# qbitUni Tutorial

I recommend you read the `README.md` file for a step-by-step guide on setting up qbitUni.

I also recommend you use the qbitUni Studio, which is a web interface. It's easier, with a lot more features.

```bash
streamlit run app.py
```

---

**For Python devs:**

You should have your virtual environment, dependencies, and script ready to go.

Here's a start. Initializing the quantum universe...

```
import qbitUni as qu

# Initialize a simulation environment with 3 qubits
# The system starts in the state |000>
qu = qu.QuantumUniverse(3)
```

Single Qubit Gates:

```
qu.h(i)
    -> Hadamard Gate. Puts qubit 'i' into superposition.

qu.x(i)
    -> Pauli-X (NOT Gate). Flips 0 to 1, or 1 to 0.

qu.y(i)
    -> Pauli-Y Gate. Rotation around Y-axis.

qu.z(i)
    -> Pauli-Z Gate. Flips the phase of the |1> state.

qu.s(i)
    -> S-Gate. Adds a 90-degree phase shift.

qu.t(i)
    -> T-Gate. Adds a 45-degree phase shift.
```

Multi Qubit Gates:

```
qu.cnot(c, t)
    -> Controlled-NOT. Flips target 't' if control 'c' is 1.

qu.cz(c, t)
    -> Controlled-Z. Flips phase if both 'c' and 't' are 1.

qu.toffoli(c1, c2, t)
    -> Toffoli Gate (CCX). Flips target 't' only if 'c1' AND 'c2' are 1.

qu.swap(a, b)
    -> Swaps the quantum states of qubits 'a' and 'b'.
```

Parametric Rotations:

```
qu.rx(i, theta)
    -> Rotate qubit 'i' by 'theta' radians around the X-axis.

qu.phase(i, theta)
    -> Phase gate 'i' by 'theta' radians.
```

Measurement:

```
val = qu.measure_qubit(i)
    -> Collapses the wavefunction of qubit 'i'.
    -> Returns an integer: 0 or 1.
```

## Example Operation

Create an entangled Bell Pair.

```
import qbitUni as qu

# 1. Create Environment
qu = qu.QuantumUniverse(2)

# 2. Apply Gates
qu.h(0)          # Put q[0] in superposition
qu.cnot(0, 1)    # Entangle q[0] with q[1]

# 3. Measure
m0 = qu.measure_qubit(0)
m1 = qu.measure_qubit(1)

print(f"Result: {m0}{m1}")
# Output will be roughly 50% "00" and 50% "11"
```
