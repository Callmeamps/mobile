import socket
import chainlit as cl
#from server import active

HEADER = 1024
PORT = 8881
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "#DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(message):
    msg = message.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(msg)
    
def recieve():
    client.listen()

@cl.action_callback("connect")
def connect(action):
    client.connect(ADDRESS)
    cl.Message(content=f"Executed {action.name}").send()
    # Optionally remove the action button from the chatbot user interface

@cl.action_callback("disconnect")
def disconnect(action):
    send(DISCONNECT_MESSAGE)
    cl.Message(content=f"Executed {action.name}").send()
    # Optionally remove the action button from the chatbot user interface

def analyse_file():
    pass

@cl.on_chat_start
def start():
    nickname = cl.AskUserMessage(content="What's your Nickname?", timeout=10).send()
    if nickname:
        cl.Message(content=f"Your Nickname is: {nickname['content']}").send()
    # Connect client to server
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(name="connect", value="connect", description="connect"),
        cl.Action(name="disconnect", value="disconnect", description="disconnect")
    ]
    text_content = "1"
    elements = [
        cl.Text(name="Active", text=text_content, display="page")
    ]

    cl.Message(content="Active", elements=elements).send()
    cl.Message(content="Interact with this action button:", actions=actions).send()

@cl.on_message
def main(message: str):
    """The main function will be called every time a user inputs a message in the chatbot UI.
    [ARGS]
    message: string
    """
    
    # Your custom logic goes here...
    send(message)
    # Send a response back to the user
    cl.Message(
        content=f"Received: {message}",
    ).send()
