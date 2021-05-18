import time
import requests
from keys import BOT_CHATID, BOT_TOKEN


def send_telegram_message(bot_message):

    vacio = {}
    if bot_message != vacio:
        send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + \
            '/sendMessage?chat_id=' + BOT_CHATID + \
            '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()
