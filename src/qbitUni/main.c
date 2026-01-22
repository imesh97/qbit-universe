#include <stdio.h>

#include "universe.h"
#include "gates.h"

// the real test, after all

int main() {
    Universe *u = init_universe(1);
    
    // Apply H to qubit 0 ONLY ONCE
    apply_hadamard(u, 0); 
    apply_s(u, 0);

    double total_prob = 0;
    for(long long i = 0; i < u->dim; i++) {
        // Prob = real^2 + imag^2
        double p = creal(u->psi[i])*creal(u->psi[i]) + cimag(u->psi[i])*cimag(u->psi[i]);
        total_prob += p;
        printf("State %lld: %f + %fi (Prob: %f)\n", i, creal(u->psi[i]), cimag(u->psi[i]), p);
    }
    printf("Total Universe Probability: %f\n", total_prob);

    destroy_universe(u);
    return 0;
}