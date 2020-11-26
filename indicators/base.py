
class Indicator:
    
    def get_buy_signals(self):
        raise NotImplementedError

    def get_sell_signals(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
