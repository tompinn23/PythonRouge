from network.Server import GameServer
from game.Player import Player
import socket

server = GameServer(localaddr=(socket.gethostbyname(socket.gethostname()), 32078))

print(socket.gethostbyname(socket.gethostname()))

server.Launch()

ready = False
while not ready:
    print("Ready?")
    for p in server.players:
        print(p.nickname)
    c = input()
    if c.upper() == "YES" or c.upper() == "Y":
        ready = True
    else:
        ready = False

server.SendToAll()