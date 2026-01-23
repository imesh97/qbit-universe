#include <stdio.h>

#include "universe.h"

void print_state(Universe *u) {
    printf("\n--- C-Engine State Dump ---\n");
    
    int printed_any = 0;
    
    // Calculate number of qubits from dimension: log2(dim)
    // We can just loop until 1<<n == dim
    int n_qubits = 0;
    long long temp = u->dim;
    while (temp >>= 1) n_qubits++;

    for (long long i = 0; i < u->dim; i++) {
        double complex val = u->psi[i];
        double prob = cabs(val) * cabs(val); // |amplitude|^2

        // Filter: Only print states with > 0.01% probability to keep it clean
        if (prob > 0.0001) {
            printed_any = 1;
            
            // Print the Ket |...>
            printf("|");
            // Print Binary Representation (High bit to Low bit)
            for (int b = n_qubits - 1; b >= 0; b--) {
                printf("%d", (int)((i >> b) & 1));
            }
            printf("> ");

            // Print Amplitude and Probability
            // creal() and cimag() extract parts of the complex number
            printf(": %.3f %+.3fi  (Prob: %.2f%%)\n", 
                   creal(val), cimag(val), prob * 100.0);
        }
    }
    
    if (!printed_any) {
        printf("  (Vacuum/Empty State)\n");
    }
    printf("---------------------------\n");
}