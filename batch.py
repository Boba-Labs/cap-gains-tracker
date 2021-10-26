from datetime import date
class Batch:
    def __init__(self, quantity, price, date, action):
        self.quantity = quantity
        self.date = date
        self.price = price
        self.action = action # 0 for buy, 1 for sell, 2 for call, 3 for put 


