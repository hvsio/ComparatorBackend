import json
from marshmallow import Schema, fields


class BankEntrySchema(Schema):
    name = fields.Str()
    exchangeRate = fields.Str()
    toCurrency = fields.Str()
    volume = fields.Float()
    fromCurrency = fields.Str()
    totalFee = fields.Float()
    totalCost = fields.Float()


class BankEntry:

    def __init__(self, name, exchange_rate, fee_single_transaction, nr_transactions, volume, from_currency,
                 to_currency):
        self.name = name
        self.exchangeRate = exchange_rate
        self.toCurrency = to_currency
        self.volume = volume
        self.fromCurrency = from_currency
        self.totalFee = fee_single_transaction * nr_transactions
        self.totalCost = BankEntry.calculate_total_cost(self.totalFee, volume, exchange_rate)

    #def to_JSON(self):
    #    string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
    #    return json.loads(string)

    @staticmethod
    def calculate_total_cost(total_fee, volume, exchange_rate):
        return volume / exchange_rate + total_fee
