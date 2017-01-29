from network.PodSixNet.Connection import connection, ConnectionListener

from game.Player import Player
import logging
from queue import Queue


class Client(ConnectionListener):
    def __init__(self, host, port, name):
        self.Connect((host, port))
        logging.info("(Client) Client Connected")
        self.name = name
        connection.Send({'action': 'nickname', 'nickname': str(name)})
        self.isConnected = False
        self.player = Player(0, 0, False, 100, '@', self.name)
        self.msgQ = Queue()

    def Loop(self):
        connection.Pump()
        self.Pump()

    def Send(self, data):
        connection.Send(data)
    #                   #
    # NETWORK CALLBACKS #
    #                   #
    def Network(self, data):
        self.msgQ.put(data)

    def Network_connected(self, data):
        logging.info("(Client) Connected")
        self.isConnected = True

    def Network_error(self, data):
        logging.error("(Client) Error: " + data['error'][1])
        print("U r fucking connected")
        self.isConnected = False
        connection.Close()

    def Network_disconnected(self, data):
        logging.info("(Client) Disconnected")
        self.isConnected = False