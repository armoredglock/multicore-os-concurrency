#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/time.h>

sem_t sem;
long long shared_counter = 0;
long long iterations;

void* increment_counter(void* arg) {
    for (long long i = 0; i < iterations; i++) {
        sem_wait(&sem); // Lock
        shared_counter++;
        sem_post(&sem); // Unlock
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <num_threads> <iterations>\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[1]);
    iterations = atoll(argv[2]);
    pthread_t threads[num_threads];

    // Initialize binary semaphore
    sem_init(&sem, 0, 1);

    struct timeval start, end;
    gettimeofday(&start, NULL);

    // Spawn threads
    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, increment_counter, NULL);
    }

    // Wait for all threads to finish
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    gettimeofday(&end, NULL);
    double time_taken = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_usec - start.tv_usec) / 1000.0;

    printf("==================================================\n");
    printf("      POSIX Semaphore Synchronization Benchmark   \n");
    printf("==================================================\n");
    printf("Threads Spawned      : %d\n", num_threads);
    printf("Increments / Thread  : %lld\n", iterations);
    printf("Expected Counter     : %lld\n", (long long)num_threads * iterations);
    printf("Actual Final Counter : %lld\n", shared_counter);
    printf("Elapsed Time         : %.2f ms\n", time_taken);
    printf("==================================================\n");

    sem_destroy(&sem);
    return 0;
}