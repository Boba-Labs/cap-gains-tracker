import queue
from batch import Batch
import datetime

class Ticker:
    def __init__(self, symbol):
        self.symbol = symbol
        self.buys = queue.Queue()
        self.sells = queue.Queue()
        self.long_term_capital_gains = 0.0
        self.short_term_capital_gains = dict() 
        self.last_updated = datetime.datetime.now()
    
    def add_buy(self, num_shares, price, year, month, day):
        self.buys.put(Batch(num_shares, price, datetime.datetime(year,month,day),0))

    def add_sell(self, num_shares, price, year, month, day):
        self.sells.put(Batch(num_shares, price, datetime.datetime(year,month,day),1))

    def compare_buy_sell(self, buy, sell): 
        print("BUY P Q", buy.price, buy.quantity)
        print("SELL P Q", sell.price, sell.quantity)
        prev_sell = None
        prev_buy = None
        if (sell.quantity == buy.quantity):
            gain_loss = float(sell.quantity*sell.price - sell.quantity*buy.price)
        elif (sell.quantity > buy.quantity):
            gain_loss = float(buy.quantity*sell.price - buy.quantity*buy.price)
            sell.quantity -= buy.quantity 
            prev_sell = sell
        else:
            gain_loss = float(sell.quantity*sell.price - sell.quantity*buy.price)
            buy.quantity -= sell.quantity
            prev_buy = buy
        time_diff = sell.date-buy.date
        years = self.__get_years(time_diff)[0]
        if (years < 1): # short term capital gains
            quarter = self.__month_to_quarter(sell.date.month)
            curr_yr_qtr = sell.date.year * 10 + quarter 
            if (curr_yr_qtr in self.short_term_capital_gains):
                self.short_term_capital_gains[curr_yr_qtr] += gain_loss
            else:
                self.short_term_capital_gains[curr_yr_qtr] = gain_loss
        else:
            self.long_term_capital_gains += gain_loss

        return prev_buy, prev_sell

    def empty_sells_calculate_gains(self):
        prev_buy = None
        prev_sell = None
        while(self.sells.empty() == False):
            if (prev_buy):
                curr_sell = self.sells.get_nowait()
                prev_buy, prev_sell = self.compare_buy_sell(prev_buy, curr_sell)
            elif (prev_sell):
                curr_buy = self.buys.get_nowait()
                prev_buy, prev_sell = self.compare_buy_sell(curr_buy, prev_sell)
            else: 
                curr_sell = self.sells.get_nowait()     
                curr_buy = self.buys.get_nowait()              
                prev_buy, prev_sell = self.compare_buy_sell(curr_buy, curr_sell)

    def __get_years(self, timedelta):
        timedelta_seconds = timedelta.total_seconds()
        return divmod(timedelta_seconds, 31536000)

    def __month_to_quarter(self, month): 
        return int((month-1)/4) + 1