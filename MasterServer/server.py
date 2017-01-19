import socketserver
import threading

class GameServerProtocol(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        splitData = data.split(",")
        if splitData[0] == "hb":
            pass
        if splitData[0] == "nct":
            

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
        print("Server Starting")
        server_thread = threading.Thread(target=server.serve_forever)
        self.server_thread = server_thread
        server_thread.start()
        logging.info("Server Thread Started")
        print("Server Started")
        
        


    def closeServer(self):
        self.server.shutdown()
        logging.info(self.server_thread.isAlive)
