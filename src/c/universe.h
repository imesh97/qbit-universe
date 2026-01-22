#ifndef UNIVERSE_H
#define UNIVERSE_H

#include <complex.h>

typedef struct {
    int n_qubits;        // number of bits (e.g., 28)
    long long dim;       // 2^n_qubits (the total number of stories)
    _Complex double *psi; // the pointer to our (e.g. 4GB) memory block
} Universe;

// Function prototypes
Universe* init_universe(int n);
void destroy_universe(Universe *u);
double get_probability(Universe *u, long long index);
long long measure_all(Universe *u);

#endif