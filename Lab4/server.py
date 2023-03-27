import os
import signal
import hashlib
import time


# Definicja struktury postaci
class Postac:
    def __init__(self, id, nazwisko):
        self.id = id
        self.nazwisko = nazwisko


# Tablica struktur postaci
baza_danych = [Postac(1, "Kowalski"), Postac(2, "Nowak"), Postac(3, "Wójcik")]


# Obsługa sygnałów
def obsluga_sygnalow(signum, frame):
    if signum == signal.SIGUSR1:
        print("Otrzymano sygnał SIGUSR1 - kończenie pracy serwera")
        exit()
    elif signum == signal.SIGHUP or signum == signal.SIGTERM:
        print("Otrzymano sygnał SIGHUP lub SIGTERM - zatrzymywanie serwera")
        global koniec
        koniec = True


# Utworzenie kolejek FIFO
sciezka_serwer = "./server"

checksum = ""
try:
    os.mkfifo(sciezka_serwer)

except FileExistsError:
    pass

# Pętla nieskończona serwera
koniec = False

while not koniec:
    print("Oczekiwanie na zapytanie od klienta...")

    with open(sciezka_serwer) as serwer:
        print("Otrzymano zapytanie od klienta")
        # Odczytanie zapytania od klienta
        dane = serwer.readline().split(",")
        
        id = int(dane[0])
        sciezka_klienta = dane[1]
        print("ID: " + str(id))
        print("Ścieżka klienta: " + sciezka_klienta)

        # Szukanie wpisu w bazie danych
        wpis = None
        for postac in baza_danych:
            if postac.id == id:
                wpis = postac

        # Wysłanie odpowiedzi do klienta
        if wpis is not None:
            odpowiedz = wpis.nazwisko
        else:
            odpowiedz = "Nie ma"

        dlugosc_odpowiedzi = len(odpowiedz)
        dlugosc_pakietu = 4 + dlugosc_odpowiedzi
        pakiet = bytearray(dlugosc_pakietu)

        # Konwersja długości pakietu na 4-bajtowy int w kolejności sieciowej
        pakiet[0:4] = dlugosc_pakietu.to_bytes(4, byteorder='big')

        # Dodanie odpowiedzi do pakietu
        pakiet[4:] = odpowiedz.encode('utf-8')

        # Zapisanie pakietu do kolejki klienta
        with open(sciezka_klienta, 'wb') as klient:
            klient.write(pakiet)

        print("\n")
        
        print("Wysłano odpowiedź do klienta")
    # Obsługa sygnałów podczas oczekiwania na kolejne zapytanie
    signal.signal(signal.SIGUSR1, obsluga_sygnalow)
    signal.signal(signal.SIGHUP, obsluga_sygnalow)
    signal.signal(signal.SIGTERM, obsluga_sygnalow)

# Usunięcie kolejek FIFO
os.unlink(sciezka_serwer)
