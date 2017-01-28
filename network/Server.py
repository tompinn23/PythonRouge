from network.PodSixNet.Channel import Channel
from network.PodSixNet.Server import Server
from weakref import WeakKeyDictionary
from game.Map import Map

import time, pickle, logging

class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        self.name = "anonymous"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)

    def Network(self, data):
        print(data)

    def Network_nickname(self, data):
        self.nickname = data['nickname']

    def Network_wantMap(self, data):
        self._server.sendMap(self)

class GameServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        print("Launched")
        self.players = WeakKeyDictionary()
        self.gmap = Map(70, 50)
        self.gmap.generate_Dungeon(70, 50)


    def Connected(self, channel):
        print("Connection from:" + str(channel.addr))
        self.AddPlayer(channel)
        channel.Send({'action': 'connected'})

    def AddPlayer(self, channel):
        self.players[channel] = True

    def DelPlayer(self, channel):
        del self.players[channel]
        print("Deleting Player")

    def SendALL(self, data):
        for p in self.players:
            p.Send(data)

    def sendMap(self, player):
        print(self.gmap.mapTo())
        player.Send({'action': 'gameMap', 'gameMap': self.gmap.mapTo()})
        logging.info("(Server) Sent game map to " + player.nickname)

    def Launch(self):
        print(self.gmap.mapTo())
        logging.info("(Server) Launched Server")
        while True:
            self.Pump()
            time.sleep(0.0001)
