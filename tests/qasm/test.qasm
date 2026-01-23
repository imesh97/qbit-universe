OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];

// 1. Create Bell State
h q[0];
cx q[0], q[1];

// 2. Rotate Qubit 2
rx(1.5708) q[2]; 

// 3. Measure
measure q[0] -> c[0];