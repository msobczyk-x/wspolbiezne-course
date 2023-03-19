import time

liczba = input("Podaj liczbe: ")
open('dane.txt', 'w').write(liczba)

time.sleep(2)

wynik = open('wynik.txt', 'r').read()
print("Dane z pliku 'wynik.txt': ",wynik)
