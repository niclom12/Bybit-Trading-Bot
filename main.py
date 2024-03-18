from config import config_api_key, config_api_key_secret, account_type
from helper import Bybit
from logmaker import log_trade, log_start, log_error
import schedule
import time
from Hull import logic
import datetime


list = ["BTCUSD"]
def connect_server(config_api_key, config_api_key_secret, acount_type):
    bit = Bybit(config_api_key, config_api_key_secret, account_type)
    return bit

def algo(data):
    return logic(data)

def run_algo():
    bit = connect_server(config_api_key, config_api_key_secret, account_type)
    for token in list:
        try:
            data = bit.get_klines(token, 120)
            side = algo(data)
            if (side == "Buy"):
                balance = float(bit.get_balance(token.split("USD")[0]))
                balance = balance * bit.market_price(token)
                #decide how much you want to buy
                quant = str(round(balance * 1))
                #bit.set_leverage(token)
                resp = bit.make_trade_market("Buy", token, quant)
                print(resp)
                if (resp == 0):
                    price = str(bit.market_price(token))
                    log_trade("Buy", token, quant, price)

            elif (side == "Sell"):  
                #bit.set_leverage(token)
                resp = bit.make_trade_market("Sell", token, "0")
                print(resp)
                if (resp == 0):
                    price = str(bit.market_price(token))
                    log_trade("Sell", token, "", price)

        except Exception as err:
            print(type(err))
            print(err)
            log_error(err)


def run_job_at_next_minute():
    current_time = datetime.datetime.now()
    delay = 60 - current_time.second + 2
    time.sleep(delay)
    run_algo()  # run job immediately after sleep

log_start()
while True:
    run_job_at_next_minute()
"""
schedule.every().day.at("00:01").do(run_algo)
schedule.every().day.at("04:01").do(run_algo)
schedule.every().day.at("08:01").do(run_algo)
schedule.every().day.at("12:01").do(run_algo)
schedule.every().day.at("20:01").do(run_algo)

while True:
    schedule.run_pending()
    time.sleep(1)
"""




    

