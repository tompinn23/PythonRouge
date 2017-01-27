from network.PodSixNet.Channel import Channel
from network.PodSixNet.Server import Server
import time

class ClientChannel(Channel):
    def Network(data):
        print(data)

class GameServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        print("Launched")


    def Connected(self, channel):
        print ("Connected" + str(channel))


gServer = GameServer(localaddr=("0.0.0.0", 8080))
while True:
    time.sleep(0.001)
    gServer.Pump()
    
