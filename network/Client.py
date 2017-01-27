from network.PodSixNet.Connection import connection, ConnectionListener

import logging
from queue import Queue


class Client(ConnectionListener):
    def __int__(self, host, port, name):
        self.Connect((host, port))
        logging.info("(Client) Client Connected")
        connection.Send({'action': 'nickname', 'message': name})
        self.isConnected = False
        self.msgQ = Queue()

    def Loop(self):
        connection.Pump()
        self.Pump()

    def Send(self, data):
        connection.Send(data)
    #                   #
    # NETWORK CALLBACKS #
    #                   #

    def Network_Connected(self, data):
        logging.info("(Client) Connected")
        self.isConnected = True

    def Network_error(self, data):
        logging.error("(Client) Error: " + data['error'][1])
        self.isConnected = False
        connection.Close()

    def Network_disconnected(self, data):
        logging.info("(Client) Disconnected")
        self.isConnected = False

    def Network_gameMap(self, data):
        self.msgQ.put(data['message'])
