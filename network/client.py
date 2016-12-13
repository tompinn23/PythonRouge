import socket
import random
import pickle
import string
import threading


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))
    data = [1, "Tom" + random.choice(string.ascii_letters),
            [random.randint(0, 40), random.randint(0, 80)]]
    sock.sendall(pickle.dumps(data))
    response = sock.recv(1024)
    msg = pickle.loads(response)
    print(msg)
    input()
    sock.close()


threads = []
for i in range(10):
    t = threading.Thread(target=client)
    threads.append(t)
    t.start()
