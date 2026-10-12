/**
 * spinlock_atomic_sync.c
 * Hardware Atomics & False Sharing vs Cache Line Alignment Analysis.
 *
 * Part 1: Hardware-level atomic increment (__sync_fetch_and_add) using CPU bus lock.
 * Part 2: False Sharing demonstration - independent variables in the same 64-byte
 *         cache line vs. cache-aligned variables (alignas(64)).
 *
 * Author: Swati Saumya (24BCI0253)
 * Course: BCSE303L - Operating Systems Laboratory
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdalign.h>
#include <time.h>

#define DEFAULT_THREADS 4
#define DEFAULT_ITERATIONS 10000000

// Shared counter for Part 1 (Hardware Atomic)
static volatile long long atomic_counter = 0;

typedef struct {
    int thread_id;
    long long iterations;
} thread_arg_t;

void* worker_atomic(void* arg) {
    thread_arg_t* data = (thread_arg_t*)arg;
    for (long long i = 0; i < data->iterations; i++) {
        __sync_fetch_and_add(&atomic_counter, 1);
    }
    pthread_exit(NULL);
    return NULL;
}

// Structures for Part 2 (False Sharing vs Cache Alignment)
typedef struct {
    long long counter; // Contiguous in memory: shares the same 64B cache line!
} unaligned_worker_t;

typedef struct {
    alignas(64) long long counter; // Padded to dedicated 64B cache line boundary
} aligned_worker_t;

static unaligned_worker_t unaligned_data[16];
static aligned_worker_t aligned_data[16];

void* worker_false_sharing(void* arg) {
    thread_arg_t* data = (thread_arg_t*)arg;
    int id = data->thread_id;
    for (long long i = 0; i < data->iterations; i++) {
        unaligned_data[id].counter++;
    }
    pthread_exit(NULL);
    return NULL;
}

void* worker_cache_aligned(void* arg) {
    thread_arg_t* data = (thread_arg_t*)arg;
    int id = data->thread_id;
    for (long long i = 0; i < data->iterations; i++) {
        aligned_data[id].counter++;
    }
    pthread_exit(NULL);
    return NULL;
}

int main(int argc, char* argv[]) {
    int num_threads = DEFAULT_THREADS;
    long long iterations = DEFAULT_ITERATIONS;

    if (argc >= 2) num_threads = atoi(argv[1]);
    if (argc >= 3) iterations = atoll(argv[2]);

    if (num_threads <= 0 || num_threads > 16 || iterations <= 0) {
        fprintf(stderr, "Usage: %s [num_threads (1-16)] [iterations_per_thread]\n", argv[0]);
        return 1;
    }

    pthread_t* threads = malloc(num_threads * sizeof(pthread_t));
    thread_arg_t* args = malloc(num_threads * sizeof(thread_arg_t));

    struct timespec start, end;

    // --- PART 1: Hardware Atomic Fetch-and-Add ---
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < num_threads; i++) {
        args[i].thread_id = i;
        args[i].iterations = iterations;
        pthread_create(&threads[i], NULL, worker_atomic, &args[i]);
    }
    for (int i = 0; i < num_threads; i++) pthread_join(threads[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &end);
    double atomic_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    // --- PART 2A: False Sharing (Unaligned) ---
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, worker_false_sharing, &args[i]);
    }
    for (int i = 0; i < num_threads; i++) pthread_join(threads[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &end);
    double false_sharing_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    // --- PART 2B: Cache-Aligned (Mitigated) ---
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, worker_cache_aligned, &args[i]);
    }
    for (int i = 0; i < num_threads; i++) pthread_join(threads[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &end);
    double aligned_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    printf("==============================================================\n");
    printf("  Hardware Atomics & Cache Line False-Sharing Profiling      \n");
    printf("==============================================================\n");
    printf("Threads: %d | Iterations per Thread: %lld\n", num_threads, iterations);
    printf("--------------------------------------------------------------\n");
    printf("1. Hardware Atomic (Bus Lock) : %8.2f ms (Count: %lld)\n", atomic_ms, atomic_counter);
    printf("2. False Sharing (Same 64B)   : %8.2f ms (Cache Bouncing)\n", false_sharing_ms);
    printf("3. Cache Aligned (alignas 64) : %8.2f ms (Isolated Line)\n", aligned_ms);
    printf("--------------------------------------------------------------\n");
    printf("False Sharing Speedup Gain    : %.2fx faster with alignment\n", false_sharing_ms / aligned_ms);
    printf("==============================================================\n");

    free(threads);
    free(args);
    return 0;
}
