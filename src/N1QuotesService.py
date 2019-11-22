from src.IN1Quotes import IN1Quotes
from interface import implements
from src.bank_entry import BankEntry
import requests


class N1QuotesService(implements(IN1Quotes)):

    def get_quote(self, from_country_code, to_country_code, from_currency_code, to_currency_code, amount):
        payload = {'fromCountryCode': from_country_code,
                   'toCountryCode': to_country_code,
                   'fromCurrencyCode': from_currency_code,
                   'toCurrencyCode': to_currency_code,
                   'amount': amount,
                   'feeType': 'Shared',
                   'side': 'Buy',
                   'paymentType': 'Spot'}
        response = requests.get('https://api.novemberfirst.com/v1/quote', params=payload)
        return BankEntry()
