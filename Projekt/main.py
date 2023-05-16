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
GREY = (128, 128, 128)

# Draw the game board on the screen
# Draw the game board on the screen
# Draw the game board on the screen
def draw_board():
    screen.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Draw the cell
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            pygame.draw.rect(screen, BLACK, cell_rect, 1)
            if board[row][col] == 3:
                pygame.draw.rect(screen, GREY, cell_rect.inflate(-10, -10))

            # Draw the player symbol
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, cell_rect.center, CELL_SIZE // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.rect(screen, BLUE, cell_rect.inflate(-10, -10))

def player_move(row, col):
    if board[row][col] == 3:
        return False
    elif board[row][col] == 0:
        board[row][col] = 1
        # Make adjacent and diagonal cells unplayable
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row+i < BOARD_SIZE and 0 <= col+j < BOARD_SIZE:
                    board[row+i][col+j] = 3
        board[row][col] = 1
        return True
    else:
        return False

# Check for a winner
def check_winner(player_turn):
    if any(0 in row for row in board):
        return None
    else:
        if player_turn:
            return 1
        else:
            return 2

# Handle computer moves

def computer_move():
    empty_cells = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if board[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        
        # Make adjacent cells unplayable
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row+i < BOARD_SIZE and 0 <= col+j < BOARD_SIZE:
                    board[row+i][col+j] = 3
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
                winner = check_winner(player_turn)
                if winner is not None:
                    running = False
                else:
                    player_turn = False
        elif not player_turn:
            computer_move()
            winner = check_winner(player_turn)
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