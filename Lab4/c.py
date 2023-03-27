import os

# Utworzenie kolejki FIFO dla klienta
number = 1
while True:
    try:
        os.mkfifo(f'./client{number}')
        break
    except FileExistsError:
        number += 1
    
# Nazwa pliku kolejki FIFO klienta
client_queue_path = f'./client{number}'
print(f'Created FIFO: {client_queue_path}')

# Wysłanie zapytania do serwera
id = input('Enter ID: ')
request = f'{id},{client_queue_path}'.encode()
with open('./server', 'wb', buffering=0) as server_queue:
    server_queue.write(request)

# Odczytanie odpowiedzi od serwera
with open(client_queue_path, 'rb', buffering=0) as client_queue:
    response = b''
    while True:
        data = client_queue.read()
        if not data:
            break
        response += data

    if response:
        response_length = int.from_bytes(response[:4], byteorder='big')
        message = response[4:].decode() if response_length > 0 else ''
        print(f'Response from server: {message}')
    else:
        print('No response from server')
