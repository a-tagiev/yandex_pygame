from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from random import shuffle
import pickle
import os
import sys
import time

attribs = []
hand_out = []
path = [os.path.join('Cards', file) for file in os.listdir('Cards')]
mean = [file.split('.')[0] for file in os.listdir('Cards')]
names = [file for file in os.listdir('Cards')]
for i in range(len(path)):
    atr = ['hand_out', path[i], mean[i].split('_')[0], mean[i].split('_')[1], names[i]]
    attribs.append(atr)
shuffle(attribs)

i = 0
for el in attribs[:14]:
    attribs[i].append(i % 2)
    hand_out.append(pickle.dumps(attribs[i]))
    i += 1
del attribs[:14]


def accept_incoming_connections():
    number = -1
    while True:
        client, client_address = SERVER.accept()
        print(" присоединился к переписке - ", client_address)
        print("%s:%s присоединился к переписке - " % client_address)
        number = number + 1
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, number)).start()


def handle_client(client, n):
    clients[client] = n
    broadcast(pickle.dumps(["number", n]))
    if len(clients) >= 2:
        for e in hand_out:
            broadcast(e)
            time.sleep(0.1)

    while True:
        msg = client.recv(BUFSIZ)
        msg1 = pickle.loads(msg)
        print(msg1)
        if msg1 != "Q" and msg1 != "get1":
            broadcast(msg)
        elif msg1 == "get1":
            obj = get1(clients[client])
            if obj == 'end':
                print("game over, nobody win")
                broadcast(pickle.dumps('winner_no'))
            else:
                broadcast(obj)

        elif msg1 == "Q":
            print("Q = ", msg)
            broadcast(msg)
            client.close()
            del clients[client]
            broadcast(bytes("%s покинул Игру." % n, "utf8"))
            break


def broadcast(msg):
    for sock in clients:
        sock.send(msg)


def get1(n_clint):
    el = []
    if attribs != []:
        el.extend(attribs[0])
        el.append(n_clint)
        del attribs[0]
        return pickle.dumps(el)
    else:
        return 'end'


clients = {}
addresses = {}
HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 2048
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("ожидание соединения")

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
