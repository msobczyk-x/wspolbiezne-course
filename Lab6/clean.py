import posix_ipc
from multiprocessing import shared_memory
import os
sem_name = "./semaphore_turn"
mem_name = "./board"


posix_ipc.unlink_semaphore(sem_name)



