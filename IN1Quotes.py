from interface import Interface


class IN1Quotes(Interface):
    def get_quote(self, from_country_code, to_country_code, from_currency_code, to_currency_code, amount):
        pass
