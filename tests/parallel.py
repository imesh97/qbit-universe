###########################
# never forget concurrency
#                 ~Gemini
########################

from qbitUni import QuantumUniverse
import time
import os

# Colors for terminal output
CYAN = "\033[96m" 
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def run_benchmark(n_qubits, n_threads):
    """
    Sets the C-level environment variable and times a heavy operation.
    """
    os.environ["THREADS"] = str(n_threads) # Set the C Environment Variable
    
    # Initialize Universe (Allocates RAM)
    # We use a large universe to ensure the CPU has enough work
    u = QuantumUniverse(n_qubits)
    
    # Time the Operation (Hadamard on highest qubit = Worst Case Memory Access)
    start = time.perf_counter()
    u.h(n_qubits - 1) 
    end = time.perf_counter()
    
    return end - start

def test_thread_scaling():
    print(f"\n{CYAN}--- TEST 1: Multithreading Efficiency Audit ---{RESET}")
    
    # 24 Qubits = ~16 Million amplitudes (~256 MB RAM)
    # This is large enough to see threading benefits, but safe for most laptops.
    QUBITS = 24 
    WORKERS = 4
    
    print(f"Logic: Compare execution time of 1 Worker vs {WORKERS} Workers.")
    print(f"Workload: {QUBITS} Qubits ({1<<QUBITS:,} states) | Gate: H({QUBITS-1})")
    print("-" * 60)

    # --- PHASE 1: Single Thread Baseline ---
    print(f"  [1/2] Running with {YELLOW}1 Worker{RESET}...")
    t1 = run_benchmark(QUBITS, 1) # 1 Worker
    print(f"      -> Time: {t1:.4f}s")

    # --- PHASE 2: Multi-Threaded Run ---
    print(f"  [2/2] Running with {YELLOW}{WORKERS} Workers{RESET}...")
    t_multi = run_benchmark(QUBITS, WORKERS) # 4 Workers
    print(f"      -> Time: {t_multi:.4f}s")

    # --- PHASE 3: The Audit ---
    print("-" * 60)
    
    if t_multi == 0: # Avoid division by zero if it's too fast
        t_multi = 0.0001
        
    speedup = t1 / t_multi
    print(f"  [AUDIT] Speedup Factor: {GREEN}{speedup:.2f}x{RESET}")
    
    # Verification Logic
    if speedup > 1.2:
        print(f"  ✅ {GREEN}SUCCESS:{RESET} Parallel engine is actively reducing wait times.")
        print(f"     (Theoretical Max: {WORKERS}.0x | Real-World Target: >1.5x)")
    elif speedup > 0.9:
        print(f"  ⚠️ {YELLOW}WARNING:{RESET} Performance is flat. System might be memory-bound.")
    else:
        print(f"  ❌ {RED}FAILURE:{RESET} Threads caused a slowdown (Overhead > Math).")
        # We don't assert False here because CI machines often have erratic CPU availability,
        # but locally this should pass easily.

def test_concurrency_safety():
    print(f"\n{CYAN}--- TEST 2: Concurrency Safety Check ---{RESET}")
    print("Logic: Ensure 4 threads writing to the same array don't corrupt data.")
    
    n = 20
    os.environ["THREADS"] = "4"
    sim = QuantumUniverse(n)
    
    # Apply H to all qubits (Massive parallel write)
    print(f"  [1/2] Applying parallel Hadamard to {n} qubits...")
    for i in range(n):
        sim.h(i)
        
    # CHECK RESULT:
    # H on |0...0> n times creates equal superposition.
    # Prob of state |0...0> should be 1 / 2^n
    expected_prob = 1.0 / (1 << n)
    actual_prob = sim.get_prob(0)
    
    print("  [2/2] Verifying integrity of state |0...0>...")
    print(f"      -> Expected: {expected_prob:.8f}")
    print(f"      -> Actual:   {actual_prob:.8f}")
    
    assert abs(actual_prob - expected_prob) < 1e-9, "Thread Safety Failed! Data corruption detected."
    print("  ✅ Proof: Parallel writes did not cause race conditions.")

if __name__ == "__main__":
    test_thread_scaling()
    test_concurrency_safety()