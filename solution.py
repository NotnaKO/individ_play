import os
import sys
import random
import pygame
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(500, 20, 151, 22))
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sp = ['схема', "спутник", "гибрид"]
        self.comboBox.addItems(self.sp)
        self.comboBox.activated[str].connect(self.choice)
        self.show()

    def choice(self, text):
        global typ
        index = self.sp.index(text)
        if index == 0:
            self.comboBox.setCurrentIndex(0)
            typ = 'map'
        if index == 1:
            self.comboBox.setCurrentIndex(1)
            typ = 'sat'
        if index == 2:
            self.comboBox.setCurrentIndex(2)
            typ = 'sat,skl'
        self.close()


pygame.init()
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Set(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('set.jpg')
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.x = 600 - self.rect.w


def set_map():
    global ch
    app = QApplication(sys.argv)
    ex = MyWidget()
    app.exec_()
    del ex
    ch = True


def draw():
    global map_file, ch, screen
    map_request = f"http://static-maps.yandex.ru/1.x/?&pt={','.join(map(str, coord))}&z={z}&l={typ}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    ch = False


# coord = list(map(float, input().split()))
# z = int(input())
coord = [37.948858, 54.180362]
z = 7
step_y = 181.65 / 2 ** (z - 1)
step_x = 416.26 / 2 ** (z - 1)
screen = pygame.display.set_mode([600, 450])
ch = True
typ = 'map'
setts = Set()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove(map_file)
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                z -= 1
                if z < 0:
                    z = 1
                ch = True
            if event.key == pygame.K_PAGEUP:
                z += 1
                if z > 17:
                    z = 17
                ch = True
            if event.key == pygame.K_UP and coord[1] + step_y < 90:
                coord[1] += step_y
                ch = True
            if event.key == pygame.K_DOWN and coord[1] - step_y > -90:
                coord[1] -= step_y
                ch = True
            if event.key == pygame.K_LEFT and coord[0] - step_x > -180:
                coord[0] -= step_x
                ch = True
            if event.key == pygame.K_RIGHT and coord[0] + step_x < 180:
                coord[0] += step_x
                ch = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if setts.rect.x <= event.pos[0] <= setts.rect.right:
                if setts.rect.y <= event.pos[1] <= setts.rect.y + setts.rect.h:
                    set_map()
                    screen = pygame.display.set_mode([600, 450])
        draw()
        all_sprites.draw(screen)
    pygame.display.flip()
