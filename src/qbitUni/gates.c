#include <math.h>

#include "universe.h"
#include "gates.h"

void apply_hadamard(Universe *u, int target) {
    // 1. Calculate the 'Normalization' factor (1/sqrt(2))
    double factor = 1.0 / sqrt(2.0);
    
    // 2. Identify the bit we are targeting (e.g., qubit 0 = 001)
    long long bit = 1LL << target;

    // 3. Loop through every state in the universe
    for (long long i = 0; i < u->dim; i++) {
        // We only want to find pairs. 
        // If the 'target bit' in index i is 0, we find its partner where it's 1.
        if (!(i & bit)) {
            long long j = i | bit; // The "partner" state

            double complex v0 = u->psi[i];
            double complex v1 = u->psi[j];

            // The Hadamard Math (FOIL happens inside these additions!)
            u->psi[i] = (v0 + v1) * factor;
            u->psi[j] = (v0 - v1) * factor;
        }
    }
}

void apply_cnot(Universe *u, int control, int target) {
    long long ctrl_bit = 1LL << control;
    long long targ_bit = 1LL << target;

    for (long long i = 0; i < u->dim; i++) {
        // Rule: Only act if the control bit is 1 
        // AND to avoid swapping twice, we only act when target bit is 0
        if ((i & ctrl_bit) && !(i & targ_bit)) {
            long long j = i | targ_bit; // The state where target bit is 1

            // Swap the 'stories' (amplitudes)
            double complex temp = u->psi[i];
            u->psi[i] = u->psi[j];
            u->psi[j] = temp;
        }
    }
}

void apply_z(Universe *u, int target) {
    long long bit = 1LL << target;

    for (long long i = 0; i < u->dim; i++) {
        // If the target bit is 1, flip the sign
        if (i & bit) {
            u->psi[i] = -u->psi[i];
        }
    }
}

void apply_s(Universe *u, int target) {
    long long bit = 1LL << target;

    for (long long i = 0; i < u->dim; i++) {
        // Rule: Only act if the target bit is 1
        if (i & bit) {
            // Multiply the amplitude by the imaginary unit 'I'
            u->psi[i] *= I;
        }
    }
}

void apply_x(Universe *u, int target) {
    long long bit = 1LL << target;

    for (long long i = 0; i < u->dim; i++) {
        // We iterate through all states.
        // To avoid double-swapping, we only act when the target bit is 0.
        if (!(i & bit)) {
            long long j = i | bit; // The partner state (where target is 1)

            // SWAP the amplitudes
            double complex temp = u->psi[i];
            u->psi[i] = u->psi[j];
            u->psi[j] = temp;
        }
    }
}

void apply_y(Universe *u, int target) {
    long long bit = 1LL << target;
    
    for (long long i = 0; i < u->dim; i++) {
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