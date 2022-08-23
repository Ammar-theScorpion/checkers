from distutils.log import error
import pickle
import threading
 
from networkstatic import*

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((m_server, port))

 
client_lock = threading.Lock()
clients = set()
m_players = []  



header = 64

def handel_connection(conn, client_status):
    print(client_status)
    if client_status == 0:
        conn.send(str.encode(str("same")))
   
    else:
        conn.send(str.encode(str("reflict")))


    while True:
        try:
            piece = pickle.loads(conn.recv(256))
            if not piece:
                break
            print("r")
            with client_lock:
                for c in clients:
                    if c is not conn:
                    
                        c.send(pickle.dumps(piece))
        except socket.error as e:
            print("lost connection", e, client_status)
            break
server.listen()
def start():
    client_counter = 0
    client_status  = 0
    while True:
        conn, addr = server.accept()
        client_status = client_counter%2
        client_counter+=1
        print(f'{addr} has connected')
        with client_lock:
            clients.add(conn)
        print(client_status)
        thread = threading.Thread(target=handel_connection, args=(conn, client_status))
        thread.start()

print("server [Running]")
start()
