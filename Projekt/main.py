import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Obstruction")

# Set up the game board
BOARD_SIZE = 8
CELL_SIZE = 80
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Draw the game board on the screen
# Draw the game board on the screen
# Draw the game board on the screen
def draw_board():
    screen.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
            if board[row][col] == 1:
                pygame.draw.line(screen, RED, (col * CELL_SIZE + 10, row * CELL_SIZE + 10), ((col + 1) * CELL_SIZE - 10, (row + 1) * CELL_SIZE - 10), 5)
                pygame.draw.line(screen, RED, ((col + 1) * CELL_SIZE - 10, row * CELL_SIZE + 10), (col * CELL_SIZE + 10, (row + 1) * CELL_SIZE - 10), 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 10, 5)
            # Draw a grey rectangle around the 3x3 square around the player's or computer's move
            if board[row][col] != 0:
                pygame.draw.rect(screen, (128, 128, 128), ((col - 1) * CELL_SIZE, (row - 1) * CELL_SIZE, 3 * CELL_SIZE, 3 * CELL_SIZE))
                if board[row][col] == 1:
                    pygame.draw.line(screen, RED, (col * CELL_SIZE + 10, row * CELL_SIZE + 10), ((col + 1) * CELL_SIZE - 10, (row + 1) * CELL_SIZE - 10), 5)
                    pygame.draw.line(screen, RED, ((col + 1) * CELL_SIZE - 10, row * CELL_SIZE + 10), (col * CELL_SIZE + 10, (row + 1) * CELL_SIZE - 10), 5)
                elif board[row][col] == 2:
                    pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 10, 5)
                    
# Handle player moves
def player_move(row, col):
    if board[row][col] == 0:
        board[row][col] = 1
        return True
    else:
        return False

# Check for a winner
def check_winner():
    # Check rows
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - 2):
            if board[row][col] == board[row][col+1] == board[row][col+2] != 0:
                return board[row][col]
    # Check columns
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - 2):
            if board[row][col] == board[row+1][col] == board[row+2][col] != 0:
                return board[row][col]
    # Check diagonals
    for row in range(BOARD_SIZE - 2):
        for col in range(BOARD_SIZE - 2):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] != 0:
                return board[row][col]
            if board[row][col+2] == board[row+1][col+1] == board[row+2][col] != 0:
                return board[row][col+2]
    # Check for tie
    if all(cell != 0 for row in board for cell in row):
        return 0
    # No winner yet
    return None

# Handle computer moves
def computer_move():
    empty_cells = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if board[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 2

# Initialize the winner variable
winner = None

# Create a game loop to keep the game running
running = True
player_turn = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP and player_turn:
            # Get the row and column of the clicked cell
            row = event.pos[1] // CELL_SIZE
            col = event.pos[0] // CELL_SIZE
            if player_move(row, col):
                winner = check_winner()
                if winner is not None:
                    running = False
                else:
                    player_turn = False
        elif not player_turn:
            computer_move()
            winner = check_winner()
            if winner is not None:
                running = False
            else:
                player_turn = True
        if winner is not None:
            if winner == 0:
                print("Tie!")
            elif winner == 1:
                print("You win!")
            else:
                print("Computer wins!")
            running = False

    # Draw the game board on the screen
    draw_board()

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()