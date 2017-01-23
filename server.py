from network.Server import GameServer
from game.Player import Player
import socket

server = GameServer(localaddr=(socket.gethostbyname(socket.gethostname()), 32078))

print(socket.gethostbyname(socket.gethostname()))

server.Launch()
