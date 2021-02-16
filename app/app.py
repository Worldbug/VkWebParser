# Импорты для работы приложения
from flask import Flask, render_template, send_from_directory, request, Markup, redirect
import os
import base64
from datetime import datetime
# Либа для парсинга
import VkParser
# Ну да, Qt, и что ты мне сделаешь
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread

# Настройки
LOG_STATE       = False
NGROK_STATE     = False

# Запуск приложения
app = Flask(__name__, static_folder=str(STATIC_DIR))
checkLaunch()

# Проверка логирования и нгрока
def checkLaunch():
    # Нгрок (Веб-прокся с доменрм)
    if NGROK_STATE:
        from pyngrok import ngrok
        http_tunel = ngrok.connect(5000)
        print(ngrok.get_tunnels())

    # Лог
    if LOG_STATE:
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

# Обработчик парсера
@app.route('/parse', methods=['POST'])
def launchParse():
    # Потом может быть переделать на restapi
    if request._method == 'POST':
        # Собираем данные
        user_id = request.form["uid"]
        group_id = request.form["gid"]
        # Проверяем токен для UID
            # Я верю на слово
        # Токен есть, идем собирать
        parser = VkParser.VkParser(group_id) # Добавить проверку валидности
        parserThread = QThread(parent=self)  # Возможно тут будет ГГ
        parserThread.started.connect(self.parser.onStart)
        parser.moveToThread(self.parserThread)
        parserThread.start()
        # Ну собсна все
    else:
        return("Соси хуй, меня надо пинать POST`ом")

# Ланчуем рататата
if __name__ == '__main__':
    app.run()

