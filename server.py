import socket
import threading

HEADER = 1024
PORT = 8881
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "#DISCONNECT"
active = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

connections = []
nicknames = []
chat_history = []

def broadcast(message):
    for connection in connections:
        connection.send(message).encode(FORMAT)
        print(message)

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address}")
    connected = True
    while connected:
        try:
            msg_length = connection.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = connection.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    broadcast(f"[DISCONNECTING] {address}...")
                    connected = False
                broadcast(f"{address} {msg}")
        except Exception as err:
            index = connections.index(connection)
            connections.remove(connection)
            nickname = nicknames.index(index)
            nicknames.remove(nickname)
            broadcast(f"{nickname} has left\n{str(err)}")
            connected = False
            
    connection.close()

def thread_connections(conn, addr):
    handle = threading.Thread(target=handle_client, args=(conn, addr))
    handle.start()
    conn_count = threading.active_count() - 1
    return conn_count

def recieve():
    connected = True
    while connected:
        connection, address = server.accept()
        nickname = connection.recv()
        nicknames.append(nickname)
        connections.append(connection)
        broadcast(f"{nickname} joined the chat")
        all_connections = thread_connections(connection, address)
        print(f"[ACTIVE CONNECTIONS] {all_connections}")

def start():
    server.listen()
    recieve()


if __name__ == "__main__":
    print(f"Starting server on [{SERVER}]")
    start()
    print(f"Listening on port: {PORT}")