import sys

from interface import implements
from src.models.bank_entry import BankEntry
from flask import Response, json
from src.environment.enviroment import Config
from interface import Interface
import requests


class IN1QuotesService(Interface):
    def get_quote(self, from_country_code, to_country_code, from_currency_code, to_currency_code, amount,
                  nr_transactions):
        pass

    def are_quotes_available(self):
        pass


class N1QuotesService(implements(IN1QuotesService)):
    def __init__(self):
        Config.initialize()
        self.n1_api_url = Config.cloud('N1API') if (
                len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'N1API')

    def get_quote(self, from_country_code, to_country_code, from_currency_code, to_currency_code, amount,
                  nr_transactions):
        payload = {'fromCountryCode': from_country_code,
                   'toCountryCode': to_country_code,
                   'fromCurrencyCode': from_currency_code,
                   'toCurrencyCode': to_currency_code,
                   'amount': amount,
                   'feeType': 'Shared',
                   'side': 'Buy',
                   'paymentType': 'Spot'}
        response = requests.get(self.n1_api_url + '/quote', params=payload)
        if response.status_code == 503:
            return []
        # TODO create the bankentry with the response.
        n1_quote = response.json()
        return BankEntry('November First', n1_quote['ExchangeRate'], n1_quote['FeeAmount'], nr_transactions, amount,
                  from_currency_code, to_country_code)

    def are_quotes_available(self):
        payload = {'fromCountryCode': 'DK',
                   'toCountryCode': 'DE',
                   'fromCurrencyCode': 'DKK',
                   'toCurrencyCode': 'EUR',
                   'amount': '100',
                   'feeType': 'Shared',
                   'side': 'Buy',
                   'paymentType': 'Spot'}
        response = requests.get(self.n1_api_url + '/quote', params=payload)

        if response.status_code == 200:
            return Response(
                response='ok',
                status=200)
        else:
            return Response(
                response='service not available',
                status=200)
