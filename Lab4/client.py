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
    
    with open('./server', 'w') as server:
        print(str(id)+','+file_name)
    
    
        
    with open(file_name) as client:
        print('Received response from server: '+client.read().strip())
        
    break
        
        
os.unlink(file_name)
    
    
        
    