from network import Server
from game import Player
import socket

server = Server(socket.gethostbyname(socket.gethostname()), 32078)

print(socket.gethostbyname(socket.gethostname()))


while server.server_thread.isAlive:
    pass
