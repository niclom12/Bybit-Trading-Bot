from config import config_api_key, config_api_key_secret, account_type
from helper import Bybit
from logmaker import log_trade, log_start, log_error
import schedule
import time
import datetime
from pybit.unified_trading import HTTP
import numpy as np
import pandas as pd
from Hull import  Hulls, create_data_set, logic

"""
session = HTTP(api_key=config_api_key, api_secret=config_api_key_secret)
resp = session.get_wallet_balance(accountType=account_type, coin="USDT")['result']['list'][0]['coin'][0]['walletBalance']
resp = round(float(resp), 3)
print(resp)
"""

'''
bit = Bybit(config_api_key, config_api_key_secret, account_type)
resp = bit.session.get_wallet_balance(accountType="CONTRACT", coin="BTC")['result']['list'][0]['coin'][0]['equity']
print(resp)
v = bit.get_position()
print(v)
'''
"""
log_start()
log_trade("Buy", "BTCUSD", 1, 50000)
log_trade("Sell", "BTCUSD", 1, 55000)
"""
"""
bit = Bybit(config_api_key, config_api_key_secret, account_type)
price_df = bit.session.get_kline(
                    category='linear',
                    symbol="BTCUSD",
                    interval=1,
                    limit=1
                    )['result']['list']
price_df = pd.DataFrame(price_df)
price_df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover']
price = float(price_df.iloc[-1]["Open"])
log_start()
log_trade("Buy", "BTCUSD", 1, 50000)
log_trade("Sell", "BTCUSD", 1, price)
log_trade("Buy", "ETHUSD", 1, 50000)
log_trade("Buy", "DOGEUSD", 1, price)
log_trade("Sell", "DOGEUSD", 1, 50000)
log_trade("Sell", "ETHUSD", 1, price)

"""
"""
bit = Bybit(config_api_key, config_api_key_secret, account_type)
quant = str(0.001)
suc = bit.make_trade_market("Buy", "BTCUSDT", quant)
print(suc)
bit = Bybit(config_api_key, config_api_key_secret, account_type)
suc = bit.make_trade_market("Buy", "BTCUSD", "100")
print(suc)

"""
"""
balance = 124.567
quant = str(math.floor((balance * 0.5) * 1000) / 1000)
print(quant)


"""


"""
bit = Bybit(config_api_key, config_api_key_secret, account_type)
balance = bit.market_price("BTCUSD")
print(balance)
"""
"""
bit = Bybit(config_api_key, config_api_key_secret, account_type)
data = bit.get_klines("BTCUSDT", 150)
raw_hma = create_data_set(data)
smooth_hma = Hulls(raw_hma)
print(smooth_hma)

"""
"""
bit = Bybit(config_api_key, config_api_key_secret, account_type)
data = bit.get_klines("BTCUSDT", 200)
print(data[0])

for i in range(15):
    he = logic(data[i:])

"""



"""
bit = Bybit(config_api_key, config_api_key_secret, account_type)
resp = bit.session.get_kline(
                category='inverse',
                symbol="BTCUSDT",
                interval="1",
                limit=20
            )['result']['list']
resp = pd.DataFrame(resp)
resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover']
resp = resp.set_index('Time')
resp = resp.astype(float)
resp = resp['Close']

print(resp)

"""

"""
hma=[None]*6
hma[5] = smooth_hma(dat[5:], 55)
hma[4] = smooth_hma(dat[4:], 55)
hma[3] = smooth_hma(dat[3:], 55)
hma[2] = smooth_hma(dat[2:], 55)

hma[1] = smooth_hma(dat[1:], 55)
hma[0] = smooth_hma(dat, 55)
hull = logic(hma)
print(hull)

raw = []
raw[3] = create_dataset(55, data[3:])
raw[2] = create_dataset(55, data[2:])
raw[1] = create_dataset(55, data[1:])
raw[0] = create_dataset(55, data)
hma = []
hma[2] = smooth_hma(raw[2], 55)
hma[2] = smooth_hma(raw[2], 55)
hma[1] = smooth_hma(raw[1], 55)
hma[0] = smooth_hma(raw[0], 55)


#buy = logic(hma)
print(hma)
"""
"""
bit = Bybit(config_api_key, config_api_key_secret, account_type)
data = bit.get_klines("BTCUSDT", 260)
token = "BTCUSDT"
for i in range(100):
    x = 99 - i
    data = data[x:]
    try:

        side = algo(data)
        if (side == "Buy"):
            balance = bit.get_balance(token)
            balance = balance * bit.market_price(token)
            #decide how much you want to buy
            quant = str((balance * 0.5))
            #resp = bit.make_trade_market("Buy", token, quant)
            resp = 1
            if (resp == 1):
                log_trade("Buy", token, quant, price)

        elif (side == "Sell"):  
            #resp = bit.make_trade_market("Sell", token, quant)
            resp = 1
            if (resp == 1):
                price_df = bit.session.get_kline(
                category='inverse',
                symbol=token,
                interval=1,
                limit=1
                )['result']['list']
                price_df = pd.DataFrame(price_df)
                price_df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover']
                price = float(price_df.iloc[-1]["Open"])
                log_trade("Sell", token, "", price)

    except Exception as err:
        print(err)
        log_error(err)
"""






"""
balance = float(bit.get_balance(token.split("USD")[0]))
print(balance)
balance = balance * float(bit.market_price(token))
print(balance)
pos = bit.session.get_positions(
    category="inverse",
    symbol="BTCUSD",
)
print(pos)

quant = str(round(balance * 1))
print(quant)
bit.set_leverage("BTCUSD")
"""

"""
log_start()
bit = Bybit(config_api_key, config_api_key_secret, account_type)
token = "BTCUSD"
log_error("first err")
log_error("2 err")

price = str(bit.market_price(token))
log_trade("Buy", token, "200", price)
time.sleep(5)
balance = float(bit.get_balance(token.split("USD")[0]))
balance = balance * bit.market_price(token)
#decide how much you want to buy
quant = str(round(balance * 1))
price = str(bit.market_price(token))
log_trade("Buy", "ETHUSD", "200", price)

log_error("3 err")
price = str(bit.market_price(token))
log_trade("Sell", "ETHUSD", "200", price)
time.sleep(5)

log_error("4 err")

price = str(bit.market_price(token))
log_trade("Sell", token, "200", price)
"""


bit = Bybit(config_api_key, config_api_key_secret, account_type)
pos = bit.session.get_positions(
    category="inverse",
    symbol="BTCUSD",
)
balance = float(bit.get_balance("BTCUSD".split("USD")[0]))
balance = balance * bit.market_price("BTCUSD")
print(balance)
print(pos)
"""
bit = Bybit(config_api_key, config_api_key_secret, account_type)
t = bit.session.place_order(
                category="inverse",
                symbol="BTCUSD",
                side="Buy",
                orderType="Market",
                qty="24",
                isLeverage=1,
                orderFilter="Order",
                )
print(t)
"""