import socket
import threading

m_server = socket.gethostbyname(socket.gethostname()) 
port = 5965
class utext:
    def __init__(self, text, ctime):
        self.text = text
        self.ctime = ctime