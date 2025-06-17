import asyncio

async def task_1():
    print("Task 1: Starting")
    await asyncio.sleep(2)  # Simulates a long I/O task
    print("Task 1: Done")

async def task_2():
    print("Task 2: Starting")
    await asyncio.sleep(1)  # Simulates a shorter I/O task
    print("Task 2: Done")

async def main():
    await asyncio.gather(task_1(), task_2())  # Run tasks concurrently

asyncio.run(main())



'''

COMMUNICATION (asyncio library):
synch -  when a process is dependant on another processes to procede (drone1 gives data to another drone2, and wait for drone2 to complete a task before drone1 takes action)
asynch -  able to give mulitple task without stopping a process (drone1 gives drone2, drone3, drone4, a task but continues the process without denpending on responses)
    --> even if asynch doesnt depend on the response, it need to be able to 'listen' when a proccess failed or succeeded --> need a code to keep track of that
    --> to be able to listen need (ports)
alerts -> notify the main process if a task succeeds or fails
polls -> regularly check the status of each drones task without blocking the main process (used in async)
queue -> manage tasks for drones --> async Queue can assign and retrieve tasks ; ensures each "drone" gets tasks in the right order.
proccesses -> seperate memory spaces to run -->  PID number : a unique ID that idenifties the different running process (task manager)
    Multi Proccesses: multiple proccess running at the same time
    threads: shared its memory with the program; S (proccesses have thier own memory space) --> mainly used for recieving and sending info
await -> "Wait for this task to finish, but dont stop everything else while waiting." EXAMPEL;' Drone1 can send a task to Drone2, await its response, and continue checking on other drones at the same time

'''
