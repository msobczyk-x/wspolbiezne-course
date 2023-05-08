import threading
import math
import time

# Muteks do synchronizacji dostępu do wspólnych zmiennych
mutex = threading.Lock()

# Liczba wątków
num_threads = 128

# Przedział, w którym szukamy liczb pierwszych
start_range = 2
end_range = 1000000

# Lista na liczby pierwsze
prime_numbers = []

# Bariery do synchronizacji wątków

barrier = threading.Barrier(num_threads + 1)

# Funkcja sprawdzająca, czy liczba jest pierwsza
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

# Funkcja wykonywana przez wątek
def thread_function(thread_id, start, end):
    # Oczekiwanie na sygnał startowy


    # Szukanie liczb pierwszych w podprzedziale
    local_primes = []
    for num in range(start, end):
        if is_prime(num):
            local_primes.append(num)

    # Wspólne dodawanie liczb pierwszych do listy
    mutex.acquire()
    prime_numbers.extend(local_primes)
    mutex.release()

    # Oczekiwanie na sygnał zakończenia
    barrier.wait()

# Tworzenie i uruchamianie wątków
threads = []
chunk_size = (end_range - start_range) // num_threads
for i in range(num_threads):
    start = start_range + i * chunk_size
    end = start_range + (i + 1) * chunk_size
    thread = threading.Thread(target=thread_function, args=(i, start, end))
    threads.append(thread)
    thread.start()

# Pomiar czasu przed rozpoczęciem
start_time = time.time()

# Oczekiwanie na zakończenie pracy wątków
barrier.wait()

# Pomiar czasu po zakończeniu
end_time = time.time()

# Wyświetlanie listy liczb pierwszych
#print("Prime numbers:", prime_numbers)

# Wyświetlanie czasu wykonania
execution_time = end_time - start_time
print("Thread number: ",num_threads ,"Execution time:", execution_time, "seconds")
