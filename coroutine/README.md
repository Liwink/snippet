### Operating System

* Neither CPUs nor applications know anything about multitasking. **OS** know about it.
* By rapidly switching between tasks, the os does allow multitasking.
* An operating system uses **interrupts** and **traps** to gain control and CPU runs code that's part of the OS 

##### An Insight

* The yield statement is a kind of 'trap'
* When a generator function hit a 'yield' statement, it immediately suspends execution
* Control is passes back to whatever code made generator function run

##### Motivation

* There has been a lot of recent interest in alternative to threads (especially due to the GIL)
* Non-blocking and asynchronous I/O
* Example: servers capable of supporting thousands of simultaneous client connections