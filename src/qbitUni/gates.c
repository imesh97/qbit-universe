#include "universe.h"
#include "gates.h"
#include "thread.h"

// --- IMPORT KERNELS ---
extern void kernel_hadamard(Universe *u, int target, int control, long long start, long long end);
extern void kernel_x(Universe *u, int target, int control, long long start, long long end);
extern void kernel_y(Universe *u, int target, int control, long long start, long long end);
extern void kernel_z(Universe *u, int target, int control, long long start, long long end);
extern void kernel_s(Universe *u, int target, int control, long long start, long long end);
extern void kernel_cnot(Universe *u, int target, int control, long long start, long long end);

// --- PUBLIC API ---
void apply_hadamard(Universe *u, int target) {
    dispatch_parallel(u, kernel_hadamard, target, -1);
}

void apply_x(Universe *u, int target) {
    dispatch_parallel(u, kernel_x, target, -1);
}

void apply_y(Universe *u, int target) {
    dispatch_parallel(u, kernel_y, target, -1);
}

void apply_z(Universe *u, int target) {
    dispatch_parallel(u, kernel_z, target, -1);
}

void apply_s(Universe *u, int target) {
    dispatch_parallel(u, kernel_s, target, -1);
}

void apply_cnot(Universe *u, int control, int target) {
    dispatch_parallel(u, kernel_cnot, target, control);
}