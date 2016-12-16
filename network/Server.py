import socketserver
import threading
import pickle
import logging
# Lock for making sure that only one thread access the players data at a time.
playerLock = threading.Lock()
# Dictionary containing player xy coords.
players = {}
entities = {}


class GameServerProtocol(socketserver.BaseRequestHandler):
    """This is the protocol for handling incoming messages."""

    def handle(self):
        data = pickle.loads(self.request.recv(1024))
        print(threading.current_thread())
        if data[0] == 1:
            playerLock.acquire()
            players[data[1]] = data[2]
            playerLock.release()
        response = pickle.dumps(players)
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """This class just exists to be a subclass of
    ThreadingMixIn and TCPServer"""
    pass


class Server():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        server = ThreadedTCPServer((address, port), GameServerProtocol)
        self.server = server
        logging.info("Server Thread Starting")
        server_thread = threading.Thread(target=server.serve_forever)
        self.server_thread = server_thread
        server_thread.start()
        logging.info("Server Thread Started")

    def closeServer(self):
        self.server.shutdown()
        logging.info(self.server_thread.isAlive)