from network.PodSixNet.Connection import connection, ConnectionListener
from time import sleep
class ClientListener(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        print("Client Started")

    def Network(self, data):
        print(data)

    def Send(self, message):
        connection.Send(message)

c = ClientListener("localhost",8080)
while True:
    connection.Pump()
    c.Pump()
    sleep(0.001)
