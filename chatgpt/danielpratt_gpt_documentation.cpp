#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <semaphore.h>

#define NUM_THREADS 10000  // Define the number of threads to create

using namespace std;

// Global semaphore and variable
sem_t globalVariable_sem;  // Semaphore for protecting access to globalVariable
int globalVariable = 0;    // Global variable shared between threads

/**
 * Function that adds 1 to the globalVariable.
 * 
 * @param args - Thread argument (thread ID in this case).
 */
void *sampleWork_add(void *args) 
{
    // Generate a local variable with a random value between 0 and 9
    int localVariable = rand() % 10;

    // Dereference the thread ID passed as an argument
    long *tid_addr = (long*)args;
    long tid = *tid_addr;

    // Lock the semaphore to protect the globalVariable
    sem_wait(&globalVariable_sem);
    globalVariable = globalVariable + 1;  // Increment the global variable
    sem_post(&globalVariable_sem);        // Unlock the semaphore

    // Print the thread ID, local variable, and the global variable value
    printf("thread id = %ld; \t Local Variable = %d; \t global Variable = %d \n", tid, localVariable, globalVariable);

    pthread_exit(args);  // Exit the thread
}

/**
 * Function that subtracts 1 from the globalVariable.
 * 
 * @param args - Thread argument (thread ID in this case).
 */
void *sampleWork_sub(void *args) 
{
    // Generate a local variable with a random value between 0 and 9
    int localVariable = rand() % 10;

    // Dereference the thread ID passed as an argument
    long *tid_addr = (long*)args;
    long tid = *tid_addr;

    // Lock the semaphore to protect the globalVariable
    sem_wait(&globalVariable_sem);
    globalVariable = globalVariable - 1;  // Decrement the global variable
    sem_post(&globalVariable_sem);        // Unlock the semaphore

    // Print the thread ID, local variable, and the global variable value
    printf("thread id = %ld; \t Local Variable = %d; \t global Variable = %d \n", tid, localVariable, globalVariable);

    pthread_exit(args);  // Exit the thread
}

/**
 * Main function that creates threads and manages the global variable.
 * 
 * Creates half of the threads for addition and the other half for subtraction.
 * Uses a semaphore to ensure synchronized access to the global variable.
 */
int main() 
{
    pthread_t thread[NUM_THREADS];          // Array to hold thread IDs
    pthread_attr_t thread_attr;             // Thread attributes

    sem_init(&globalVariable_sem, 0, 1);    // Initialize the semaphore
    long tid = 0;                           // Variable to hold thread ID

    srand(time(NULL));                      // Seed the random number generator
    pthread_attr_init(&thread_attr);        // Initialize thread attributes

    // Create half of the threads that add to the global variable
    for (; tid < NUM_THREADS / 2; tid++) 
    {
        if (pthread_create(&thread[tid], &thread_attr, sampleWork_add, &tid))
        {
            // Error handling if thread creation fails
            printf("Error creating thread %ld \n", tid);
            exit(-1);
        }
    }

    // Create the remaining half of the threads that subtract from the global variable
    for (; tid < NUM_THREADS; tid++) 
    {
        if (pthread_create(&thread[tid], &thread_attr, sampleWork_sub, &tid))
        {
            // Error handling if thread creation fails
            printf("Error creating thread %ld \n", tid);
            exit(-1);
        }
    }

    // Wait for all threads to complete
    for (tid = 0; tid < NUM_THREADS; tid++)
    {
        if (pthread_join(thread[tid], NULL))
        {
            // Error handling if thread joining fails
            printf("Error joining thread %ld\n", tid);
        }
    }

    // Output the final value of the global variable
    printf("Global Variable = %d\n", globalVariable);

    return 0;
}
