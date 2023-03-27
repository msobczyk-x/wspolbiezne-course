import os

SERWERFIFO = "./serwerfifo"
KLIENTFIFO = "./klientfifo"

class Nazwiska:
    def __init__(self, ID, nazwisko):
        self.ID = ID
        self.nazwisko = nazwisko
try:
    os.mkfifo(SERWERFIFO)
    os.mkfifo(KLIENTFIFO)
except FileExistsError:
    pass
baza = [Nazwiska(1, "Nowak"), Nazwiska(2, "Kowalski"), Nazwiska(3, "Wisniewski")]

while True:
    readbuf = ""
    dlugosc = ""
    index = ""
    klient = ""
    sciezka = ""
    odpowiedz = "nie ma\n"
    i = j = k = p = dx = ix = 0

    with open(SERWERFIFO, "r") as fs:
        readbuf = fs.readline()

    # pobieranie dlugosci komunikatu
    dlugosc = readbuf[0:2]
    dx = int(dlugosc) + 2

    # ustalanie dlugosci podanej liczby
    p = readbuf.find('/')

    # pobieranie indeksu
    if readbuf[3].isdigit():
        index = readbuf[2:4]
    else:
        index = readbuf[2]
    ix = int(index) - 1
    if readbuf[4].isdigit():
        ix = 22

    # sprawdzanie indeksu
    if ix < 20:
        odpowiedz = baza[ix].nazwisko
    if ix > 20:
        odpowiedz = "nie ma"
    if ix < 0:
        odpowiedz = "nie ma"

    # pobieranie sciezki home klienta
    klient = readbuf[p+1:dx]

    # montowanie sciezki do fifo
    sciezka = klient + KLIENTFIFO

    # otwieranie fifo u klienta
    try:
        fk = os.open(sciezka, os.O_WRONLY)
        os.write(fk, bytes(odpowiedz + "\0", "utf-8"))
        os.close(fk)
    except OSError:
        print("Blad otwarcia\n")