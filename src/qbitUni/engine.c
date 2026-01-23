#include <stdlib.h>
#include <time.h>
#include <math.h>

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
    double r = (double)rand() / (double)RAND_MAX; // Generate a random number between 0 and 1
    double cumulative_prob = 0;

    for (long long i = 0; i < u->dim; i++) {
        double p = creal(u->psi[i])*creal(u->psi[i]) + cimag(u->psi[i])*cimag(u->psi[i]);
        cumulative_prob += p;

        // If the random number falls within this state's probability range
        if (r <= cumulative_prob) {
            // COLLAPSE: Set this state to 1.0 and all others to 0.0
            for (long long j = 0; j < u->dim; j++) {
                u->psi[j] = 0.0 + 0.0 * I;
            }
            u->psi[i] = 1.0 + 0.0 * I;
            return i; // Return the index we "observed"
        }
    }
    return 0;
}

int measure_qubit(Universe *u, int target) {
    long long bit = 1LL << target;
    double prob_1 = 0.0;

    // Calculate Probability of being |1>
    // (This loop can be parallelized with a reduction!)
    for (long long i = 0; i < u->dim; i++) {
        if (i & bit) {
            prob_1 += cabs(u->psi[i]) * cabs(u->psi[i]);
        }
    }

    // Roll the die
    // (Using simple rand() for clarity, use safer RNG in production)
    double r = (double)rand() / RAND_MAX;
    int result = (r < prob_1); // 1 if we rolled below prob_1, else 0

    // Collapse and Renormalize
    double norm_factor = 1.0 / sqrt(result ? prob_1 : (1.0 - prob_1));

    for (long long i = 0; i < u->dim; i++) {
        int is_on = (i & bit) != 0;
        
        if (is_on == result) { // This state survives. Boost it to keep total prob = 1.0
            u->psi[i] *= norm_factor;
        } else { // This state dies.
            u->psi[i] = 0;
        }
    }

    return result;
}