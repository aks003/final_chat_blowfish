import threading
import socket

host='172.16.30.133'
port=55555

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)  
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command Refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt','a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned by the Admin!')
                    f.close()
                else:
                    client.send('Command Refused!'.encode('ascii'))
            else:
                broadcast(message)   # As soon as message recieved, broadcast it.
        
        except:
            if client in clients:
                index = clients.index(client)
                #Index is used to remove client from list after getting diconnected
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the Chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break

def receive():
    while True:
        client,address=server.accept()
        print('Connected with {}'.format(str(address)))

        client.send('NICK'.encode('ascii'))
        nickname=client.recv(1024).decode('ascii')
        
        if nickname in nicknames:
            client.send('SAME'.encode('ascii'))
            client.close()
            continue
        
        with open('bans.txt', 'r') as f:
             bans = f.readlines()
        
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
        
        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'temp@123':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue
        
        nicknames.append(nickname)
        clients.append(client)

        print('Nickname is {}'.format(nickname))
        broadcast("{} joined!!!".format(nickname).encode('ascii'))
        client.send('Connected to server!!!'.encode('ascii'))

        thread=threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('Exit'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked from the server!'.encode('ascii'))

print('Server ready!!!')
receive()