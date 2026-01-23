from qbitUni import QuantumUniverse
import time

def test_grover():
    print("============================")
    print("🔎 GROVER'S SEARCH ALGORITHM")
    print("============================")

    # We will search for the state |111> (Index 7) in a 3-qubit system.
    # Classical search needs ~4-8 checks. Grover needs ~2.    
    n = 3
    u = QuantumUniverse(n)

    print("\n[0] Initial State...") # Print initial state
    u.print_state()
    
    # 1. Initialization: Equal Superposition
    t0 = time.perf_counter()
    print("\n[1] Initialization (Hadamard all)...")
    for i in range(n):
        u.h(i)
    
    u.print_state()
    t1 = time.perf_counter()
    print(f"Time: {t1 - t0:.2f} seconds")
    
    # 2. The Oracle (Marks the state |111>)
    t0 = time.perf_counter()
    print("\n[2] Applying Oracle (Marking |111>)...")
    # For |111>, a specialized Triple-Control-Z is ideal. But using our Toffoli:
    # We can assume the Oracle flips the phase of |111>
    # Construction of a Phase Oracle for |111> using Gates:
    # H(2) -> Toffoli(0,1,2) -> H(2) {-> This turns the Bit-Flip Toffoli into a Phase-Flip.
    u.h(2)
    u.toffoli(0, 1, 2)
    u.h(2)

    u.print_state()
    t1 = time.perf_counter()
    print(f"Time: {t1 - t0:.2f} seconds")
    
    # 3. The Diffuser (Amplifies the marked state)
    
    print("\n[3] Applying Diffuser (Amplification)...")
    # Inversion about the mean.
    # Circuit: H -> X -> Multi-Z -> X -> H    
    t0 = time.perf_counter()
    for i in range(n): u.h(i) # A. Apply H to all
    for i in range(n): u.x(i) # B. Apply X to all
    
    # C. Multi-Controlled Z (H-Toffoli-H trick again)
    t_mid = time.perf_counter()
    u.h(2)
    u.toffoli(0, 1, 2)
    u.h(2)
    t_mid_end = time.perf_counter()
    
    u.print_state()
    
    for i in range(n): u.x(i) # D. Undo X
    for i in range(n): u.h(i) # E. Undo H
    
    t1 = time.perf_counter()
    print(f"Total Diffuser Time: {(t1-t0)*1000:.4f} ms")
    print(f"[Toffoli Core took: {(t_mid_end - t_mid)*1000:.4f} ms]")
    
    print("\n[4] Measurement...") # Print final state
    u.print_state()
    
    # We expect |111> to have high probability (> 70%)
    t0 = time.perf_counter()
    prob = u.get_prob(7)
    t1 = time.perf_counter()
    print(f"Time: {t1 - t0:.2f} seconds")
    print(f"\nProbability of finding |111>: {prob*100:.2f}%")
    
    if prob > 0.7:
        print("✅ SUCCESS: Grover found the needle in the haystack!")
    else:
        print("❌ FAILURE: Search failed.")

if __name__ == "__main__":
    test_grover()
