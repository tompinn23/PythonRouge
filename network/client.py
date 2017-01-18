import socket
import pickle
import select


class Client():
    def __init__(self, address, port, name=None):
        self.address = address
        self.port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.name = name

    def connect(self, name):
        self.name = name
        self.sock.connect((self.address, self.port))
        data = [1, name, {0, 0}]
        self.sock.sendall(pickle.dumps(data))

    def sendMessage(self, msgType, msg):
        data = [msgType, self.name, msg]
        self.sock.sendall(pickle.dumps(data))

    def readData(self):
        rlist, wlist, xlist = select.select([self.sock], [], [])
        for i in rlist:
            data = i.recv(1024)
        if len(data) != 0:
            return data
        else:
            return None

    def disconnnect(self):
        self.sock.close()
