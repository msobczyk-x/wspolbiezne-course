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
        data = pickle.dumps(array)
        shrd_mem = posix_ipc.SharedMemory("./board", posix_ipc.O_CREX, size=len(data))
        mm = mmap.mmap(shrd_mem.fd, shrd_mem.size)
        mm.write(data)

    except posix_ipc.ExistentialError:
        shrd_mem = posix_ipc.SharedMemory("./board")
        mm = mmap.mmap(shrd_mem.fd, shrd_mem.size)
        data = mm.read(shrd_mem.size)
        array = pickle.loads(data)

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

        draw_board(array)
        with semaphore_turn:
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
                 # Save the array to shared memory
                data = pickle.dumps(array)
                mm.write(data)
                

        # Read the array from shared memory



        print("Oponnent's turn!")
        # read the array from shared memory

