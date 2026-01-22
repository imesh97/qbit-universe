#ifndef GATES_H
#define GATES_H

#include "universe.h"

void apply_hadamard(Universe *u, int target);
void apply_cnot(Universe *u, int control, int target);
void apply_z(Universe *u, int target);
void apply_s(Universe *u, int target);
void apply_x(Universe *u, int target);
void apply_y(Universe *u, int target);

#endif