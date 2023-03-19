import hashlib
import os
import time
while True:
    if os.path.exists("dane_server.txt"):
        print("Otrzymano dane od klienta")
        print("Blokuje dostęp do pliku ...")
        open("lockfile","w").write("lock")
        clientFile=open("dane_server.txt","r").read()
        
        clientText = open("dane_client.txt" ,"r").read() 
    
        inputText = input("Podaj swój text (server): ")
    
        open(clientFile,"w").write(clientText + inputText)
        print("Wysłano dane do klienta")
        os.remove("lockfile")
        os.remove("dane_server.txt")
    time.sleep(1)
    print("Oczekiwanie na klienta ...")
    