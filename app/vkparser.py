from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread

import sys
import vk_api
import json
import sqlite3
import threading
from datetime import datetime


class VkParser(QObject):
    # Выпилить Qt
    parsingFinished = pyqtSignal()
    # Поменять говнокод с перебором
    # на говнокод со словарями
    def __init__(self,source):
        super().__init__()
        self.pl = {
            1 : "Mobile",
            2 : "iPhone",
            3 : "iPad",
            4 : "Android",
            5 : "Windows Phone",
            6 : "Windows 10",
            7 : "Web"
        }

        self.gender = {1 : "Ж", 2 : "M"}
        self.source = source

    @pyqtSlot()
    def onStart(self):
        print("Parse thread : Start")
        self.loadSettings()
        #threading.Thread(target=self.getGroupSubs, args=[self.source]).start()
        self.getGroupSubs(self.source)

    def initConnectons(self):
        # Селф.автор = пидорас, нахуй так делать, вдруг дети увидят
        self.vk_session = vk_api.VkApi(self.login, self.password)
        self.vk_session.auth()
        self.vk = self.vk_session.get_api()
        self.db_c = sqlite3.connect(self.db_path)
        self.cursor = self.db_c.cursor()

    def tui(self):
        hlp = """Справка :
            parse - Пропарсить группу
            init - Создать окружение (БД + Файл настроек)
            load - загрузить окружение (Выполнить при первом запуске !)
            exit - Выход"""
        print(hlp)
        while(True):
            cmd = input("> ")
            if cmd == "exit":
                break
            if cmd == "parse":
                self.getGroupSubs(input("ID группы: "))
            if cmd == "init":
                self.init_settins()
            if cmd == "load":
                self.loadSettings()
        self.db_c.close()

    def makeDB(self):
        # Ммм, свап говна в дерьмо
        pass

    def init_settins(self):
        settings = {'db_path' : input("DB: "), 'vk_logn' : input("Логин: "), 'vk_pass' : input("Пароль ВК: ")}
        file = open("settings.bin", "wb")
        file.write(json.dumps(settings, indent=2).encode('utf-8'))
        file.close()

    def loadSettings(self):
        file = open("settings.bin", "br")
        settings = json.loads(file.read().decode('utf-8'))
        file.close()
        self.db_path = settings['db_path']
        self.login = settings['vk_logn']
        self.password = settings['vk_pass']
        print(self.db_path, self.login, self.password)
        self.initConnectons()

    def parsedata(self, data, g_id):
        lids_count = 0
        for item in data:
            try:
                status = item['is_closed']
            except:
                status = True

            if status:
                continue

            name = self.fuck(item['first_name'] + " " + item['last_name'])
            # Испровить эту хуету
            try:
                link = item['id']
            except:
                link = ""

            try:
                bday = self.dateParse(self.fuck(item['bdate']))
            except:
                bday = ""

            try:
                sex = self.fuck(self.gender[item['sex']])
            except:
                sex = ""

            try:
                phone = self.fuck(item['mobile_phone'])
            except:
                phone = ""
            try:
                phone += self.fuck(" , " + item['home_phone'])
            except:
                pass

            if phone == " , ":
                phone = ""

            try:
                city = self.fuck(item['city']['title'])
            except:
                city = ""

            try:
                platform = self.fuck(self.pl[item['last_seen']['platform']])
            except:
                platform = ""

            note = ""

            sqlreq = """INSERT INTO 'users'
                        (source, link, name, bday, sex, phone, city, platform, note)
                        VALUES
                        ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}', '{8}')
                        """.format(g_id, link ,name, bday, sex, phone, city, platform, note)
            print("('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}', '{8}')".format(g_id, link ,name, bday, sex, phone, city, platform, note))
            self.cursor.execute(sqlreq)
            lids_count += 1
        self.db_c.commit()
        return(lids_count)

    def getGroupSubs(self, g_id):
        print("Parse : RUN")
        search_filter = "sex, bdate, city, contacts, last_seen"
        max_ofst = int(json.loads(str(self.vk.groups.getMembers(group_id=g_id)).replace("'","\""))['count'])
        cur_ofst = 0
        lids = 0
        while(max_ofst > cur_ofst):
            data = (self.vk.groups.getMembers(group_id=g_id, offset=cur_ofst, fields=search_filter))['items']
            lids += self.parsedata(data, g_id)
            cur_ofst += 1000
        print("Добавлено {0} человек".format(lids))
        self.parsingFinished.emit()

    def fuck(self, inp):
        return inp.replace("'","")

    def dateParse(self, date):
        if len(date.split('.')) == 3:
            return str(datetime.strptime(date, "%d.%m.%Y"))
        elif len(date.split('.')) == 2:
            return str(datetime.strptime(date, "%d.%m"))

