import json
import requests
import urllib
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

TOKEN = ''
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
COINMARKETCAP_URL = "https://api.coinmarketcap.com/v1/"
COIN = "boscoin/"
COMMANDS = ['/price', '/wallet', '/notice', '/forum', '/donation']


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def send_message(text, chat_id, reply_markup=None):
    # text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
        return max(update_ids)


# def echo_all(updates):
#     for update in updates["result"]:
#         try:
#             text = update["message"]["text"]
#             chat = update["message"]["chat"]["id"]
#             send_message(text, chat)
#         except Exception as e:
#             print(e)
def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            coin = COIN
            msg = None
            if text == '/start':
                # start greeting message
                pass
            elif text == '/help':
                keyboard = build_keyboard()
                print(keyboard)
                print("entered")
                send_message("help is here!", chat_id=chat, reply_markup=keyboard)
                print("sent message")
            elif text == '/price':
                msg = get_price(coin)
            elif text == '/wallet':
                msg = "Check the BOScoin wallet website for more information \nhttps://wallet.boscoin.io/"
            elif text == '/notice':
                # get_notice()
                pass
            elif text == '/forum':
                msg = "Check BOScoin's latest newsletters in the forum \nhttps://medium.com/@boscoin"
            elif text == '/donation':
                msg = "Donations can be made to the developer's BOScoin public address: Gdwadwadaw"
            else:
                msg = "https://medium.com/@boscoin/latest"

            # send_message(msg, chat)

        except Exception as e:
            print("error")
            print(e)


def build_keyboard():
    # keyboard = [{"text": "wallet", "url": "https://wallet.boscoin.io/"}]
    button_list = [
        InlineKeyboardButton("col1", callback_data="dwad"),
        InlineKeyboardButton("col2", callback_data="dawdaw"),
        InlineKeyboardButton("row 2", callback_data="dadw")
    ]
    # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    # custom_keyboard = [{"text":"1", "url": 'top-left', 'top-right'], ['bottom-left', 'bottom-right']]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def get_price(coin):
    url = COINMARKETCAP_URL + "ticker/" + coin
    coin_info = get_json_from_url(url)
    coin = coin_info[0]
    coin_id = coin['id']
    name = coin['name']
    symbol = coin['symbol']
    rank = coin['rank']
    price_usd = coin['price_usd']
    price_btc = coin['price_btc']
    price_eth = "ethereum_not_implemented"
    pc_1h = coin['percent_change_1h']
    pc_24h = coin['percent_change_24h']
    pc_7d = coin['percent_change_7d']
    output_str = "{} ({}) \nRank: {}\n\nPrice: \n    USD: ${}\n    BTC: B{}\n\nChange:\n     1h: {}%\n   24h: " \
                 "{}%\n     7d: {}%".format(name, symbol, rank, price_usd, price_btc, pc_1h, pc_24h, pc_7d)
    return output_str


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)


if __name__ == '__main__':
    main()
