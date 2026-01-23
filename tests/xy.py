# another test, too.
from qbitUni import QuantumUniverse
import time

def format_state(univ, n):
    """Audits the state vector in Dirac notation."""
    terms = []
    for i in range(1 << n):
        amp = univ.get_amplitude(i)
        if abs(amp) > 1e-6:
            label = format(i, f'0{n}b')
            terms.append(f"({amp.real:+.3f}{amp.imag:+.3f}j)|{label}>")
    return " + ".join(terms)

def test_pauli_x_y():
    print("\n--- TEST 4: Pauli X (NOT) and Y (Complex Swap) ---")
    print("Logic: X flips |0> to |1>. Y flips |1> to -i|0>.")
    sim = QuantumUniverse(1)
    
    # 1. Test X
    sim.x(0)
    print(f"  After X:   {format_state(sim, 1)}")
    assert sim.get_prob(1) == 1.0, "X-Gate Failed (Did not flip to |1>)"
    
    # 2. Test Y
    # Current state is |1>. Applying Y should result in -i|0>. So... Y|1> = -i|0>
    sim.y(0)
    print(f"  After Y:   {format_state(sim, 1)}")
    
    amp0 = sim.get_amplitude(0)
    # Check: Real ~ 0.0, Imag ~ -1.0
    assert abs(amp0.real) < 1e-6 and abs(amp0.imag + 1.0) < 1e-6, f"Y-Gate Failed! Got {amp0}"
    print("  ✅ Proof: X and Y gates are behaving according to linear algebra.")

def test_large_scale_pauli():
    print("\n--- TEST 5: Large Scale Pauli Torture Test ---")
    n = 22  # 2^22 = ~4.1 Million states (~64MB RAM)
    print(f"Logic: Testing X/Y gates on {n} qubits ({1<<n:,} amplitudes)...")
    
    sim = QuantumUniverse(n)
    
    # --- PHASE 1: The X-Gate cascade ---
    # Apply X to every even qubit. This shifts half the memory.
    # State should go from |00...00> to |0101...01>
    print("  [1/3] Applying X to all even qubits...")
    start = time.perf_counter()
    
    for i in range(0, n, 2):
        sim.x(i)
        
    end = time.perf_counter()
    print(f"  -> Finished in {(end-start):.4f}s")
    
    # Validation: Measure. We expect a specific binary pattern.
    # Pattern: ...010101 (Binary)
    # If n=4, we want |0101> = 5.
    expected_pattern = 0
    for i in range(0, n, 2):
        expected_pattern |= (1 << i)
        
    res = sim.measure_all()
    assert res == expected_pattern, f"Large Scale X Failed! Expected {expected_pattern:b}, Got {res:b}"
    print(f"  ✅ X-Gate Pattern Verified: |{res:b}>")
    
    # --- PHASE 2: The Y-Gate Rotation ---
    # Apply Y to qubit 0.
    # Current state has qubit 0 as |1>. Y|1> -> -i|0>.
    # So the whole state should flip qubit 0 to 0, and gain a -i phase.
    print("  [2/3] Applying Y to Qubit 0...")
    
    # We need to re-initialize to the pattern state because measure_all() collapsed it
    # But wait! measure_all() collapses to the state we found. So we are ALREADY in state |...0101>.
    # So we can just proceed.
    
    sim.y(0)
    
    # Now qubit 0 should be 0.
    # New pattern is old_pattern MINUS bit 0.
    new_expected = expected_pattern & ~1
    
    # Audit the amplitude of this specific new state
    amp = sim.get_amplitude(new_expected)
    print(f"  -> Amplitude of |{new_expected:b}>: {amp.real:.1f}{amp.imag:.1f}j")
    
    # Expect -i (0.0 - 1.0j)
    assert abs(amp.imag + 1.0) < 1e-5, "Large Scale Y Math Failed!"
    print("  ✅ Y-Gate Phase Verified (-i).")
    
    print("  ✅ Large Scale Pauli Test Passed.")

if __name__ == "__main__":
    test_pauli_x_y()
    test_large_scale_pauli()