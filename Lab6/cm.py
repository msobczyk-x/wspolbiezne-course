import posix_ipc
import os
import signal
import mmap
import pickle
from multiprocessing import shared_memory
import numpy as np


def draw_board(arr):

    convert_array = np.array(arr).tolist()
    for i in range(len(convert_array)):
        for j in range(len(convert_array[i])):
            if convert_array[i][j] == 1:
                convert_array[i][j] = "O"
            elif convert_array[i][j] == 2:
                convert_array[i][j] = "X"
            else:
                convert_array[i][j] = " "
    print("    0   1   2 ")
    print("   --- --- ---")
    print(
        f"0 | {convert_array[0][0]} | {convert_array[0][1]} | {convert_array[0][2]} |"
    )
    print("   --- --- ---")
    print(
        f"1 | {convert_array[1][0]} | {convert_array[1][1]} | {convert_array[1][2]} |"
    )
    print("   --- --- ---")
    print(
        f"2 | {convert_array[2][0]} | {convert_array[2][1]} | {convert_array[2][2]} |"
    )
    print("   --- --- ---")


def init_board_array():
    board = []
    for i in range(3):
        board.append([])
        for j in range(3):
            board[i].append(0)
    return board


# initializing the board
nparray = np.array(init_board_array())
nparsize = np.array(nparray).nbytes
semaphore_turn = None
shrd_mem = None
turn = 0
symbol = ""
mm = None


# main function

if __name__ == "__main__":

    try:
        semaphore_turn = posix_ipc.Semaphore(
            "./semaphore_turn", posix_ipc.O_CREX, initial_value=1
        )
        symbol = "O"
    except posix_ipc.ExistentialError:
        semaphore_turn = posix_ipc.Semaphore("./semaphore_turn")
        symbol = "X"

    print("Welcome to Tic Tac Toe!")

    while True:

        if turn == 0:
            print("Oponnent's turn!")
        with semaphore_turn:

            try:
                shrd_mem = shared_memory.SharedMemory(name="./board")

                nparray = np.ndarray((3, 3), dtype=np.int8, buffer=shrd_mem.buf)

            except FileNotFoundError:
                shrd_mem = shared_memory.SharedMemory(
                    name="./board", create=True, size=nparsize
                )
                nparray = np.ndarray((3, 3), dtype=np.int8, buffer=shrd_mem.buf)

            turn = 1
            if turn:
                os.system("clear")
                print("Your turn!")
                print("Your symbol is: " + symbol)
                draw_board(nparray)
                choice = input("Enter your move (X,Y): ")
                choice = choice.split(",")
                x = int(choice[0])
                y = int(choice[1])
                if symbol == "O":
                    nparray[y][x] = 1
                else:

                    nparray[y][x] = 2
                turn = 0
                output_array = np.ndarray(
                    nparray.shape, dtype=nparray.dtype, buffer=shrd_mem.buf
                )
                output_array[:] = nparray[:]
                os.system("clear")
                print("Opponent's turn!")
                draw_board(nparray)
