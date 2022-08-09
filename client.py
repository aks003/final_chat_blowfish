import socket
import threading
import getpass
import os
import sys
import handler
handler.init()
nickname=input('Choose your nickname : ')
if nickname == 'admin':
    password = getpass.getpass(prompt='Enter your pasword: ')
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('172.16.30.133',55555))

stop_thread = False
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(2048).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection is Refused !! Wrong Password")
                        stop_thread = True
                        os._exit(0)
                # Clients those are banned can't reconnect
                elif next_message == 'BAN':
                    print('Connection Refused due to Ban')
                    client.close()
                    stop_thread = True
                    os._exit(0)

                elif next_message == 'SAME':
                    print('Connection Refused as there is another user with same nickname :(')
                    client.close()
                    stop_thread = True
                    os._exit(0)

            elif message == "Exit":
                print('You are kicked out of the room by the admin :(')
                client.close()
                stop_thread= True
                os._exit(0)
            else:
                try:
                    print(message)
                    arr=message.split('*')
                    # print(arr)
                    decrypted_msg=handler.handler_decrypt(arr)
                    print(decrypted_msg)
                except:
                	pass
                  #  print(message)

        except Exception as e: 
            print(e)
            print('Error Occured while Connecting')
            client.close()
            break
        
def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    # 2 for : and whitespace and 6 for /KICK_
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    # 2 for : and whitespace and 5 for /BAN
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                print("Commands can be executed by admins only !!")
        else:
            arr=handler.handler_encrypt(message)
            print(''.join(arr))
            for x in arr:
                client.send(x.encode('ascii'))
                client.send("*".encode('ascii'))

receive_thread=threading.Thread(target=receive)
receive_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()
