from threading import Semaphore
from multiprocessing import shared_memory


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
semaphore = None
shrd_mem = None
turn = 0
# main function

if __name__ == "__main__":
    try:
        shrd_mem = shared_memory.SharedMemory(create=True, size=9, name="board")
    except FileExistsError:
        shrd_mem = shared_memory.SharedMemory(name="board")

    semaphore = Semaphore(1)

    print("Welcome to Tic Tac Toe!")

    draw_board(array)
    while True:
        if semaphore.acquire():
            turn = 1
            if turn:
                print("Your turn!")
                draw_board(array)
                choice = input("Enter your move (X,Y): ")
        else:
            turn = 0
            if not turn:
                print("Oponnent's turn!")
                draw_board(array)
                choice = input("Enter your move (X,Y): ")
                
