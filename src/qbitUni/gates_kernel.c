#include <math.h>
#include <complex.h>
#include "universe.h"

/* --- KERNEL FUNCTIONS --- */
/* Pure math. Run in parallel later. */

void kernel_hadamard(Universe *u, int target, int control, long long start, long long end) {
    double factor = 1.0 / sqrt(2.0); // Calculate the 'Normalization' factor (1/sqrt(2))
    long long bit = 1LL << target; // Identify the bit we are targeting (e.g., qubit 0 = 001)

    for (long long i = start; i < end; i++) {    // Loop through every state in the universe
        if (!(i & bit)) { // Only act on the 'partner' state (where the target bit is 0)
            long long j = i | bit; // Find the 'partner' state (where the target bit is 1)
            
            double complex v0 = u->psi[i]; // Get the amplitudes
            double complex v1 = u->psi[j];

            // The Hadamard Math (FOIL happens inside these additions!)
            u->psi[i] = (v0 + v1) * factor;
            u->psi[j] = (v0 - v1) * factor;
        }
    }
}

void kernel_x(Universe *u, int target, int control, long long start, long long end) {
    long long bit = 1LL << target; 
    
    for (long long i = start; i < end; i++) {
        // We iterate through all states.
        // To avoid double-swapping, we only act when the target bit is 0.
        if (!(i & bit)) {
            long long j = i | bit;
            double complex temp = u->psi[i];
            u->psi[i] = u->psi[j];
            u->psi[j] = temp;
        }
    }
}

void kernel_y(Universe *u, int target, int control, long long start, long long end) {
    long long bit = 1LL << target;
    for (long long i = start; i < end; i++) {
        if (!(i & bit)) {
            long long j = i | bit;

            double complex v0 = u->psi[i];
            double complex v1 = u->psi[j];

            // 1. Swap
            // 2. Multiply v1 by -i (which is -I in C)
            // 3. Multiply v0 by i  (which is I in C)
            u->psi[i] = -I * v1;
            u->psi[j] =  I * v0;
        }
    }
}

void kernel_z(Universe *u, int target, int control, long long start, long long end) {
    long long bit = 1LL << target;
    for (long long i = start; i < end; i++) {
        if (i & bit) {
            u->psi[i] = -u->psi[i]; // If the target bit is 1, flip the sign
        }
    }
}

void kernel_s(Universe *u, int target, int control, long long start, long long end) {
    long long bit = 1LL << target;

    for (long long i = start; i < end; i++) {
        // Rule: Only act if the target bit is 1
        if (i & bit) {
            // Multiply the amplitude by the imaginary unit 'I'
            u->psi[i] *= I;
        }
    }
}

void kernel_cnot(Universe *u, int target, int control, long long start, long long end) {
    long long ctrl_bit = 1LL << control;
    long long targ_bit = 1LL << target;

    for (long long i = start; i < end; i++) {
        // Rule: Only act if the control bit is 1 
        // AND to avoid swapping twice, we only act when target bit is 0
        if ((i & ctrl_bit) && !(i & targ_bit)) {
            long long j = i | targ_bit; // The state where target bit is 1

            double complex temp = u->psi[i];

            u->psi[i] = u->psi[j]; // Swap the 'stories' (amplitudes)
            u->psi[j] = temp;
        }
    }
}
