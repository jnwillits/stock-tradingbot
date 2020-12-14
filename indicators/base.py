from pandas import DataFrame


class Indicator:

    def __init__(self, data: DataFrame):
        self.data = data

    def plot(self):
        raise NotImplementedError

    def calculate(self):
        raise NotImplementedError

