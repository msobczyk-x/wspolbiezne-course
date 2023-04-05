import posix_ipc
import os
import signal
import mmap
import pickle

def draw_board(arr):
    print("    0   1   2 ")
    print("   --- --- ---")
    print(f"0 | {arr[0][0]} | {arr[0][1]} | {arr[0][2]} |")
    print("   --- --- ---")
    print(f"1 | {arr[1][0]} | {arr[1][1]} | {arr[1][2]} |")
    print("   --- --- ---")
    print(f"2 | {arr[2][0]} | {arr[2][1]} | {arr[2][2]} |")
    print("   --- --- ---")


def init_board_array():
    board = []
    for i in range(3):
        board.append([])
        for j in range(3):
            board[i].append(" ")
    return board


# initializing the board
array = init_board_array()
semaphore_turn = None
shrd_mem = None
turn = 0
symbol = ""
mm = None

def signal_handler(signal, frame):
    posix_ipc.unlink_semaphore(semaphore_turn)
    posix_ipc.unlink_shared_memory(shrd_mem)


signal.signal(signal.SIGINT, signal_handler)
# main function

if __name__ == "__main__":


    try:
        semaphore_turn = posix_ipc.Semaphore(
            "./semaphore_turn", posix_ipc.O_CREX, mode=0o777, initial_value=1
        )
        symbol = "O"
    except posix_ipc.ExistentialError:
        semaphore_turn = posix_ipc.Semaphore("./semaphore_turn")
        symbol = "X"

    print("Welcome to Tic Tac Toe!")

    while True:
        print("array: " + str(array))
        
        if turn == 0:
            print("Oponnent's turn!")
        with semaphore_turn:
            
            try:
        
                shrd_mem = posix_ipc.SharedMemory("./board", posix_ipc.O_CREX, 0o777, size=9)


            except posix_ipc.ExistentialError:
                shrd_mem = posix_ipc.SharedMemory("./board", mode=0o777)

            turn = 1
            if turn:
                print("Your turn!")
                print("Your symbol is: " + symbol)
                draw_board(array)
                choice = input("Enter your move (X,Y): ")
                choice = choice.split(",")
                x = int(choice[0])
                y = int(choice[1])
                array[x][y] = symbol
                turn = 0
                shrd_mem.close_fd()

                

