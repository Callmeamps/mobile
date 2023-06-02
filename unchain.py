import os
import socket
from dotenv import load_dotenv
import chainlit as cl
from chainlit import user_session as users
#from server import active
load_dotenv()



HEADER = 1024
PORT = 38880
SERVER = os.getenv("HOST_SERVER")
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "#DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send(message):
    msg = message.encode(FORMAT)
    client.send(msg)
    
def set_nickname(nickname):
    pass

def recieve():
    connected = True
    while connected:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            return message
        except Exception as err:
            print(f"[ERROR] {err}")
            client.close()
            connected = False
            

@cl.action_callback("connect")
def connect_client(action):
    client.connect(ADDRESS)
    cl.Message(content="connected").send()
    nickname = cl.AskUserMessage(content="What's your Nickname?", timeout=10).send()
    if nickname:
        current_user = users.set("nickname", nickname)
        nickname["author"] = str(nickname)
        print(current_user)
        send(nickname['content'])
        cl.Message(content=f"Nickname set: {nickname['content']}").send()
        message = recieve()
        cl.Message(content=f"SYSTEM\n{message}")
    # Optionally remove the action button from the chatbot user interface

@cl.action_callback("disconnect")
def disconnect(action):
    send(DISCONNECT_MESSAGE)
    client.close()
    cl.Message(content=f"Executed {action.name}").send()
        # Optionally remove the action button from the chatbot user interface

def analyse_file():
    pass

@cl.on_chat_start
def start():
    # Connect client to server
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(name="connect", value="connect", description="connect"),
        cl.Action(name="disconnect", value="disconnect", description="disconnect")
    ]
    elements = [
        cl.Text(name="Side Panel", text=str(users), display="side")
    ]

    cl.Message(content="Side Panel", elements=elements).send()
    cl.Message(content="Interact with this action button:", actions=actions).send()

@cl.on_message
def main(message: str):
    """The main function will be called every time a user inputs a message in the chatbot UI.
    [ARGS]
    message: string
    """
    # Your custom logic goes here...
    send(message)
    cast = recieve()
    # Send a response back to the user
    cl.Message(content=f"Received: {cast}").send()
