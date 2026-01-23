#ifndef SCIENCE_H
#define SCIENCE_H

#include "universe.h"

void apply_noise(Universe *u, int target, double probability);
double get_expectation(Universe *u, int target);

#endif