import socket

SERVER_IP = 'localhost'
SERVER_PORT = 5000
BUFFER_SIZE = 1024

def get_game_result(player1_choice, player2_choice):
    if player1_choice == 'koniec' or player2_choice == 'koniec':
        return 'koniec'
    elif player1_choice == player2_choice:
        return 'tie'
    elif player1_choice == 'p' and player2_choice == 'k':
        return 'win'
    elif player1_choice == 'k' and player2_choice == 'n':
        return 'win'
    elif player1_choice == 'n' and player2_choice == 'p':
        return 'win'
    
    else:
        return 'lose'

def print_score(player1_score, player2_score):
    print(f'Gracz 1: {player1_score}\tGracz 2: {player2_score}')

def play_game():
    player1_score = 0
    player2_score = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))

    while True:
        player1_choice, player1_addr = sock.recvfrom(BUFFER_SIZE)
        player2_choice, player2_addr = sock.recvfrom(BUFFER_SIZE)

        result = get_game_result(player1_choice.decode(), player2_choice.decode())
        result2 = get_game_result(player2_choice.decode(), player1_choice.decode())

        if result == 'win':
            player1_score += 1
        elif result == 'lose':
            player2_score += 1
        
        
        sock.sendto(f'{player2_choice.decode()},{result}'.encode(), player1_addr)
        sock.sendto(f'{player1_choice.decode()},{result2}'.encode(), player2_addr)

        if result == 'koniec':
            print('Koniec gry')
            print("Resetowanie wyników")
            break
        print(f'Gracz 1 ({player1_addr[0]}:{player1_addr[1]}): {player1_choice.decode()}\tGracz 2 ({player2_addr[0]}:{player2_addr[1]}): {player2_choice.decode()}\tWynik rundy: {result.upper()}')
        print_score(player1_score, player2_score)


if __name__ == '__main__':
    while True:
        try:
            play_game()
        except KeyboardInterrupt:
            break
