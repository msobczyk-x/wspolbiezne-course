import os
import time

while True:
    if os.path.exists("lockfile"):
        print("(Lockfile) Oczekiwanie na klienta")
        time.sleep(1)
        if os.path.exists("dane_serwer.txt"):
            inputFilename = open("dane_serwer.txt", "r").read()
            fileText = open(inputFilename, "r").read()
            
            print(fileText)
            inputText = input("Podaj tekst do zapisu:")
            open(inputFilename, "w").write(fileText +"Server: "+ inputText +"\n")
            os.remove("dane_serwer.txt")
            os.remove("lockfile")
    else:
        print("Server jest wolny")
        time.sleep(1)