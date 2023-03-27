#!/usr/bin/env python3

import os
import sys


SERWERFIFO = "./serwerfifo"
KLIENTFIFO = "./klientfifo"

if len(sys.argv) != 2:
    print("Użycie: klientfifo [indeks rekordu bazy]")
    sys.exit(1)

home = os.getenv("HOME")
msg = sys.argv[1] + home
index = len(msg)

with open(SERWERFIFO, "w") as fs:
    fs.write(str(index) + msg)

with open(KLIENTFIFO, "r") as fk:
    readbuf = fk.read()
    print(readbuf.strip())