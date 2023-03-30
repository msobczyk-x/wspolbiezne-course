from ipcqueue import sysvmq
import time

server_queue = sysvmq.Queue(1)
client_queue = sysvmq.Queue(2)
q_size = server_queue.qsize()

dictionary = {
    "kot": "cat",
    "pies": "dog",
    "krowa": "cow",
}

while True:
    client_pid, word = server_queue.get()

    if word in dictionary:
        client_queue.put(dictionary[word], msg_type=client_pid)
    else:
        client_queue.put("Word not found", msg_type=client_pid)
