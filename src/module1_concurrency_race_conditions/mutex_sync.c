/**
 * mutex_sync.c
 * Thread synchronization using POSIX Mutex (pthread_mutex_t).
 *
 * Enforces mutual exclusion on the shared 64-bit integer, eliminating race
 * conditions at the cost of lock acquisition overhead and kernel wait states.
 *
 * Author: Sagnik Datta (24BCT0102)
 * Course: BCSE303L - Operating Systems Laboratory
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#define DEFAULT_THREADS 4
#define DEFAULT_ITERATIONS 1000000

static volatile long long shared_counter = 0;
static pthread_mutex_t lock;

typedef struct {
    int thread_id;
    long long iterations;
} thread_arg_t;

void* worker_mutex(void* arg) {
    thread_arg_t* data = (thread_arg_t*)arg;
    for (long long i = 0; i < data->iterations; i++) {
        pthread_mutex_lock(&lock);
        shared_counter++;
        pthread_mutex_unlock(&lock);
    }
    pthread_exit(NULL);
    return NULL;
}

int main(int argc, char* argv[]) {
    int num_threads = DEFAULT_THREADS;
    long long iterations = DEFAULT_ITERATIONS;

    if (argc >= 2) num_threads = atoi(argv[1]);
    if (argc >= 3) iterations = atoll(argv[2]);

    if (num_threads <= 0 || iterations <= 0) {
        fprintf(stderr, "Usage: %s [num_threads] [iterations_per_thread]\n", argv[0]);
        return 1;
    }

    if (pthread_mutex_init(&lock, NULL) != 0) {
        perror("Mutex init failed");
        return 1;
    }

    pthread_t* threads = malloc(num_threads * sizeof(pthread_t));
    thread_arg_t* args = malloc(num_threads * sizeof(thread_arg_t));

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < num_threads; i++) {
        args[i].thread_id = i;
        args[i].iterations = iterations;
        if (pthread_create(&threads[i], NULL, worker_mutex, &args[i]) != 0) {
            perror("Failed to create thread");
            return 1;
        }
    }

    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed_ms = (end.tv_sec - start.tv_sec) * 1000.0 +
                        (end.tv_nsec - start.tv_nsec) / 1000000.0;

    long long expected = (long long)num_threads * iterations;
    long long lost_updates = expected - shared_counter;

    printf("==================================================\n");
    printf("        POSIX Mutex Synchronization Benchmark     \n");
    printf("==================================================\n");
    printf("Threads Spawned      : %d\n", num_threads);
    printf("Increments / Thread  : %lld\n", iterations);
    printf("Expected Counter     : %lld\n", expected);
    printf("Actual Final Counter : %lld\n", shared_counter);
    printf("Correctness Status   : %s\n", (lost_updates == 0) ? "VERIFIED (100% Consistent)" : "FAILED");
    printf("Elapsed Time         : %.3f ms\n", elapsed_ms);
    printf("Throughput           : %.2f M ops/sec\n", ((double)expected / (elapsed_ms / 1000.0)) / 1000000.0);
    printf("==================================================\n");

    pthread_mutex_destroy(&lock);
    free(threads);
    free(args);
    return 0;
}
