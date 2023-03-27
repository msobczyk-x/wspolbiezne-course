# reader.py
import os
from pathlib import Path

fifo_path = Path("fifo")
os.mkfifo(fifo_path)

while True:
    print(fifo_path.read_text())  # blocks until data becomes available