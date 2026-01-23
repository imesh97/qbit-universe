from qbitUni import QuantumUniverse
import math

def test_teleportation():
    print("=================================")
    print("🚀 QUANTUM TELEPORTATION PROTOCOL")
    print("=================================")
    print("Goal: Move state of Qubit 0 (Alice) -> Qubit 2 (Bob)")
    
    # We need 3 Qubits:
    # Q0: The "Payload" (The secret state we want to send)
    # Q1: Alice's half of the entangled pair
    # Q2: Bob's half of the entangled pair
    u = QuantumUniverse(3)
    u.print_state()
    
    # --- STEP 1: PREPARE THE PAYLOAD (Q0) ---
    # We create a specific secret state on Q0 using H then T.
    # State becomes: 0.707|0> + (0.5+0.5i)|1>
    print("\n1. Preparing Payload on Qubit 0 [H and T]...")
    u.h(0)
    u.t(0)
    u.print_state()
    
    # Record the target amplitude for manual verification later
    amp0 = u.get_amplitude(0b001) # State |001> (Q0=1, others=0)
    print(f"    Target Amplitude to Match: {amp0.real:.3f} {amp0.imag:+.3f}j")

    # --- STEP 2: CREATE ENTANGLEMENT (THE "BRIDGE") ---
    # Alice (Q1) and Bob (Q2) share a Bell Pair.
    print("\n2. Entangling Alice (Q1) and Bob (Q2) [H and CNOT]...")
    u.h(1)
    u.cnot(1, 2)
    u.print_state()
    
    # --- STEP 3: ALICE'S BELL MEASUREMENT ---
    # Alice performs a Bell Basis measurement on her two qubits (Q0 & Q1).
    # This entangles the payload with the bridge.
    print("\n3. Alice performs Bell Measurement on Q0 & Q1 [CNOT and H]...")
    u.cnot(0, 1)
    u.h(0)
    u.print_state()
    
    # Alice measures her qubits. This collapses Q0 and Q1 to classical bits,
    # but the quantum information is projected onto Bob's qubit (Q2).
    bit0 = u.measure_qubit(0)
    bit1 = u.measure_qubit(1)
    
    print(f"    Alice Measured: {bit1}{bit0} (Binary)")
    
    # --- STEP 4: BOB'S CORRECTION (CLASSICAL FEEDBACK) ---
    # Bob applies specific gates to Q2 based on the bits Alice sent him.
    print("\n4. Bob applies corrections based on Alice's bits...")
    
    if bit1 == 1:
        print("    -> Applying X (Bit Flip)")
        u.x(2)
        
    if bit0 == 1:
        print("    -> Applying Z (Phase Flip)")
        u.z(2)
        
    # --- STEP 5: VERIFICATION ---
    # Qubit 2 should now hold the exact state Qubit 0 started with.
    # Note: Q0 and Q1 are now collapsed (0 or 1), but Q2 is in the secret superposition.
    print("\n5. Verifying Bob's Qubit (Q2)...")
    u.print_state()

    print("\n6. SCIENTIFIC PROOF [Uncomputing]")
    # To prove Q2 holds the secret, we apply the INVERSE of the preparation steps.
    # Preparation was: H -> T
    # Inverse is: Inverse-T -> Inverse-H
    
    u.phase(2, -math.pi/4) # Reverse T (Using Phase Gate with -PI/4)
    u.h(2) # Reverse H (H is its own inverse)
    
    # If Q2 held the correct state, uncomputing it must result in exactly |0>.
    # If we measure 1, the teleportation failed.
    result = u.measure_qubit(2)
    
    if result == 0:
        print("SUCCESS! Bob's qubit uncomputed perfectly to |0>.")
    else:
        print("FAILURE! Bob's qubit was |1>. Information lost.")
    
    print("\n✅ TELEPORTATION COMPLETE.")

    # --- MANUAL VERIFICATION NOTES (For the math curious) ---
    # We check the amplitude of the state where Q2=1 (from Step 5).
    # Depending on the random collapse of Q0/Q1, the index will change.
    # If Alice measured 00, we check index 0b100 (4)
    # If Alice measured 01, we check index 0b101 (5)
    # But wait! print_state() shows us everything.
    # We just need to verify that the RELATIVE phase/magnitude of Bob's |0> vs |1> is correct.
    
    # Let's do a mathematical check:
    # We apply the INVERSE of the preparation to Q2.
    # Inverse of (H then T) is (Inverse-T then H).
    # Since T^4 = Z, Inverse-T is T^7 (or just Tdg).
    # Let's just manually check the math of the final state printed above.
    print("Compare the 'Target Amplitude' from Step 1 with Q2's amplitude in the final print dump.")

if __name__ == "__main__":
    test_teleportation()