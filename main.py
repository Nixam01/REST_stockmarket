import requests
import json

authHeader = {'Authorization': 'Basic hash'}


def check_account(auth):
    client_data = requests.get("https://zsutstockserver.azurewebsites.net/api/client", headers=authHeader)
    return client_data.json()


def buy_shares(auth, stock, share, amount):
    get_price = requests.get("https://zsutstockserver.azurewebsites.net/api/shareprice/%s?share=%s" % (stock, share))
    buy_price = get_price.json()[0]["price"]
    print("Buying shares of ", share, "Price: ", buy_price)
    body = {"stockExchange": stock, "share": share, "amount": amount, "price": buy_price+1}
    requests.post("https://zsutstockserver.azurewebsites.net/api/buyoffer", json=body, headers=auth)


def sell_shares(auth, stock, share, amount):
    get_price = requests.get("https://zsutstockserver.azurewebsites.net/api/shareprice/%s?share=%s" % (stock, share))
    sell_price = get_price.json()[1]["price"]
    print("Selling shares of ", share, "Price: ", sell_price)
    body = {"stockExchange": stock, "share": share, "amount": amount, "price": sell_price-1}
    requests.post("https://zsutstockserver.azurewebsites.net/api/selloffer", json=body, headers=auth)


def buy_from_stock(auth, stock):
    get_stock_shares = requests.get("https://zsutstockserver.azurewebsites.net/api/shareslist/%s" % stock).json()
    for share in get_stock_shares:
        share_length = len(share)
        if share in check_account(auth)["shares"]:
            current_share_amount = int(check_account(auth)["shares"][share])
        else:
            current_share_amount = 0
        if share_length > current_share_amount:
            buy_shares(auth, stock, share, share_length-current_share_amount)
        if share_length < current_share_amount:
            sell_shares(auth, stock, share, current_share_amount-share_length)


def save_history():
    data = requests.get("https://zsutstockserver.azurewebsites.net/api/history", headers=authHeader)
    with open('history1.json', 'w') as f:
        json.dump(data.json(), f)


def zadanie3_2(auth):
    for i in range(1, 13):
        buy_shares(auth, "KGHM", 1)
        buy_shares(auth, "BOGDANKA", 1)
        buy_shares(auth, "LOTOS", 1)
        buy_shares(auth, "GRODNO", 1)


def zadanie3_3(auth):
    buy_from_stock(auth, "Praga")
    buy_from_stock(auth, "Warszawa")
    buy_from_stock(auth, "Londyn")
    buy_from_stock(auth, "Wieden")


print("Client GET response: ", check_account(authHeader))

#buy_shares(authHeader, "KGHM", 1)
#zadanie3_2(authHeader)
#zadanie3_3(authHeader)


print("Client GET response: ", check_account(authHeader))

save_history()
