#include <stdio.h>
#include <assert.h>
#include <math.h>
#include <complex.h>

#include "../universe.h"
#include "../gates.h"

// Helper to check if the total probability is 1.0
void verify_integrity(Universe *u, const char* test_name) {
    double total_prob = 0;
    for (long long i = 0; i < u->dim; i++) {
        total_prob += creal(u->psi[i]) * creal(u->psi[i]) + 
                      cimag(u->psi[i]) * cimag(u->psi[i]);
    }
    // Check if total probability is close to 1.0
    if (fabs(total_prob - 1.0) > 1e-6) {
        printf("❌ FAILED: %s (Prob: %f)\n", test_name, total_prob);
        assert(0);
    }
    printf("✅ PASSED: %s\n", test_name);
}

void run_hadamard() {
    // Test 1: Hadamard Reversibility (H * H = Identity)
    Universe *u1 = init_universe(1);
    apply_hadamard(u1, 0);
    apply_hadamard(u1, 0);
    assert(creal(u1->psi[0]) > 0.99); // Should be back at |0>
    verify_integrity(u1, "Hadamard Reversibility");
    destroy_universe(u1);
}

void run_s_gate() {
    // Test 2: S-Gate Phase Rotation
    Universe *u2 = init_universe(1);
    apply_hadamard(u2, 0);
    apply_s(u2, 0);
    // |1> state should now be purely imaginary (0.707i)
    assert(fabs(cimag(u2->psi[1]) - 0.707107) < 1e-5);
    verify_integrity(u2, "S-Gate Phase Shift");
    destroy_universe(u2);
}

void run_z_gate() {
    // Test 3: Z-Gate Interference
    Universe *u3 = init_universe(1);
    apply_hadamard(u3, 0);
    apply_z(u3, 0);
    apply_hadamard(u3, 0);
    // H -> Z -> H turns |0> into |1>
    assert(creal(u3->psi[1]) > 0.99); 
    verify_integrity(u3, "Z-Gate Interference");
    destroy_universe(u3);
}

void run_cnot() {
    // Test 4: CNOT Entanglement (Bell State)
    Universe *u4 = init_universe(2);
    apply_hadamard(u4, 0);
    apply_cnot(u4, 0, 1);
    // In a Bell state, only |00> and |11> should exist
    assert(fabs(creal(u4->psi[1])) < 1e-6); // |01> must be 0
    assert(fabs(creal(u4->psi[2])) < 1e-6); // |10> must be 0
    verify_integrity(u4, "CNOT Entanglement");
    destroy_universe(u4);
}

int main() {
    printf("--- Starting Quantum Gate Tests ---\n");

    run_hadamard();
    run_s_gate();
    run_z_gate();
    run_cnot();

    printf("\nAll systems nominal. Your C engine is physics-accurate.\n");
    return 0;
}