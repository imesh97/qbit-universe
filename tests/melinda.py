############################
# never forget the 2nd test
#                ~nimsitha
#########################

from qbitUni import QbitUni
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

def test_bell_state():
    print("\n--- TEST 1: Bell State Entanglement ---")
    print("Logic: Qubits 0 and 1 should always be the same (00 or 11)")
    
    # Audit a single state transformation first
    audit_sim = QbitUni(2)
    audit_sim.h(0)
    audit_sim.cnot(0, 1)
    print(f"  Audit Math: {format_state(audit_sim, 2)}")
    
    counts = {"00": 0, "11": 0, "Errors": 0}
    for _ in range(100):
        # We re-run the circuit to simulate 100 'shots'
        s = QbitUni(2)
        s.h(0)
        s.cnot(0, 1)
        res = f"{s.measure():02b}"
        if res in ["00", "11"]:
            counts[res] += 1
        else:
            counts["Errors"] += 1
            
    print(f"  Results after 100 shots: {counts}")
    assert counts["Errors"] == 0, "Entanglement Failed! Qubits were not perfectly correlated."
    print("  ✅ Correlation Proof: P(01)=0, P(10)=0 verified.")

def test_interference():
    print("\n--- TEST 2: Quantum Interference (H-Z-H) ---")
    print("Logic: H -> Z -> H should turn |0> into |1> with 100% certainty")
    sim = QbitUni(1)
    
    sim.h(0)
    print(f"  After H:   {format_state(sim, 1)}")
    
    sim.z(0)
    print(f"  After Z:   {format_state(sim, 1)}  <-- Phase flipped")
    
    sim.h(0)
    print(f"  After H:   {format_state(sim, 1)}  <-- Destructive interference on |0>")
    
    result = sim.measure()
    print(f"  Observed State: |{result}>")
    assert result == 1, "Interference Failed! State should be |1>."
    print("  ✅ Interference Proof: Probability of |0> is now 0.")

def test_phase_rotation():
    print("\n--- TEST 3: S-Gate (90-degree) Rotation ---")
    print("Logic: H -> S should create a state with a 0.707i imaginary amplitude")
    sim = QbitUni(1)
    sim.h(0)
    
    print(f"  Before S: {format_state(sim, 1)}")
    sim.s(0)
    print(f"  After S:  {format_state(sim, 1)}")
    
    amp = sim.get_amplitude(1)
    print(f"  Audit: Amplitude of |1> is {amp.real:+.3f}{amp.imag:+.3f}j")
    
    # Check if the imaginary part is roughly 0.707
    assert abs(amp.imag - 0.707) < 0.01, "Phase Rotation Failed!"
    print("  ✅ Phase Proof: S-gate successfully rotated the vector into the imaginary axis.")

# ... (keep format_state and previous tests) ...

def test_large_scaling():
    print("\n--- TEST 4: Memory Scaling & Performance Audit ---")
    n = 20
    num_amplitudes = 1 << n
    print(f"Logic: Testing {n} qubits ({num_amplitudes:,} amplitudes)...")
    
    try:
        # Benchmark Allocation
        start_alloc = time.perf_counter()
        sim = QbitUni(n)
        end_alloc = time.perf_counter()
        print(f"  [TIME] Allocation: {(end_alloc - start_alloc)*1000:.2f}ms")

        # Benchmark Parallel Hadamard (O(N) operation)
        start_h = time.perf_counter()
        sim.h(0)
        end_h = time.perf_counter()
        
        h_time = end_h - start_h
        velocity = (num_amplitudes / h_time) / 1e6 # Millions of ops/sec
        
        print(f"  [TIME] Hadamard:   {h_time*1000:.2f}ms")
        print(f"  [AUDIT] Velocity:   {velocity:.2f} Million Amplitudes/sec")

        # Benchmark CNOT (O(N) with conditional logic)
        start_cnot = time.perf_counter()
        sim.cnot(0, 1)
        end_cnot = time.perf_counter()
        print(f"  [TIME] CNOT:       {(end_cnot - start_cnot)*1000:.2f}ms")
        
        print(f"  ✅ Performance Audit: Successfully processed {n} qubits.")
        
    except Exception as e:
        print(f"  ❌ Scaling Failed: {e}")
        raise e

if __name__ == "__main__":
    print("🧪 STARTING SECOND AUDIT SUITE")
    print("="*40)
    test_bell_state()
    test_interference()
    test_phase_rotation()
    test_large_scaling()
    print("\n✨ All mathematical proofs in Test 2 passed!")
