import os
import time
inputFilename = input("Podaj nazwę pliku do odczytu dla serwera: ")

while True:
    if os.path.exists(inputFilename):
        
        if os.path.exists("lockfile"):
            print("Plik jest zablokowany")
            print("Oczekiwanie na serwer ...")
            time.sleep(3)
        else:
            print("Odczytuje dane z pliku ...")
            clientFile = open(inputFilename, "r").read()
            print("Odczytano dane z pliku")
            inputText = input("Podaj swój text (client): ")
            open("dane_client.txt", "w").write(clientFile + inputText)
            open("dane_server.txt","w").write(inputFilename)
            print("Wysłano dane do serwera")
            break   
        