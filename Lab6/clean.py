import posix_ipc

sem_name = "./semaphore_turn"
mem_name = "./board"

posix_ipc.unlink_semaphore(sem_name)
posix_ipc.unlink_shared_memory(mem_name)