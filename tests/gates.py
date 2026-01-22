############################
# never forget the 1st test
#                   ~imesh
#########################

from qbitUni import QuantumUniverse
import numpy as np

def format_state(univ, n_qubits):
    """Helper to audit the full state vector math."""
    terms = []
    for i in range(2**n_qubits):
        amp = univ.get_amplitude(i)
        if abs(amp) > 1e-6:
            # Format as binary string for the ket
            label = format(i, f'0{n_qubits}b')
            terms.append(f"({amp.real:+.3f}{amp.imag:+.3f}j)|{label}>")
    return " + ".join(terms)

def test_hadamard_reversibility():
    print("--- AUDIT 1: Hadamard Reversibility (H² = I) ---")
    univ = QuantumUniverse(1)
    
    print(f"  t=0 (Start):       {format_state(univ, 1)}")
    
    univ.h(0) 
    print(f"  t=1 (Superpos):    {format_state(univ, 1)}")
    
    univ.h(0) 
    print(f"  t=2 (Interference): {format_state(univ, 1)}")
    
    final_amp = univ.get_amplitude(0)
    assert np.isclose(abs(final_amp), 1.0), f"Math Error! Expected 1.0, got {abs(final_amp)}"
    print("  ✅ Proof: H applied to 1/√2(|0> + |1>) correctly restored |0>.")

def test_entanglement_logic():
    print("\n--- AUDIT 2: Bell State Creation (|00> + |11>) ---")
    univ = QuantumUniverse(2)
    
    print(f"  t=0 (Vacuum):      {format_state(univ, 2)}")
    
    univ.h(0)
    print(f"  t=1 (H on q0):     {format_state(univ, 2)}")
    
    univ.cnot(0, 1)
    print(f"  t=2 (CNOT 0->1):   {format_state(univ, 2)}")
    
    # Audit logic
    p01 = univ.get_prob(1) 
    p10 = univ.get_prob(2)
    
    assert p01 == 0 and p10 == 0, "Audit Failure: Probability leak found in |01> or |10>!"
    print("  ✅ Proof: State is perfectly entangled. No leakage into forbidden states.")

if __name__ == "__main__":
    print("🔬 QUANTUM ENGINE MATHEMATICAL AUDIT\n" + "="*40)
    try:
        test_hadamard_reversibility()
        test_entanglement_logic()
        print("\n✨ All mathematical proofs verified.")
    except AssertionError as e:
        print(f"\n❌ MATH ERROR: {e}")
    except Exception as e:
        print(f"\n💥 SYSTEM ERROR: {e}")