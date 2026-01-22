#ifndef THREAD_H
#define THREAD_H

#include "universe.h"

// 1. The Kernel Signature -- Any function matching this shape can be parallelized.
typedef void (*KernelFunc)(Universe *u, int target, int control, long long start, long long end);

// 2. The Dispatcher -- Use this to launch any kernel across all available CPU cores.
void dispatch_parallel(Universe *u, KernelFunc kernel, int target, int control);

#endif