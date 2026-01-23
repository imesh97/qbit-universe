import re
from . import QuantumUniverse

class QASMParser:
    def __init__(self):
        self.u = None
        self.qreg_map = {} 
        self.creg_map = {} 

    def load(self, qasm_string):
        print("📦 Parsing OpenQASM Circuit...")
        
        lines = [line.strip() for line in qasm_string.split('\n')]
        
        for line in lines: # 1. Cleanup
            if '//' in line:
                line = line.split('//')[0].strip()
            if not line:
                continue
            if line.startswith("OPENQASM") or line.startswith("include"):
                continue
            
            line = line.replace(';', '')
            
            # --- CRITICAL FIX ---
            # Split only once to separate "Command" from "All Arguments"
            # "cx q[0], q[1]" -> ['cx', 'q[0], q[1]']
            parts = line.split(None, 1)
            
            if len(parts) < 2:
                continue # Skip if no arguments
            
            cmd = parts[0]
            args_str = parts[1] # Now contains "q[0], q[1]"

            # 2. Register Allocation
            if cmd == 'qreg':
                match = re.match(r'([a-z]+)\[(\d+)\]', args_str)
                if match:
                    name, size = match.groups()
                    size = int(size)
                    self.qreg_map[name] = size
                    if self.u is None:
                        self.u = QuantumUniverse(size)
                        print(f"   -> Allocated Universe with {size} qubits")
            
            # 3. Measurement
            elif cmd == 'measure':
                # Parse "q[0] -> c[0]"
                # Use original line for '->' splitting safety
                if '->' in line:
                    arrow_split = line.split('->')
                    q_part = arrow_split[0].strip().split()[-1] # Gets "q[0]"
                    
                    idx = int(re.search(r'\[(\d+)\]', q_part).group(1))
                    if self.u:
                        val = self.u.measure_qubit(idx)
                        print(f"   -> Measured q[{idx}] = {val}")

            # 4. Standard Gates
            elif self.u:
                # Now passing the full argument string "q[0], q[1]"
                self._apply_gate(cmd, args_str)

        return self.u

    def _apply_gate(self, cmd, args_str):
        gate_map = {
            'h': 'h', 'x': 'x', 'y': 'y', 'z': 'z', 
            's': 's', 't': 't', 'cx': 'cnot', 'cz': 'cz',
            'swap': 'swap', 'rx': 'rx', 'phase': 'phase'
        }
        
        # Regex will now find ALL indices in the string
        indices = [int(x) for x in re.findall(r'\[(\d+)\]', args_str)]
        
        if cmd in gate_map:
            method_name = gate_map[cmd]
            # Now indices has [0, 1], so *indices expands to (0, 1) -> Success!
            getattr(self.u, method_name)(*indices)
            
        elif '(' in cmd:
            op_name = cmd.split('(')[0]
            param = float(re.search(r'\(([\d\.-]+)\)', cmd).group(1))
            
            if op_name == 'rx':
                self.u.rx(indices[0], param)
            elif op_name == 'rz': 
                self.u.phase(indices[0], param)

def run_file(filename):
    with open(filename, 'r') as f:
        parser = QASMParser()
        u = parser.load(f.read())
        if u:
            print("\n--- Final State ---")
            u.print_state()