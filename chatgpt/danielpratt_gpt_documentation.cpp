#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <semaphore.h>

#define NUM_THREADS 10000  // Define the total number of threads to be created

// Using C++'s standard namespace
using namespace std;

// Global semaphore and variable
sem_t globalVariable_sem;  // Semaphore to synchronize access to the globalVariable
int globalVariable = 0;    // Shared global variable, accessed and modified by multiple threads

/**
 * This function is executed by each thread in the 'addition' set.
 * It increments the global variable by 1, and it is protected by a semaphore
 * to prevent race conditions when multiple threads try to modify it at the same time.
 *
 * @param args - Pointer to the thread's unique ID (passed during thread creation).
 */
void *sampleWork_add(void *args) 
{
    // Generate a local variable, which is independent for each thread, with a random value (0-9)
    int localVariable = rand() % 10;

    // Retrieve the thread ID from the passed argument
    long *tid_addr = (long*)args;
    long tid = *tid_addr;

    // Critical section: lock the semaphore to protect access to the shared globalVariable
    sem_wait(&globalVariable_sem);
    globalVariable = globalVariable + 1;  // Safely increment the global variable
    sem_post(&globalVariable_sem);        // Unlock the semaphore after updating the global variable

    // Print out the thread ID, local variable, and updated global variable value
    printf("thread id = %ld; \t Local Variable = %d; \t global Variable = %d \n", tid, localVariable, globalVariable);

    // Terminate the thread and return the thread ID as a pointer
    pthread_exit(args);
}

/**
 * This function is executed by each thread in the 'subtraction' set.
 * It decrements the global variable by 1, using a semaphore to prevent race conditions.
 *
 * @param args - Pointer to the thread's unique ID (passed during thread creation).
 */
void *sampleWork_sub(void *args) 
{
    // Generate a random local variable, unique to this thread (random value between 0 and 9)
    int localVariable = rand() % 10;

    // Retrieve the thread ID from the passed argument
    long *tid_addr = (long*)args;
    long tid = *tid_addr;

    // Critical section: lock the semaphore to ensure exclusive access to the global variable
    sem_wait(&globalVariable_sem);
    globalVariable = globalVariable - 1;  // Safely decrement the global variable
    sem_post(&globalVariable_sem);        // Unlock the semaphore after the update

    // Print out the thread ID, local variable, and updated global variable value
    printf("thread id = %ld; \t Local Variable = %d; \t global Variable = %d \n", tid, localVariable, globalVariable);

    // Terminate the thread and return the thread ID as a pointer
    pthread_exit(args);
}

/**
 * Main function to control the program.
 * It creates and manages a set of threads to perform addition and subtraction operations 
 * on the shared global variable. Semaphore is used to ensure synchronization between the threads.
 */
int main() 
{
    pthread_t thread[NUM_THREADS];          // Array to store thread IDs
    pthread_attr_t thread_attr;             // Thread attributes object for controlling thread properties

    // Initialize the semaphore, setting its value to 1 (binary semaphore for mutual exclusion)
    sem_init(&globalVariable_sem, 0, 1);
    
    long tid = 0;                           // A counter used for generating thread IDs

    // Seed the random number generator with the current time
    srand(time(NULL));                      
    pthread_attr_init(&thread_attr);        // Initialize the thread attribute object with default settings

    // Create the first half of the threads to perform addition operations
    for (; tid < NUM_THREADS / 2; tid++) 
    {
        if (pthread_create(&thread[tid], &thread_attr, sampleWork_add, &tid))
        {
            // Error handling: print message and exit if thread creation fails
            printf("Error creating thread %ld \n", tid);
            exit(-1);
        }
    }

    // Create the remaining threads to perform subtraction operations
    for (; tid < NUM_THREADS; tid++) 
    {
        if (pthread_create(&thread[tid], &thread_attr, sampleWork_sub, &tid))
        {
            // Error handling: print message and exit if thread creation fails
            printf("Error creating thread %ld \n", tid);
            exit(-1);
        }
    }

    // Wait for all the threads to finish execution
    for (tid = 0; tid < NUM_THREADS; tid++)
    {
        if (pthread_join(thread[tid], NULL))
        {
            // Error handling: print message if thread joining fails
            printf("Error joining thread %ld\n", tid);
        }
    }

    // Output the final value of the global variable after all threads have completed their work
    printf("Global Variable = %d\n", globalVariable);

    return 0;  // Program ends
}
