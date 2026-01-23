#include <stdlib.h>

#include "universe.h"
#include "gates.h"

void apply_noise(Universe *u, int target, double prob) {
    double r = (double)rand() / RAND_MAX; // Roll the dice (0.0 to 1.0)
    if (r < prob) { // If we are unlucky, apply an error
        // Pick an error type randomly: X, Y, or Z.
        // We can just roll another integer 0, 1, or 2.
        int error_type = rand() % 3;
        if (error_type == 0) {
            apply_x(u, target); // Bit Flip Error
        } else if (error_type == 1) {
            apply_y(u, target); // Phase+Bit Flip Error
        } else {
            apply_z(u, target); // Phase Flip Error
        }
    }
    // Else: The qubit survives unchanged.
}

double get_expectation(Universe *u, int target) {
    long long bit = 1LL << target;
    double prob_1 = 0.0;

    // 1. Calculate the total probability of the qubit being |1>
    // (Loop over the whole statevector)
    for (long long i = 0; i < u->dim; i++) {
        if (i & bit) { // Add |amplitude|^2
            prob_1 += cabs(u->psi[i]) * cabs(u->psi[i]);
        }
    }
    
    // 2. Calculate Expectation Value <Z>
    // Formula: P(0) - P(1)
    // Since P(0) = 1.0 - P(1),
    // Result = (1.0 - P(1)) - P(1)  =>  1.0 - 2*P(1)
    return 1.0 - (2.0 * prob_1);
}