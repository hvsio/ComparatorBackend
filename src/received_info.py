class ReceivedInfo:
    def __init__(self, from_country, to_country, from_currency, to_currency, amount, frequency, *args, **kwargs):
        self.fromCountry = from_country
        self.toCountry = to_country
        self.fromCurrency = from_currency
        self.toCurrency = to_currency
        self.amount = amount
        self.frequency = frequency
