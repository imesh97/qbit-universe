#include <stdlib.h>
#include <time.h>

#include "universe.h"

/*

first we create the universe (init).
then we apply gates (apply_hadamard, apply_cnot, etc.).
then we measure (get_probability).
finally we destroy the universe (destroy_universe).

*/

Universe* init_universe(int n) {
    Universe *u = malloc(sizeof(Universe));
    u->n_qubits = n;
    u->dim = 1LL << n; // 2^n

    // Allocate the memory block (e.g., 28 qubits = 4GB)
    u->psi = (double complex*)calloc(u->dim, sizeof(double complex));

    if (u->psi == NULL) return NULL; // Fail if RAM is full

    // Start the universe at |00...0>
    u->psi[0] = 1.0 + 0.0 * I;
    return u;
}

void destroy_universe(Universe *u) {
    if (u) {
        if (u->psi) free(u->psi);
        free(u);
    }
}

double get_probability(Universe *u, long long index) {
    if (index < 0 || index >= u->dim) return 0.0;
    
    double r = creal(u->psi[index]);
    double i = cimag(u->psi[index]);
    
    return (r * r) + (i * i);
}

long long measure_all(Universe *u) {
    srand(time(NULL)); // Seeds the random number generator with the current time
    // 1. Generate a random number between 0 and 1
    double r = (double)rand() / (double)RAND_MAX;
    double cumulative_prob = 0;

    for (long long i = 0; i < u->dim; i++) {
        double p = creal(u->psi[i])*creal(u->psi[i]) + cimag(u->psi[i])*cimag(u->psi[i]);
        cumulative_prob += p;

        // 2. If the random number falls within this state's probability range
        if (r <= cumulative_prob) {
            // 3. COLLAPSE: Set this state to 1.0 and all others to 0.0
            for (long long j = 0; j < u->dim; j++) {
                u->psi[j] = 0.0 + 0.0 * I;
            }
            u->psi[i] = 1.0 + 0.0 * I;
            return i; // Return the index we "observed"
        }
    }
    return 0;
}
