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
        self.players= {}
        self.players[name] = Player(0, 0, False, 100, '@', name)
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

    def Network_posUpdate(self, data):
        sData = data['posUpdate']
        print(self.players.values())
        if not sData[0] in self.players.keys():
            self.players[sData[0]] = Player(sData[1], sData[2], False, 100, '@', sData[0])
        else:
            self.players[sData[0]].x = sData[1]
            self.players[sData[0]].y = sData[2]