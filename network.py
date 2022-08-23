import pickle
from networkstatic import*
class Network:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = self.connect()

    def get_status(self):
        return self.status

    def connect(self):
        (self.server.connect((m_server, port))) 
        return self.server.recv(64).decode()
    def sendto(self, data):
        try:

            self.server.sendto(pickle.dumps(data), (m_server, port))
            d, a =self.server.recvfrom(64)
            return pickle.loads(d)
        except:
            pass 

    def send(self, data):
        try:
            self.server.send(pickle.dumps(data))
        except:
            pass
    def get(self):
        return pickle.loads(self.server.recv(256))

