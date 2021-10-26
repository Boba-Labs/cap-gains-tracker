import batch
import ticker
import csv 
from datetime import datetime
from re import sub
from decimal import Decimal

class Profile:
    def __init__(self, brokerage):
        self.tickers = dict() 
        self.brokerage = brokerage
# CAN ONLY READ CSVs FROM CHARLES SCHWAB 
# WANT TO MAKE THIS FOR EVERY BROKERAGE/CRYPtO EXCHANGE 
def read_CSV(name, profile):
    with open(name, newline='') as csvfile:
        stockreader = csv.reader(csvfile)
        line_cunt = 0 
        for row in stockreader: 
            if line_cunt > 1 and line_cunt < 13: 
                date = datetime.strptime(row[0], '%m/%d/%Y')
                price = Decimal(sub(r'[^\d.]', '', row[5]))
                if row[2] not in profile.tickers:
                    profile.tickers[row[2]] = ticker.Ticker(row[2])
                if row[1] == "Buy":
                    profile.tickers[row[2]].add_buy(int(row[4]), price, date.year, date.month, date.day)
                elif row[1] == "Sell":
                    profile.tickers[row[2]].add_sell(int(row[4]), price, date.year, date.month, date.day)
            line_cunt += 1 
        
        profile.tickers["TSLA"].empty_sells_calculate_gains()
        print("FINAL RESULT -----------------------")
        print(profile.tickers["TSLA"].short_term_capital_gains)
        print(profile.tickers["TSLA"].long_term_capital_gains)



def main():
    profile = Profile("Schwab")
    print("Profile with brokerage " + profile.brokerage + " analyze")
    read_CSV("TSLA_TEST2.csv", profile)



if __name__ == "__main__":
    main()