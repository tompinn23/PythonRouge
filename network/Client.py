from network.PodSixNet.Connection import connection, ConnectionListener


class Client(ConnectionListener):
    def __init__(self, host, port, name):
        self.Connect((host,port))
        connection.Send({"action": "nickname", "nickname": name})
        self.isConnected = False
        self.msgs = []

    def Loop(self):
        connection.Pump()
        self.Pump()

    def Send(self, action, message):
        connection.Send({"action": action, "message": message})


    def Network(self, data):
        print(data)
        self.msgs.append(data)
        # built in stuff

    def Network_connected(self, data):
        print("You are now connected to the server")
        self.isConnected = True

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()
        self.isConnected = False

    def Network_disconnected(self, data):
        print('Server disconnected')
        self.isConnected = False
