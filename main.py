from helper import Bybit
from logmaker import log_trade, log_start, log_error
import schedule
import pandas as pd
import time
from Hull import logic
import datetime
import requests
import pybit.exceptions as pybit_exceptions



tokens = ["BTCUSD", "SOLUSD", "ETHUSD"]
memory = {"BTCUSD": 0, "ETHUSD": 0, "SOLUSD": 0}
open = {"BTCUSD": -1.0, "ETHUSD": -1.0, "SOLUSD": -1.0}


def connect(config_api_key, config_api_key_secret):
    bit = Bybit(config_api_key, config_api_key_secret, "CONTRACY")
    return bit

def algo(data):
    return logic(data)

def run_algo():
    time.sleep(1)
    print("...................................................................")
    client_info = pd.read_excel('Users.xlsx')
    first_row = client_info.iloc[0]
    bit = connect(str(first_row['api']), str(first_row['private']))
    for token in tokens:
        try:
            data = bit.get_klines(token, 120)
            side, hull = algo(data[1:])
            if (side == "Buy"):
                print(token)
                open[token] = data[0]
                for index, row in client_info.iterrows():
                    try:
                        client = connect(row.api, row.private)
                        quant = str(client.get_buy_amount(token, hull, memory[token], data[0]))
                        #bit.set_leverage(token)
                        resp = client.make_trade_market("Buy", token, quant)
                        print(resp)
                        positions = row.positions.split(",")
                        for i, position in enumerate(positions):
                            if token in position:
                                positions[i] = token + str(quant)
                        client_info.loc[index, 'positions'] = ",".join(positions)
                        
                    except pybit_exceptions.FailedRequestError as e:
                        log_error(str(e) + ": " + row.Users) 
                
                    except pybit_exceptions.InvalidRequestError as e:
                        log_error(str(e) + ": " + row.Users) 
 
                    except Exception as e:
                        log_error(str(e) + ": " + row.Users)
                        
            elif (side == "Sell"):  
                print(token)
                closing_price = data[0]
                if (open[token] >= 0 and float(closing_price - open[token]) < 0):
                    memory[token] = int(memory[token]) + 1
                else:
                    memory[token] = 0
                for index, row in client_info.iterrows():
                    try:
                        client = connect(row.api, row.private)
                        positions = row.positions.split(",")
                        for i, position in enumerate(positions):
                            if token in position:
                                parts = position.split(token)
                                quant = str(parts[-1])  # get the last part after splitting
                                resp = bit.make_trade_market("Sell", token, quant)
                                positions[i] = token + '0'
                        client_info.loc[index, 'positions'] = ",".join(positions)
                        
                    except pybit_exceptions.FailedRequestError as e:
                        log_error(str(e) + ": " + row.Users) 
                
                    except pybit_exceptions.InvalidRequestError as e:
                        log_error(str(e) + ": " + row.Users) 
 
                    except Exception as e:
                        log_error(str(e) + ": " + row.Users) 
                        
                    
        except (requests.ConnectionError, requests.Timeout) as e:
            log_error(e)
       
        except Exception as err:
            log_error(err)
    
    client_info.to_excel('Users.xlsx', index=False)
    print(memory)
    print(open)


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




    

