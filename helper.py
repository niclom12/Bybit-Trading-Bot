from pybit.unified_trading import HTTP
import pandas as pd
from logmaker import log_error, log_response



class Bybit:

    def __init__(self, api, secret, accounttype):
        self.api = api
        self.secret = secret
        self.accountType = accounttype
        try:
            self.session = HTTP(api_key=self.api, api_secret=self.secret)
        except Exception as err:
            print("failed to connect")
            log_error(err)
           
    def get_klines(self, symbol, size):
        try:
            resp = self.session.get_kline(
                #change to inverse
                category='inverse',
                symbol=symbol,
                interval="1",
                limit=size
            )['result']['list']
            resp = pd.DataFrame(resp)
            resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover']
            resp = resp.set_index('Time')
            resp = resp.astype(float)
            resp = resp['Close']
            return resp.values
        except Exception as err:
            log_error(err)

    def get_balance(self, type):
        try:
            resp = self.session.get_wallet_balance(accountType="CONTRACT", coin=type)['result']['list'][0]['coin'][0]['equity']
            resp = round(float(resp), 8)
            return resp
        except Exception as err:
            log_error(err)


    def get_position(self):
        try:
            resp = self.session.get_positions(category='inverse')['result']['list']
            pos = []
            for elem in resp:
                pos.append([elem['symbol'], elem['size']])
            return pos
        except Exception as err:
            log_error(err)

    #Quant has to be in the base coin amount...But not for inverse only for linear.
    def make_trade_market(self, side, symbol, quant):
        try:
            resp = 1
            if (side == 'Buy'):
                resp = self.session.place_order(
                category="inverse",
                symbol=symbol,
                side=side,
                orderType="Market",
                qty=quant,
                isLeverage=1,
                orderFilter="Order"
                )['retCode'] # type: ignore
            elif(side == "Sell"):
                quant = quant
                resp = self.session.place_order(
                category="inverse",
                symbol=symbol,
                side="Sell",
                orderType="Market",
                qty=quant,
                isLeverage=1,
                orderFilter="Order",
                #reduceOnly="true"
                )['retCode'] # type: ignore
            return int(resp)
        except Exception as err:
            log_error(err)
            return 1

    def market_price(self, symbol):
        try:
            resp = self.session.get_kline(
                category='inverse',
                symbol=symbol,
                interval="1",
                limit=1
            )['result']['list']
            return float(resp[0][4])  
        except Exception as err:
            log_error(err)  

    def set_leverage(self, token):
        try:
            self.session.set_leverage(
            category="inverse",
            symbol=token,
            buyLeverage="10",
            sellLeverage="10",
            )
        except Exception as err:
            log_error(err)
            
    def get_buy_amount(self, symbol, hull, mem, closing_price):
        try:
            coin_balance = float(self.get_balance(symbol.split("USD")[0]))
            b3 = abs(((closing_price - hull) / closing_price) * 100)
            amount = (closing_price * coin_balance)
            memory_lev = 9 - int(mem)
            lev = (100 / (memory_lev * (b3 * 0.9206 + 1.4126)))
            if (lev >= 10):
                lev = 10
            amount = round(amount * lev)
            return amount
        except Exception as e:
            log_error(e)