#include <math.h>
#include <complex.h>
#include "universe.h"

/* --- KERNEL FUNCTIONS --- */
/* Pure math. Run in parallel later. */

void kernel_hadamard(Universe *u, int target, int control, double param, long long start, long long end) {
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

void kernel_x(Universe *u, int target, int control, double param, long long start, long long end) {
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

void kernel_y(Universe *u, int target, int control, double param, long long start, long long end) {
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

void kernel_z(Universe *u, int target, int control, double param, long long start, long long end) {
    long long bit = 1LL << target;
    for (long long i = start; i < end; i++) {
        if (i & bit) {
            u->psi[i] = -u->psi[i]; // If the target bit is 1, flip the sign
        }
    }
}

void kernel_s(Universe *u, int target, int control, double param, long long start, long long end) {
    long long bit = 1LL << target;

    for (long long i = start; i < end; i++) {
        // Rule: Only act if the target bit is 1
        if (i & bit) {
            // Multiply the amplitude by the imaginary unit 'I'
            u->psi[i] *= I;
        }
    }
}

void kernel_t(Universe *u, int target, int control, double param, long long start, long long end) {
    long long bit = 1LL << target;
    
    // Pre-calculate the complex constant for 45 degrees
    // 0.70710678 + 0.70710678i
    double complex phase = cexp(I * M_PI / 4.0); // e^(iπ/4)

    for (long long i = start; i < end; i++) {
        // Apply only if the qubit is |1>
        if (i & bit) {
            u->psi[i] *= phase;
        }
    }
}

void kernel_cnot(Universe *u, int target, int control, double param, long long start, long long end) {
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

void kernel_phase(Universe *u, int target, int control, double param, long long start, long long end) {
    long long bit = 1LL << target;
    double complex phase_factor = cexp(I * param); // Euler's formula (e^iθ)

    for (long long i = start; i < end; i++) {
        if (i & bit) {
            u->psi[i] *= phase_factor;
        }
    }
}

void kernel_swap(Universe *u, int target, int control, double param, long long start, long long end) {
    long long bit_a = 1LL << target;  // "Target" as Qubit A
    long long bit_b = 1LL << control; // "Control" as Qubit B (reused parameter)
    
    for (long long i = start; i < end; i++) {
        // We only swap if the bits are DIFFERENT (01 swaps with 10)
        // If they are 00 or 11, swapping does nothing.
        int val_a = (i & bit_a) != 0;
        int val_b = (i & bit_b) != 0;
        
        if (val_a != val_b) {
            // Check to ensure we only swap once (e.g., when we encounter the smaller index)
            // Calculate the partner index 'j'. Only swap if i < j.
            
            long long j = i ^ bit_a ^ bit_b; // Construct partner index 'j' by flipping both bits
            
            if (i < j) {
                double complex temp = u->psi[i];
                u->psi[i] = u->psi[j];
                u->psi[j] = temp;
            }
        }
    }
}

void kernel_cz(Universe *u, int target, int control, double param, long long start, long long end) {
    long long bit_t = 1LL << target;
    long long bit_c = 1LL << control;
    long long mask = bit_t | bit_c;

    for (long long i = start; i < end; i++) {
        if ((i & mask) == mask) { // If both bits are 1
            u->psi[i] = -u->psi[i];
        }
    }
}

void kernel_toffoli(Universe *u, int target, int control, double param, long long start, long long end) {
    int control2 = (int)param; // Hack: Cast double back to int
    
    long long t_bit = 1LL << target;
    long long c1_bit = 1LL << control;
    long long c2_bit = 1LL << control2;
    
    long long mask = c1_bit | c2_bit;

    for (long long i = start; i < end; i++) {
        
        if ((i & mask) == mask) { // If both controls are 1...
            if (!(i & t_bit)) { // ... we act on the target (avoid double swap logic)
                long long j = i | t_bit;
                double complex temp = u->psi[i];
                u->psi[i] = u->psi[j];
                u->psi[j] = temp;
            }
        }
    }
}