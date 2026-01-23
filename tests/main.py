import qbitUni as qu  # ~main_test

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
