#include <stdio.h>
#include <pthread.h>
#include <assert.h>
#include <stdlib.h>

pthread_cond_t cond;
pthread_mutex_t mutex;

int buffer;
int count = 0;

void put(int value) {
    assert(count == 0);
    count = 1;
    buffer = value;
}

int get() {
    assert(count == 1);
    count = 0;
    return buffer;
}

void *producer(void *arg) {
    int i;
    for (i = 0; i < 10; i++) {
        pthread_mutex_lock(&mutex);
        while (count == 1)
            pthread_cond_wait(&cond, &mutex);
        put(i);
        pthread_cond_signal(&cond);
        pthread_mutex_unlock(&mutex);
    }
}

void *consumer(void *arg) {
    int i;
    for (i = 0; i < 10; i++) {
        pthread_mutex_lock(&mutex);
        while (count == 0)
            pthread_cond_wait(&cond, &mutex);
        int tmp = get();
        pthread_cond_signal(&cond);
        pthread_mutex_unlock(&mutex);
        printf("%d\n", tmp);
    }
}

int
main(int argc, char *argv[]) {
    pthread_t p1;
    pthread_t p2;

    pthread_create(&p1, NULL, producer, &argc);
    pthread_create(&p2, NULL, consumer, &argc);
    pthread_join(p1, NULL);
    pthread_join(p2, NULL);
    printf("End");
    return 0;
}

