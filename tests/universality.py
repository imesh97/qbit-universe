# T^4 = Z

from qbitUni import QuantumUniverse
from qbitUni.visuals import print_bloch_vector
import math

def test_t_versus_z():
    print("====================================")
    print("🔮 UNIVERSALITY CHECK: T^4 vs Z Gate")
    print("====================================")
    
    u_t = QuantumUniverse(1)
    u_t.print_state() # Print initial state
    
    # --- EXPERIMENT A: The T-Gate Chain ---
    print("\n🧪 Experiment A: Applying T four times")

    u_t.h(0) # Start in Superposition |+>
    print("   [Visual] Start (|0> + |1>):") 
    print_bloch_vector(u_t.get_amplitude(0), u_t.get_amplitude(1))

    print("   Applying T -> T -> T -> T")
    u_t.t(0) # Apply T four times (45° * 4 = 180°)
    u_t.t(0)
    u_t.t(0)
    u_t.t(0)
    
    u_t.print_state() # Print state after T^4 test
    print("   [Visual] End (Should be |0> - |1>):")
    print_bloch_vector(u_t.get_amplitude(0), u_t.get_amplitude(1))
    
    # --- EXPERIMENT B: The Z-Gate Baseline ---
    print("\n🧪 Experiment B: Applying Z once (Control Group)")
    u_z = QuantumUniverse(1)
    
    u_z.h(0) # Start in Superposition |+>    
    u_z.z(0) # Apply Z once (180°)
    
    u_z.print_state() # Print state after Z test
    print("   [Visual] End (Z Gate):")
    print_bloch_vector(u_z.get_amplitude(0), u_z.get_amplitude(1))
    
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

def test_phase_universality():
    print("================================")
    print("🎨 Testing Parametric Phase Gate")
    print("================================")
    
    # --- CASE 1: Phase(PI) vs Z ---
    print("\n[1] Checking if Phase(PI) == Z...")
    
    # Experiment A: Using Phase(PI)
    print("  -> Applying Phase(PI)...")
    u1 = QuantumUniverse(1)
    u1.print_state() # Print initial
    print("   [Visual] End (Z Gate):")
    print_bloch_vector(u1.get_amplitude(0), u1.get_amplitude(1))

    u1.h(0)
    u1.phase(0, math.pi)
    u1.print_state()  # Print state
    print("   [Visual] End (Z Gate):")
    print_bloch_vector(u1.get_amplitude(0), u1.get_amplitude(1))
    
    # Experiment B: Using Standard Z
    print("  -> Applying Standard Z...")
    u2 = QuantumUniverse(1)
    u2.print_state() # Print initial
    print("   [Visual] End (Z Gate):")
    print_bloch_vector(u2.get_amplitude(0), u2.get_amplitude(1))

    u2.h(0)
    u2.z(0)
    u2.print_state()  # Print state
    print("   [Visual] End (Z Gate):")
    print_bloch_vector(u2.get_amplitude(0), u2.get_amplitude(1))
    
    # Verification
    amp1 = u1.get_amplitude(1)
    amp2 = u2.get_amplitude(1)
    
    print(f"    Phase(PI) |1>: {amp1.real:.3f} {amp1.imag:+.3f}j")
    print(f"    Z Gate    |1>: {amp2.real:.3f} {amp2.imag:+.3f}j")
    
    # Check Real parts (since PI rotation flips real sign)
    if abs(amp1.real - amp2.real) < 0.001:
        print("    ✅ Match.")
    else:
        print("    ❌ Mismatch.")

    # --- CASE 2: Phase(PI/2) vs S ---
    print("\n[2] Checking if Phase(PI/2) == S...")
    
    # Experiment A: Using Phase(PI/2)
    print("  -> Applying Phase(PI/2)...")
    u3 = QuantumUniverse(1)
    u3.print_state() # Print initial
    print("   [Visual] End (Z Gate):")
    print_bloch_vector(u3.get_amplitude(0), u3.get_amplitude(1))

    u3.h(0)
    u3.phase(0, math.pi/2)
    u3.print_state()
    print("   [Visual] End (Z Gate):")
    print_bloch_vector(u3.get_amplitude(0), u3.get_amplitude(1))
    
    # Experiment B: Using Standard S
    print("  -> Applying Standard S...")
    u4 = QuantumUniverse(1)
    u4.print_state() # Print initial
    print("   [Visual] End (Z Gate):")
    print_bloch_vector(u4.get_amplitude(0), u4.get_amplitude(1))

    u4.h(0)
    u4.s(0)
    u4.print_state()
    print("   [Visual] End (Z Gate):")
    print_bloch_vector(u4.get_amplitude(0), u4.get_amplitude(1))
    
    # Verification
    amp3 = u3.get_amplitude(1)
    amp4 = u4.get_amplitude(1)
    
    print(f"    Phase(PI/2) |1>: {amp3.real:.3f} {amp3.imag:+.3f}j")
    print(f"    S Gate      |1>: {amp4.real:.3f} {amp4.imag:+.3f}j")
    
    # Check Imaginary parts (since S rotation moves Real to Imag)
    if abs(amp3.imag - amp4.imag) < 0.001:
        print("    ✅ Match.")
    else:
        print("    ❌ Mismatch.")

if __name__ == "__main__":
    test_t_versus_z()
    print()
    test_phase_universality()