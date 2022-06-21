from socket import *
from threading import *

rooms = {}

def send_message(message, room):
    if room in rooms:
        for client in rooms[room]['clients_sockets']:
            client.send(message)

def worker(client, room):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
            send_message(message.encode(), room)
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
        
        if room not in rooms:
            rooms[room] = {}
            rooms[room]['clients_sockets'] = []
            rooms[room]['clients_names'] = []
        
        rooms[room]['clients_sockets'].append(client)
        rooms[room]['clients_names'].append(user)
        
        message = '{} joined "{}" room'.format(user, room)
        print(message)
        send_message(message.encode(), room)
        
        # Start Worker Thread For the Client
        thread = Thread(target=worker, args=(client, room))
        thread.start()

main()
