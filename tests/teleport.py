# T^4 = Z

from qbitUni import QuantumUniverse

def test_t_versus_z():
    print("🔮 UNIVERSALITY CHECK: T^4 vs Z Gate")
    print("====================================")
    
    u_t = QuantumUniverse(1)
    u_t.print_state() # Print initial state
    
    # --- EXPERIMENT A: The T-Gate Chain ---
    print("\n🧪 Experiment A: Applying T four times")

    u_t.h(0) # Start in Superposition |+>
    u_t.t(0) # Apply T four times (45° * 4 = 180°)
    u_t.t(0)
    u_t.t(0)
    u_t.t(0)
    
    u_t.print_state() # Print state after T^4 test
    
    # --- EXPERIMENT B: The Z-Gate Baseline ---
    print("\n🧪 Experiment B: Applying Z once (Control Group)")
    u_z = QuantumUniverse(1)
    
    u_z.h(0) # Start in Superposition |+>    
    u_z.z(0) # Apply Z once (180°)
    
    u_z.print_state() # Print state after Z test
    
    # --- MATHEMATICAL VERIFICATION ---
    print("\n📊 Verification Analysis")
    
    # Get amplitudes of the |1> state for both
    amp_t = u_t.get_amplitude(1)
    amp_z = u_z.get_amplitude(1)
    
    print(f"   T^4 Result (|1>): {amp_t.real:.4f} {amp_t.imag:+.4f}j")
    print(f"   Z   Result (|1>): {amp_z.real:.4f} {amp_z.imag:+.4f}j")
    
    # Calculate difference
    diff_real = abs(amp_t.real - amp_z.real)
    diff_imag = abs(amp_t.imag - amp_z.imag)
    
    if diff_real < 1e-6 and diff_imag < 1e-6:
        print("\n✅ SUCCESS: T^4 is mathematically identical to Z.")
        print("   [Theory] T rotates phase by 45° (π/4).")
        print("   [Theory] Z rotates phase by 180° (π).")
        print("   [Result] Your engine is now Universal.")
    else:
        print(f"\n❌ FAILURE: Mismatch detected. Diff: {diff_real}")

if __name__ == "__main__":
    test_t_versus_z()