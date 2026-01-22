# old logic


from sim import QuantumUniverse

import random
import numpy as np

def main():
    n = int(input("Enter number of qubits for the universe: "))
    univ = QuantumUniverse(n)
    
    print(f"\nUniverse of {n} qubits initialized.")
    print("Commands: 'h <qubit>', 'cnot <ctrl> <targ>', 'print', 'exit'")

    while True:
        cmd = input("\n> ").lower().split()
        if not cmd:
            continue
        
        if cmd[0] == 'h':
            univ.apply_hadamard(int(cmd[1]))
            print(f"Applied H to qubit {cmd[1]}")
            
        elif cmd[0] == 'z':
            target = int(cmd[1])
            if target >= n:
                print(f"Error: Qubit {target} doesn't exist in this {n}-qubit universe.")
                continue
            univ.apply_z(target)
            print(f"Applied Z to qubit {target}")

        elif cmd[0] == 'cnot':
            ctrl, targ = int(cmd[1]), int(cmd[2])
            if ctrl >= n or targ >= n:
                print("Error: Qubits out of range.")
                continue
            univ.apply_cnot(ctrl, targ)
            print(f"Applied CNOT ({ctrl}->{targ})")
            
        elif cmd[0] == 'print':
            is_valid, total = univ.verify_integrity()
            
            if not is_valid:
                print(f"⚠️ WARNING: Universe Integrity Compromised! Total Prob: {total:.4f}")
            
            print(f"--- Universe Status (Integrity: {'OK' if is_valid else 'FAIL'}) ---")
            
            for i, amp in enumerate(univ.state):
                if abs(amp)**2 > 0.0001:
                    binary = format(i, f'0{n}b')
                    # Show the real and imaginary parts
                    print(f"|{binary}>: {amp.real:+.2f} {amp.imag:+.2f}j")
        
        elif cmd[0] == 'measure':
            probs = univ.get_probabilities()
            outcome = random.choices(range(univ.dim), weights=probs)[0]
            binary = format(outcome, f'0{n}b')
            print(f"COLLAPSE: The universe has chosen state |{binary}>")
            
            # Reset the universe to that single state (Actual Physics!)
            univ.state = np.zeros(univ.dim, dtype=np.complex128)
            univ.state[outcome] = 1.0 + 0j

        elif cmd[0] == 'exit':
            break

if __name__ == "__main__":
    main()