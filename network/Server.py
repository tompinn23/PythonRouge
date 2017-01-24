import sys
sys.path.append("../")
from game.Map import Map
from game.Monster import Monster

import pickle
import logging
import time

logging.basicConfig(filename='server.log',level=logging.INFO)

from weakref import WeakKeyDictionary

from network.PodSixNet.Server import Server
from network.PodSixNet.Channel import Channel

class ClientChannel(Channel):
    """
    	This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)

    ##################################
    ### Network specific callbacks ###
    ##################################

    def Network(self, data):
        self.Send({"action": "message", "message": data["message"]})

    def Network_nickname(self, data):
        self.nickname = data['nickname']

    def Network_connected(self,data):
        print("connectedee")



class GameServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self._map = Map(70, 50)
        print('Server launched')
        logging.info("Server Launched")

    def Connected(self, channel):
        self.AddPlayer(channel)

    def AddPlayer(self, player):
        print("New Player" + str(player.addr))
        self.players[player] = True
        print("players", [p for p in self.players])
        time.sleep(2)
        player.Send({"action": "recv_map", "message": pickle.dumps(self._map.game_map)})

    def DelPlayer(self, player):
        print("Deleting Player" + str(player.addr))
        del self.players[player]

    def SendToAll(self, action , message):
        [p.Send({"action": action, "message": message}) for p in self.players]

    def Launch(self):
        self._map.generate_Dungeon(70, 50)
        while True:
            self.Pump()
            time.sleep(0.0001)
