from network.Server import GameServer
from game.Player import Player
import socket

server = GameServer(localaddr=("0.0.0.0", 32078))

print(socket.gethostbyname(socket.gethostname()))

server.Launch()

