from socket import *
from threading import *

from keygen import *
from cryptography.fernet import Fernet

rooms = {}

def send_message(message, room):
    if room in rooms:
        for client in rooms[room]['clients_sockets']:
            client.send(message)

def worker(client, room, password):
    # Key Generate
    key = keygen(password)

    # Cryptography Fernet object
    f = Fernet(key)
    
    while True:
        try:
            enc_message = client.recv(1024)
            message = f.decrypt(enc_message)
            print(message.decode())
            send_message(enc_message, room)
        except:
            # Removing The user
            i = rooms[room]['clients_sockets'].index(client)
            user = rooms[room]['clients_names'][i]
            del rooms[room]['clients_sockets'][i]
            del rooms[room]['clients_names'][i]
            
            message = '{} left "{}" room'.format(user, room)
            print(message)
            send_message(message.encode(), room)
            break

# Receive a connections
def main():
    # Starting Server
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen()
    print('server is started')
    
    while True:
        # wait for a Connection
        client, address = server.accept()
        print("New Connection From {}".format(str(address)))
        
        # Request The Room Name
        client.send('<room>'.encode())
        room = client.recv(1024).decode()
        
        # Request The User Name
        client.send('<user>'.encode())
        user = client.recv(1024).decode()
        
        # Request The Room Password
        client.send('<password>'.encode())
        password = client.recv(1024).decode()
        
        if room not in rooms:
            rooms[room] = {}
            rooms[room]['clients_sockets'] = []
            rooms[room]['clients_names'] = []
            rooms[room]['password'] = password
        
        rooms[room]['clients_sockets'].append(client)
        rooms[room]['clients_names'].append(user)
        
        # if rooms[room]['password'] != password:
        #     client.close()
        #     continue
        
        message = '{} joined "{}" room'.format(user, room)
        print(message)
        send_message(message.encode(), room)
        
        # Start Worker Thread For the Client
        thread = Thread(target=worker, args=(client, room, password))
        thread.start()

main()
