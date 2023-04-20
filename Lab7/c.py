import socket

SERVER_IP = 'localhost'
SERVER_PORT = 5000
BUFFER_SIZE = 1024

def get_player_choice():
    while True:
        choice = input('Podaj swój wybór (p - papier, k - kamień, n - nożyce): ').strip().lower()
        if choice in ('p', 'k', 'n'):
            return choice
        else:
            print('Niepoprawny wybór, spróbuj ponownie.')

def print_score(player_score, server_score):
    print(f'Twoje punkty: {player_score}\tPunkty przeciwnika: {server_score}')

def play_game():
    player_score = 0
    opponent_score = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
        while True:
            player_choice = get_player_choice()
            sock.send(player_choice.encode())

            server_choice, result = sock.recv(BUFFER_SIZE).decode().split(',')
            if result == 'win':
                player_score += 1
            elif result == 'lose':
                opponent_score += 1

            print(f'Twój wybór: {player_choice}\tWybór przeciwnika: {server_choice}\tWynik rundy: {result.upper()}')
            print_score(player_score, opponent_score)
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()

if __name__ == '__main__':
    play_game()
