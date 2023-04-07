import socket

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8000))
print('Server is listening...')

# Set up the players
players = {}
player_addresses = []
player_scores = {}

# Wait for two players to connect
while len(players) < 2:
    data, client_address = server_socket.recvfrom(1024)
    player_name = data.decode()
    
    if player_name in players:
        server_socket.sendto(b'Name already taken', client_address)
        continue
    
    players[player_name] = client_address
    player_addresses.append(client_address)
    player_scores[player_name] = 0
    
    server_socket.sendto(b'Welcome to the game!', client_address)

# Start the game
while True:
    # Get the moves from the players
    for player_name, player_address in players.items():
        server_socket.sendto(b'Your turn. Enter your move (rock/paper/scissors): ', player_address)
        data, client_address = server_socket.recvfrom(1024)
        player_move = data.decode().lower()
        
        if player_move not in ['rock', 'paper', 'scissors']:
            server_socket.sendto(b'Invalid move', player_address)
            continue
        
        # Store the player's move
        player_scores[player_name] += 1
        if player_scores[player_name] == 3:
            winner = player_name
            break

    # Determine the winner
    if player_scores[players.keys()[0]] == 3:
        winner = players.keys()[0]
    elif player_scores[players.keys()[1]] == 3:
        winner = players.keys()[1]
    else:
        # Determine the winner of the round
        player1_move = player_scores.keys()[0]
        player2_move = player_scores.keys()[1]
        if player1_move == player2_move:
            result = 'Tie!'
        elif (player1_move == 'rock' and player2_move == 'scissors') or \
             (player1_move == 'paper' and player2_move == 'rock') or \
             (player1_move == 'scissors' and player2_move == 'paper'):
            result = f'{player1_move} beats {player2_move}. {player_scores.keys()[0]} wins the round!'
            player_scores[player1_move] += 1
        else:
            result = f'{player2_move} beats {player1_move}. {player_scores.keys()[1]} wins the round!'
            player_scores[player2_move] += 1

    # Send the result to the players
    for player_address in player_addresses:
        server_socket.sendto(result.encode(), player_address)
    
    if winner:
        # Send the winner to the players
        for player_address in player_addresses:
            server_socket.sendto(f'{winner} wins the game!'.encode(), player_address)
        break
