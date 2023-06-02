import socket
import threading

HEADER = 1024
PORT = 8880
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
        msg = message.encode(FORMAT)
        connection.send(msg)
        print(message)

def get_message(connection):
    msg = connection.recv(HEADER).decode(FORMAT)
    return msg

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address}")
    connected = True
    index = connections.index(connection)
    current_connections = len(connections)
    try:
        nickname = nicknames[index]
        while connected:
            try:
                msg = get_message(connection)
                if msg == DISCONNECT_MESSAGE:
                    broadcast(f"[DISCONNECTING] {nickname}...")
                    connections.remove(connection)
                    nicknames.remove(nickname)
                    print(f"[ACTIVE CONNECTIONS] {current_connections}")
                    connected = False
                broadcast(msg)
            except Exception as err:
                connections.remove(connection)
                nicknames.remove(nickname)
                broadcast(f"{nickname} has left\n{str(err)}")
                print(f"[ACTIVE CONNECTIONS] {current_connections}")
                connected = False
    except ValueError as v_err:
        broadcast(f"Unable to add {connection}\n[Error] {v_err}")
    connection.close()

def thread_connections(conn, addr):
    handle = threading.Thread(target=handle_client, args=(conn, addr))
    handle.start()
    conn_count = threading.active_count() - 1
    return conn_count

def recieve(quit):
    connected = True
    while connected:
        if quit.lower == "r":
            connected = False
        connection, address = server.accept()
        nickname = get_message(connection)
        nicknames.append(nickname)
        connections.append(connection)
        join_msg = f"\n\n{nickname} joined the chat"
        broadcast(join_msg)
        for name in nicknames:
            print(f"\nconnected users: {name}\n")
        thread_connections(connection, address)


if __name__ == "__main__":
    connected = True
    while connected:
        stop = input("'Enter' to START\n'q' to QUIT \n'r' to RESTART")
        if stop.lower == "q":
            connected = False
        elif stop.lower == "r":
            print("Restarting server...")
        print("Starting server...")
        server.listen()
        print(f"\n\nRunning at: http://{SERVER}:{PORT}")
        recieve(stop)