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

    def available_currencies(self, country_iso):
        pass


class N1QuotesService(implements(IN1QuotesService)):
    def __init__(self):
        Config.initialize()
        self.n1_api_url = Config.cloud('N1API') if (
                len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'N1API')

    # TODO we assume that the company is registered in Denmark for N1 quotes. We can not get quotes for Norwegian
    #  swedish, UK ... companies
    def get_quote(self, from_country_code, to_country_code, from_currency_code, to_currency_code, amount,
                  nr_transactions):
        payload = {'fromCountryCode': 'DK',
                   'toCountryCode': to_country_code,
                   'fromCurrencyCode': from_currency_code,
                   'toCurrencyCode': to_currency_code,
                   'amount': amount,
                   'feeType': 'Shared',
                   'side': 'Buy',
                   'paymentType': 'Spot'}
        response = requests.get(self.n1_api_url + '/quote', params=payload)
        # 503 code if N1 API is out of service (weekends, and from 11PM - 5AM)
        # 400 if from_currency_code == to_currency_code
        if response.status_code == 503 or response.status_code == 400:
            return []
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
                response='N1 service not available',
                status=200)

    def available_currencies(self, country_iso):
        # TODO we assume that the company is registered in Denmark for N1 quotes. We can not get quotes for Norwegian
        #  swedish, UK ... companies
        payload = {'countryCode': 'DK'}
        response = requests.get(self.n1_api_url + '/allowedCurrencies', params=payload)
        if response.status_code == 200:
            return Response(
                response=json.dumps(response.json()),
                status=200,
                mimetype='application/json')
        elif response.status_code == 400:
            return Response(
                response='wrong country iso or country not supported',
                status=400,
            )
        else:
            return Response(
                response='N1 service not available',
                status=503,
            )
