import socket
import sys

# Set up the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8000)

# Register the player
player_name = sys.argv[1]
client_socket.sendto(player_name.encode(), server_address)

# Wait for the game to start
while True:
    data, server_address = client_socket.recvfrom(1024)
