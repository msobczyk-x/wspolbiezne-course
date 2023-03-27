import os
import hashlib
import time
number = 1
while True:
    try:
        os.mkfifo('./client'+str(number))
    except FileExistsError:
        number+=1
        continue
    
    file_name = './client'+str(number)
    print('Created fifo: '+file_name)
    client_fifo_hash = hashlib.md5(file_name.encode('utf-8')).hexdigest()
    id = input('Enter ID: ') 
    print('Sending request to server FIFO: ./server')
    odpowiedz = (str(id)+','+file_name)

    server_fifo = open('./server', 'w')
    server_fifo.write(f"{odpowiedz}\n")
    server_fifo.flush()
    server_fifo.close()
      
    
        
    client_fifo = open(file_name, 'r')
    client_fifo = open(file_name, 'r')
    line = client_fifo.readline()
    print('Received response from server: '+str(line))
    client_fifo.close()
        
    break
        
        
os.unlink(file_name)
    
    
        
    