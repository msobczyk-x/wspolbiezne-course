import os
import signal
import time
# Baza danych
DATABASE = {
    1: "Kowalski",
    2: "Nowak",
    3: "Wójcik"
}

# Funkcja obsługująca sygnał SIGHUP
def sighup_handler(signum, frame):
    print("Received SIGHUP signal")

# Funkcja obsługująca sygnał SIGTERM
def sigterm_handler(signum, frame):
    print("Received SIGTERM signal")
    exit(0)

# Funkcja obsługująca sygnał SIGUSR1
def sigusr1_handler(signum, frame):
    print("Received SIGUSR1 signal")
    exit(0)

# Rejestracja funkcji obsługi sygnałów
signal.signal(signal.SIGHUP, sighup_handler)
signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGUSR1, sigusr1_handler)

# Ścieżka do kolejki serwera
SERVER_QUEUE_PATH = "./server"

# Utworzenie kolejki serwera
if not os.path.exists(SERVER_QUEUE_PATH):
    os.mkfifo(SERVER_QUEUE_PATH)

print("Server is running...")

# Pętla nieskończona serwera
while True:

    with open(SERVER_QUEUE_PATH, 'rb', buffering=0) as server_queue:
        # Odczytanie zapytania od klienta
        query = server_queue.readline().strip().decode()
        if not query:
            continue

        # Rozdzielenie ID i ścieżki do kolejki klienta
        id, client_queue_path = query.split(',')
        id = int(id)

        # Wyszukanie nazwiska w bazie danych
        if id in DATABASE:
            response = DATABASE[id]
        else:
            response = "Nie ma"

        # Wysłanie odpowiedzi do klienta
        response_bytes = response.encode()
        response_length = len(response_bytes)
        message = response_length.to_bytes(4, byteorder='big') + response_bytes

        with open(client_queue_path, 'wb', buffering=0) as client_queue:
            client_queue.write(message)
