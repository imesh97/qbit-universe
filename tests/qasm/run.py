from qbitUni.qasm import run_file
import os

if __name__ == "__main__":
    filename = "tests/qasm/test.qasm" # Ensure we look in the 'tests' folder or current folder
    
    if not os.path.exists(filename): # Fallback if running from inside tests folder
        filename = "qasm/test.qasm"
        
    print(f"📂 Running: {filename}")
    run_file(filename)