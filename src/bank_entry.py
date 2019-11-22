import json


class BankEntry:
    def __init__(self, name, exchange_rate, fee_single_transaction, nr_transactions, volume):
        self.name = name
        self.exchangeRate = exchange_rate
        self.totalFee = fee_single_transaction * nr_transactions
        self.totalCost = BankEntry.calculate_total_cost(self.totalFee, volume, exchange_rate)

    # def __init__(self, ):

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)

    @staticmethod
    def calculate_total_cost(total_fee, volume, exchange_rate):
        return volume / exchange_rate + total_fee