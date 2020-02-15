import os
import sys
import pygame
import requests
import math
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore, QtWidgets


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(571, 493)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(90, 70, 441, 351))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.pushButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.pushButton_2)
        self.checkBox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBox.setChecked(flag)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.checkBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 571, 26))
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
        self.label.setText(_translate("MainWindow", "Слои карты:"))
        self.label_2.setText(_translate("MainWindow", "Поиск объекта:"))
        self.pushButton.setText(_translate("MainWindow", "Искать"))
        self.pushButton_2.setText(_translate("MainWindow", "Сброс поискового результата"))
        self.checkBox.setText(_translate("MainWindow", "Сбрасывать результаты при поиске"))


class UiMainWindow2(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 348)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 811, 201))
        self.label.setObjectName("label")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(20, 230, 171, 31))
        self.checkBox.setObjectName("checkBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 26))
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
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.checkBox.setText(_translate("MainWindow", "Почтовый индекс"))


class MyWidget(QMainWindow, UiMainWindow):
    def __init__(self, t):
        super().__init__()
        self.setupUi(self)
        self.sp = ['схема', "спутник", "гибрид"]
        self.comboBox.addItems(self.sp)
        if t == 'map':
            i = 0
        elif t == 'sat':
            i = 1
        else:
            i = 2
        self.comboBox.setCurrentIndex(i)
        self.comboBox.activated[str].connect(self.choice)
        self.pushButton.clicked.connect(self.search_topo)
        self.pushButton_2.clicked.connect(self.clear)
        self.checkBox.stateChanged.connect(self.ch)
        self.show()

    def ch(self, state):
        global flag
        flag = state

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

    def clear(self):
        global sp
        sp = list()

    def search_topo(self):
        global coord, ch
        text = self.lineEdit.text()
        geo_params = {'apikey': geo_api_key, 'geocode': text, 'format': 'json'}
        response = requests.get(geo_api_server, params=geo_params)
        check(response)
        json_response = response.json()
        point = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        name = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["metaDataProperty"][
            "GeocoderMetaData"][
            'text']
        coord1 = list(map(float, point.split()))
        sp.append(coord1)
        coord = coord1[::]
        self.ou = Out(name)
        self.ou.show()
        self.close()


class Out(QMainWindow, UiMainWindow2):
    def __init__(self, text):
        global lis
        super().__init__()
        self.setupUi(self)
        lis.append(text)
        self.checkBox.stateChanged.connect(self.ind)
        self.ind(False)

    def ind(self, state):
        global sp, lis
        if flag:
            sp = [sp[-1][::]]
            lis = [lis[-1][::]]
        if state == QtCore.Qt.Checked:
            lis2 = []
            for t in lis:
                lis2.append(t + find_ind(t))
            s = '\n'.join(lis2)
        else:
            s = '\n'.join(lis)
        self.label.setText(s)


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


def search_top(c):
    x, y = c
    xt, yt = coord[0] - (300 - x) * step_x / 600, coord[1] + (225 - y) * step_y / 450
    sp.append([xt, yt])
    geo_params = {'apikey': geo_api_key, 'geocode': f'{xt},{yt}', 'format': 'json'}
    response = requests.get(geo_api_server, params=geo_params)
    check(response)
    json_response = response.json()
    name = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["metaDataProperty"][
        "GeocoderMetaData"][
        'text']
    app = QApplication(sys.argv)
    ou = Out(name)
    ou.show()
    app.exec_()


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


def search_org(c):
    x, y = c
    xt, yt = coord[0] - (300 - x) * step_x / 600, coord[1] + (225 - y) * step_y / 450
    geo_params = {'apikey': geo_api_key, 'geocode': f'{xt},{yt}', 'format': 'json'}
    response = requests.get(geo_api_server, params=geo_params)
    check(response)
    json_response = response.json()
    name = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["metaDataProperty"][
        "GeocoderMetaData"][
        'text']
    search_params = {
        "apikey": search_api_key,
        "text": name,
        "lang": "ru_RU",
        "ll": f'{xt},{yt}',
        "spn": '0.5,0.5',
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    check(response)
    json_response = response.json()
    for i in range(10):
        try:
            organization = json_response["features"][i]
            org_name = organization["properties"]["CompanyMetaData"]["name"]
            point = organization["geometry"]["coordinates"]
            if lonlat_distance((xt, yt), point) <= 50:
                name = org_name
                sp.append(point)
                app = QApplication(sys.argv)
                ou = Out(name)
                ou.show()
                app.exec_()
                break
        except IndexError:
            continue


def set_map(t):
    global ch
    app = QApplication(sys.argv)
    ex = MyWidget(t)
    app.exec_()
    del ex
    ch = True


def check(response):
    if not response:
        print("Ошибка выполнения запроса!")
        print(response.content)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)


def draw():
    global map_file, ch, screen
    if sp:
        map_request = f"http://static-maps.yandex.ru/1.x/?&ll={','.join(map(str, coord))}&pt={','.join(map(str, coord))},pmgrs~{'~'.join(list(map(lambda x: f'{x[0]},{x[1]}', sp)))}&z={z}&l={typ}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?&ll={','.join(map(str, coord))}&pt={','.join(map(str, coord))},pmgrs&z={z}&l={typ}"
    response = requests.get(map_request)
    check(response)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    ch = False


def find_ind(text):
    geo_params = {'apikey': geo_api_key, 'geocode': text, 'format': 'json'}
    response = requests.get(geo_api_server, params=geo_params)
    check(response)
    json_response = response.json()
    toponim = json_response['response']['GeoObjectCollection']['featureMember'][0]
    try:
        spi = toponim["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        return f', {spi}'
    except KeyError:
        print('Ошибка объекта! Проверьте адрес!')
        return ''


coord = list(map(float, input().split()))
z = int(input())
# coord = [37.617240, 54.181171]
# z = 13
flag = True
sp = [coord[::]]
step_y = 181.65 / 2 ** (z - 1)
step_x = 416.26 / 2 ** (z - 1)
screen = pygame.display.set_mode([600, 450])
search_api_server = "https://search-maps.yandex.ru/v1/"
geo_api_server = 'https://geocode-maps.yandex.ru/1.x/'
map_api_server = "http://static-maps.yandex.ru/1.x/"
geo_api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
search_api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
ch = True
typ = 'map'
lis = list()
setts = Set()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove('map.png')
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                z -= 1
                if z < 0:
                    z = 1
                ch = True
            elif event.key == pygame.K_PAGEUP:
                z += 1
                if z > 17:
                    z = 17
                ch = True
            elif event.key == pygame.K_UP and coord[1] + step_y < 90:
                coord[1] += step_y
                ch = True
            elif event.key == pygame.K_DOWN and coord[1] - step_y > -90:
                coord[1] -= step_y
                ch = True
            elif event.key == pygame.K_LEFT and coord[0] - step_x > -180:
                coord[0] -= step_x
                ch = True
            elif event.key == pygame.K_RIGHT and coord[0] + step_x < 180:
                coord[0] += step_x
                ch = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if setts.rect.x <= event.pos[0] <= setts.rect.right:
                if setts.rect.y <= event.pos[1] <= setts.rect.y + setts.rect.h:
                    set_map(typ)
                    screen = pygame.display.set_mode([600, 450])
            elif event.button == pygame.BUTTON_LEFT:
                search_top(event.pos)
                ch = True
            elif event.button == pygame.BUTTON_RIGHT:
                search_org(event.pos)
                ch = True
        if ch:
            draw()
            all_sprites.draw(screen)
    pygame.display.flip()
