from qbitUni import QuantumUniverse
# ~~Bill Nye, the Science Guy!.

def test_expectation_value():
    print("\n================================")
    print("🧪 TESTING EXPECTATION VALUES <Z>")
    print("================================")
    
    u = QuantumUniverse(1)
    
    # Case 1: State |0>
    # Expectation should be +1.0
    exp = u.get_expectation(0)
    print(f"State |0> : <Z> = {exp:.2f} (Expected: 1.00)")
    
    # Case 2: State |1> (Apply X)
    # Expectation should be -1.0
    u.x(0)
    exp = u.get_expectation(0)
    print(f"State |1> : <Z> = {exp:.2f} (Expected: -1.00)")
    
    # Case 3: State |+> (Apply H)
    # Expectation should be 0.0 (Perfectly balanced)
    u.h(0)
    exp = u.get_expectation(0)
    print(f"State |+> : <Z> = {exp:.2f} (Expected: 0.00)")

def test_noise_decay():
    print("\n========================================")
    print("📉 TESTING QUANTUM NOISE (Decoherence)")
    print("========================================")
    
    # We will simulate a qubit decaying over time.
    # We apply small noise repeatedly and watch the expectation value drop.
    u = QuantumUniverse(1)
    u.get_expectation(0) # Should be 1.0
    
    print("Applying 50% noise repeatedly...")
    print("Step | <Z> Value | Status")
    print("-----|-----------|--------")
    
    for i in range(1, 101):
        u.apply_noise(0, 0.50) # Apply 50% depolarizing noise
        
        val = u.get_expectation(0) # Measure expectation
        
        # Visual bar
        bar_len = int((val + 1) * 10) # Map -1..1 to 0..20
        bar = "#" * bar_len
        
        print(f"{i:3d}  | {val:+.4f}   | {bar}")
        
    print("\n✅ Verification: The value should drift randomly or decay away from 1.0.")

if __name__ == "__main__":
    test_expectation_value()
    test_noise_decay()