#include <stdlib.h>
#include <stdio.h>

#include "universe.h"
#include "thread.h"

// --- OS DETECTION ---
#ifdef _WIN32
  #include <windows.h>
  typedef HANDLE ThreadType;
  static int get_cores() { SYSTEM_INFO s; GetSystemInfo(&s); return s.dwNumberOfProcessors; }
#else
  #include <pthread.h>
  #include <unistd.h>
  typedef pthread_t ThreadType;
  static int get_cores() {
      long n = sysconf(_SC_NPROCESSORS_ONLN); 
      return (n > 0) ? (int)n : 1; // fallback to 1 core if sysconf fails
  }
#endif

// --- INTERNAL STRUCTURES ---
typedef struct { // ThreadJob ("briefcase" for each thread)
    Universe *u;
    int target;
    int control;
    long long start;
    long long end;
    KernelFunc kernel; // Pointer to the specific math to run
} ThreadJob;

// --- THE GENERIC WORKER ---
// This is the only function the OS threads actually call. It unpacks the briefcase and runs the specific kernel.
#ifdef _WIN32
DWORD WINAPI generic_worker(LPVOID arg) {
#else
void* generic_worker(void *arg) {
#endif
    ThreadJob *job = (ThreadJob*)arg;
    
    // Execute the math kernel
    job->kernel(job->u, job->target, job->control, job->start, job->end);
    
    return 0;
}

// --- THREAD DISPATCHER ---
void dispatch_parallel(Universe *u, KernelFunc kernel, int target, int control) {
    int num_cores = get_cores();
    if (u->dim < 2048) num_cores = 1; // Don't thread small tasks

    ThreadType *threads = malloc(sizeof(ThreadType) * num_cores);
    ThreadJob *jobs = malloc(sizeof(ThreadJob) * num_cores);
    
    long long chunk = u->dim / num_cores;

    for (int i = 0; i < num_cores; i++) {
        jobs[i].u = u;
        jobs[i].target = target;
        jobs[i].control = control;
        jobs[i].kernel = kernel; // Tell the thread which math to use
        jobs[i].start = i * chunk;
        jobs[i].end = (i == num_cores - 1) ? u->dim : (i + 1) * chunk;

        #ifdef _WIN32
            threads[i] = CreateThread(NULL, 0, generic_worker, &jobs[i], 0, NULL);
        #else
            pthread_create(&threads[i], NULL, generic_worker, &jobs[i]);
        #endif
    }

    // Wait for everyone
    for (int i = 0; i < num_cores; i++) {
        #ifdef _WIN32
            WaitForSingleObject(threads[i], INFINITE);
            CloseHandle(threads[i]);
        #else
            pthread_join(threads[i], NULL);
        #endif
    }

    free(threads);
    free(jobs);
}