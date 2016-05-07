#include <stdio.h>
#include <pthread.h>
#include <assert.h>

typedef struct __counter_t {
    int value;
    pthread_mutex_t lock;
} counter_t;

void init(counter_t *c) {
    c->value = 0;
    pthread_mutex_init(&c->lock, NULL);
}

void increment(counter_t *c) {
    pthread_mutex_lock(&c->lock);
    c->value++;
    pthread_mutex_unlock(&c-lock);
}

void *
mythread(counter_t, *c)
{
    int i;
    for (i = 0; i < 1e3; i++) {
        increment(c)
    }
    return NULL;
}

int
main(int argc, char *argv[])
{
    pthread_t p1, p2;
    printf("main: begin (counter = %d)\n", counter);
    counter_t c;
    init(c)
    pthread_create(&p1, NULL, mythread, c);
    pthread_create(&p2, NULL, mythread, c);

    pthread_join(p1, NULL);
    pthread_join(p2, NULL);
    printf("main: done with both (counter = %d)\n", counter);
    return 0;

}

