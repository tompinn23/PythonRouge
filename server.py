from network.Server import GameServer
from game import Player
import socket

server = GameServer(socket.gethostbyname(socket.gethostname()), 32078)

print(socket.gethostbyname(socket.gethostname()))
