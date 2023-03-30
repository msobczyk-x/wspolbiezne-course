from ipcqueue import sysvmq
import os

server_queue = sysvmq.Queue(1)
client_queue = sysvmq.Queue(2)
client_pid = os.getpid()
input_word = input("Enter word: ")
server_queue.put([client_pid, input_word])


print(client_queue.get(msg_type=client_pid))
