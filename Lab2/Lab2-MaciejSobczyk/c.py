import os
import time

while True:
    if os.path.exists("lockfile"):
        print("Server jest zajęty")
        time.sleep(1)
    else:
        open("lockfile", "w").close()
        inputFilename = input("Podaj nazwę pliku do odczytu:")
        if os.path.exists(inputFilename):
            fileText = open(inputFilename, "r").read()
            print(fileText)
            inputText = input("Podaj tekst do zapisu:")
            open(inputFilename, "w").write(fileText + "Client: "+ inputText +"\n")
            open("dane_serwer.txt", "w").write(inputFilename)
            print("Zapisano dane")
            break
        else:
            os.remove("lockfile")
            print("Plik nie istnieje")
            