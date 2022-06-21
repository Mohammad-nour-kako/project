from socket import *
from threading import *


def receive_worker():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == '<room>':
                client.send(room.encode())
            elif message == '<user>':
                client.send(user.encode())
            else:
                print(message)
        except:
            print("connection Error")
            client.close()
            break

def send_worker():
    while True:
        user_message = input('')
        message = '{}> {}'.format(user, user_message)
        client.send(message.encode())


# main

# Enter Room name
room = input("Enter room name: ")
# Enter User name
user = input("Enter your name: ")

client = socket(AF_INET, SOCK_STREAM)
client.connect(('localhost', 12345))

receive_thread = Thread(target=receive_worker)
receive_thread.start()

send_thread = Thread(target=send_worker)
send_thread.start()
