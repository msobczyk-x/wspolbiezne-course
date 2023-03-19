import hashlib
import time
def checkData(filename):
    hashOnEnd = hashlib.md5(open(filename,'rb').read()).hexdigest()
    if hashOnStart == hashOnEnd:
        return False
    else:
        return True

filename = 'dane.txt'

while True:
    hashOnStart = hashlib.md5(open(filename,'rb').read()).hexdigest()
    print("Oczekiwanie na dane")
    wait = True
    while wait:
        if checkData(filename):
            wait = False
    print("Zmieniono dane")
    time.sleep(1)
    number = open(filename, 'r').read()
    print(number)
    open('wynik.txt', 'w').write(str(pow(int(number),2)))
    print("Wynik zapisano do pliku")
    wait = True

