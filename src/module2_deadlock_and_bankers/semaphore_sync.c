#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/time.h>

sem_t sem;
pthread_mutex_t mutex;
long long shared_counter_sem = 0;
long long shared_counter_mutex = 0;
long long iterations;

void* increment_sem(void* arg) {
    for (long long i = 0; i < iterations; i++) {
        sem_wait(&sem);
        shared_counter_sem++;
        sem_post(&sem);
    }
    return NULL;
}

void* increment_mutex(void* arg) {
    for (long long i = 0; i < iterations; i++) {
        pthread_mutex_lock(&mutex);
        shared_counter_mutex++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

double get_time(struct timeval start, struct timeval end) {
    return (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_usec - start.tv_usec) / 1000.0;
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <num_threads> <iterations>\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[1]);
    iterations = atoll(argv[2]);
    pthread_t threads[num_threads];
    struct timeval start, end;

    sem_init(&sem, 0, 1);
    pthread_mutex_init(&mutex, NULL);

    // 1. Semaphore Benchmark
    gettimeofday(&start, NULL);
    for(int i=0; i<num_threads; i++) pthread_create(&threads[i], NULL, increment_sem, NULL);
    for(int i=0; i<num_threads; i++) pthread_join(threads[i], NULL);
    gettimeofday(&end, NULL);
    double time_sem = get_time(start, end);

    // 2. Mutex Benchmark
    gettimeofday(&start, NULL);
    for(int i=0; i<num_threads; i++) pthread_create(&threads[i], NULL, increment_mutex, NULL);
    for(int i=0; i<num_threads; i++) pthread_join(threads[i], NULL);
    gettimeofday(&end, NULL);
    double time_mutex = get_time(start, end);

    printf("======================================\n");
    printf("   Semaphore vs Mutex Benchmark       \n");
    printf("======================================\n");
    printf("Threads: %d | Iterations: %lld\n", num_threads, iterations);
    printf("Semaphore Time : %.2f ms\n", time_sem);
    printf("Mutex Time     : %.2f ms\n", time_mutex);
    printf("======================================\n");

    sem_destroy(&sem);
    pthread_mutex_destroy(&mutex);
    return 0;
}