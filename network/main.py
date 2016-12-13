import socketserver
import threading
import pickle
# Lock for making sure that only one thread access the players data at a time.
playerLock = threading.Lock()
# Dictionary containing player xy coords.
players = {}


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
	"""This class just exists to be a subclass of ^"""
	pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port

    HOST, PORT = "localhost", 8080

    server = ThreadedTCPServer((HOST, PORT), GameServerProtocol)
    ip, port = server.server_address
    print(ip, port)

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
