from network.PodSixNet.Channel import Channel
from network.PodSixNet.Server import Server
from weakref import WeakKeyDictionary
from game.Map import Map
from game.Player import Player

import time, logging

class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        self.name = "anonymous"
        self.player = Player(0,0,False, 100, '@', self.name)
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)

    def Network(self, data):
        print(data)

    def Network_nickname(self, data):
        self.name = data['nickname']
        self.player.setName(self.name)
        self._server.SendALL({'action': 'updatePlayers', 'updatePlayers': self.player.getPlayerData()})

    def Network_posUpdate(self, data):
       pos = data['posUpdate']
       self.player.x = pos[0]
       self.player.y = pos[1]
       print(self.name)
       self._server.SendALL({'action': 'posUpdate', 'posUpdate': [self.name ,self.player.x,self.player.y]})

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
            print(p.name)
            p.Send(data)

    def sendMap(self, player):
        player.Send({'action': 'gameMap', 'gameMap': self.gmap.mapTo()})
        logging.info("(Server) Sent game map to " + player.name)

    def Launch(self):
        logging.info("(Server) Launched Server")
        while True:
            self.Pump()
            time.sleep(0.0001)
