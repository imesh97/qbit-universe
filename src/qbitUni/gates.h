#ifndef GATES_H
#define GATES_H

#include "universe.h"

void apply_hadamard(Universe *u, int target);
void apply_cnot(Universe *u, int control, int target);
void apply_z(Universe *u, int target);
void apply_s(Universe *u, int target);
void apply_x(Universe *u, int target);
void apply_y(Universe *u, int target);
void apply_t(Universe *u, int target);
void apply_phase(Universe *u, int target, double angle_radians);
void apply_swap(Universe *u, int q1, int q2);
void apply_cz(Universe *u, int control, int target);
void apply_toffoli(Universe *u, int control1, int control2, int target);
void apply_rx(Universe *u, int target, double angle_radians);

#endif