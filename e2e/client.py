from socket import *
from threading import *

from keygen import *
from cryptography.fernet import Fernet


def receive_worker():
    while True:
        try:
            message = client.recv(1024)
            # print(message)
            if message.decode() == '<room>':
                client.send(room.encode())
            elif message.decode() == '<user>':
                client.send(user.encode())
            else:
                try:
                    message = f.decrypt(message).decode()
                except:
                    message = message.decode()
                print(message)
        except Exception as e:
            print("connection Error")
            client.close()
            break

def send_worker():
    while True:
        user_message = input('')
        message = '{}> {}'.format(user, user_message)
        enc_message = f.encrypt(message.encode())
        client.send(enc_message)


# main

# Enter Room name
room = input("Enter room name: ")
# Enter User name
user = input("Enter your name: ")
# Enter User name
password = input("Enter room password: ")
# Key Generate
key = keygen(password)

# Cryptography Fernet object
f = Fernet(key)

client = socket(AF_INET, SOCK_STREAM)
client.connect(('localhost', 12345))

receive_thread = Thread(target=receive_worker)
receive_thread.start()

send_thread = Thread(target=send_worker)
send_thread.start()
