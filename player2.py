import pygame
import socket
from threading import Thread
import pickle
import sys

HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)
obj = bytes(0)
xy = [[75, 75], [175, 75], [275, 75], [75, 225], [175, 225], [275, 225], [75, 375], [175, 375], [275, 375], [75, 525],
      [175, 525], [275, 525], [75, 675], [175, 675], [275, 675], [75, 825], [175, 825], [275, 825]]
x1y = [[1225, 75], [1325, 75], [1425, 75], [1225, 225], [1325, 225], [1425, 225], [1225, 375], [1325, 375], [1425, 375],
       [1225, 525], [1325, 525], [1425, 525], [1225, 675], [1325, 675], [1425, 675], [1225, 825], [1325, 825],
       [1425, 825]]
end = 0


def space(b):
    arr = xy if b else x1y
    for c in range(len(arr)):
        posit = tuple(arr[c])
        if [s for s in cards if s.rect.collidepoint(posit)] == []:
            return posit


def screen_update():
    sc.blit(fon, (0, 0))
    sc.blit(sf1, (0, 0))
    sc.blit(sf2, (1150, 0))
    sc.blit(ring, (550, 250))
    sc.blit(deck.image, deck.rect)
    cards.draw(sc)
    pygame.display.update()
    pygame.time.delay(50)
    cards.update()


def screen_update1():
    sc.blit(fon, (0, 0))
    winner = pygame.sprite.Sprite
    winner.image = pygame.image.load('winner.png').convert_alpha()
    winner.image = pygame.transform.scale(winner.image, (winner.image.get_width() // 3, winner.image.get_height() // 3))
    winner.rect = winner.image.get_rect()
    winner.rect.center = (250, 450)
    sc.blit(sf1, (0, 0))
    sc.blit(sf2, (1150, 0))
    sc.blit(ring, (550, 250))
    sc.blit(deck.image, deck.rect)
    cards.draw(sc)
    sc.blit(winner.image, winner.rect)
    pygame.display.update()
    pygame.time.delay(50)
    cards.update()


def screen_update2():
    sc.blit(fon, (0, 0))
    drawer = pygame.sprite.Sprite
    drawer.image = pygame.image.load('draw2.png').convert_alpha()
    drawer.image = pygame.transform.scale(drawer.image, (drawer.image.get_width() // 5, drawer.image.get_height() // 5))
    drawer.rect = drawer.image.get_rect()
    drawer.rect.center = (750, 400)
    sc.blit(sf1, (0, 0))
    sc.blit(sf2, (1150, 0))
    sc.blit(ring, (550, 250))
    sc.blit(deck.image, deck.rect)
    cards.draw(sc)
    sc.blit(drawer.image, drawer.rect)
    pygame.display.update()
    pygame.time.delay(50)
    cards.update()


def screen_update3():
    sc.blit(fon, (0, 0))
    looser = pygame.sprite.Sprite
    looser.image = pygame.image.load('looser.png').convert_alpha()
    looser.image = pygame.transform.scale(looser.image, (looser.image.get_width() // 5, looser.image.get_height() // 5))
    looser.rect = looser.image.get_rect()
    looser.rect.center = (250, 450)
    sc.blit(sf1, (0, 0))
    sc.blit(sf2, (1150, 0))
    sc.blit(ring, (550, 250))
    sc.blit(deck.image, deck.rect)
    cards.draw(sc)
    sc.blit(looser.image, looser.rect)
    pygame.display.update()
    pygame.time.delay(50)
    cards.update()


class Player():
    end = 0

    def __init__(self, addr):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(addr)  # подключаемся к айпи адресу сервера
        self.players = []  # Создаем массив для хранения данных об игроках
        data = self.soc.recv(2048)
        data1 = pickle.loads(data)
        self.num = data1[1]
        print("------------------------------")
        Thread(target=self.receiving).start()
        Thread(target=self.sending).start()

    def receiving(self):
        while True:
            try:
                data = self.soc.recv(2048)  # 1024 бит -


выделяемая
память
на
сообщение
data1 = pickle.loads(data)
lbl = data1[0]
if data1[0] == "hand_out":
    # print(data1)
    Card(data1)
elif [s for s in cards if s.name == lbl] != []:
    spr = [s for s in cards if s.name == lbl][0]
    spr.c_update(data1)
if data1 == "Q\n":
    self.soc.close()
elif data1[0] == "winner":
    if data1[1] == self.num:
        print("you are winner")
        self.end = 1
    else:
        print("you are not winner")
        self.end = 3
if data1 == "winner_no":
    print("not winner")
    self.end = 2
except:
exit()


def sending(self):
    self.soc.send(obj)


class Card(pygame.sprite.Sprite):
    x, y = 250, 250
    q0, q1 = 0, 0

    def __init__(self, attr):
        pygame.sprite.Sprite.__init__(self)
        self.name = attr[4]
        self.image = pygame.image.load(attr[1]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 1.4, self.image.get_height() // 1.4))
        self.rect = self.image.get_rect()
        self.plr = attr[5]
        self.rect.center = space(self.plr == player.num)
        cards.add(self)

    def c_update(self, param):
        self.rect.center = param[1]
        cards.move_to_front(self)


player = Player((HOST, PORT))
cards = pygame.sprite.LayeredUpdates()
size = w, h = 1500, 900
sc = pygame.display.set_mode(size)
fon = pygame.image.load('fon.jpg')
sc.blit(fon, (0, 0))
sf1 = pygame.Surface((350, 900))
sf1.fill((95, 95, 93))
sc.blit(sf1, (0, 0))
sf2 = pygame.Surface((350, 900))
sf2.fill((95, 95, 93))
sc.blit(sf2, (1150, 0))
ring = pygame.Surface((400, 400), pygame.SRCALPHA)
pygame.draw.circle(ring, (255, 255, 255), (200, 200), 200, width=10)
sc.blit(ring, (550, 250))
deck = pygame.sprite.Sprite
deck.image = pygame.image.load('Deck.png').convert_alpha()
deck.image = pygame.transform.scale(deck.image, (deck.image.get_width() // 1.4, deck.image.get_height() // 1.4))
deck.rect = deck.image.get_rect()
deck.rect.center = (750, 100)

while 1:

    for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if [s for s in cards if s.rect.collidepoint(pos)] != []:
                spr = [s for s in cards if s.rect.collidepoint(pos)][0]
                if spr.plr == player.num:
                    spr.rect.center = (750, 450)
                    cards.move_to_front(spr)
                    obj = pickle.dumps([spr.name, spr.rect.center])
                    player.sending()
                    pygame.display.update()
                    spr.plr = 2
                    if [c for c in cards if c.plr == player.num] == []:
                        obj = pickle.dumps(['winner', player.num])
                        # obj = pickle.dumps('winner_' + str(player.num))
                        player.sending()
            elif deck.rect.collidepoint(pos):
                obj = pickle.dumps('get1')
                player.sending()
        if (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE) or (i.type == pygame.QUIT):
            obj = pickle.dumps('Q')
            # print(obj)
            player.sending()
            sys.exit()

    if player.end == 0:
        screen_update()
    elif player.end == 1:
        screen_update1()
    elif player.end == 2:
        screen_update2()
    elif player.end == 3:
        screen_update3()
