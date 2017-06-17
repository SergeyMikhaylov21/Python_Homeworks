# -*- coding: utf-8 -*-
from pymystem3 import Mystem
import json, re, tkn, telebot, flask

WEBHOOK_URL_BASE = "https://{}:{}".format(tkn.WEBHOOK_HOST, tkn.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(tkn.TOKEN)

regexp = '"gr":.+?], '
m = Mystem()

bot = telebot.TeleBot(tkn.TOKEN, threaded=False)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Приветствую! Меня зовут Бот. Граммар Бот. Мое предназначение - разбирать слова в предложениях на русском языке. Напишите мне любое предложение!")

@bot.message_handler(func=lambda m: True)
def text_analysis(message):
    text = str(message.text)
    anres = json.dumps(m.analyze(text), ensure_ascii=False, sort_keys=True)
    grinfo = re.findall(regexp, anres)
    bot.send_message(message.chat.id, 'А вот и разбор слов в Вашем предложении:')
    for word in grinfo:
        word = word.replace('}],', '')
        bot.send_message(message.chat.id, word)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
