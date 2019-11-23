from interface import implements
from src.models.bank_entry import BankEntry
from flask import Response, json
from interface import Interface
import requests


class IN1Quotes(Interface):
    def get_quote(self, from_country_code, to_country_code, from_currency_code, to_currency_code, amount):
        pass


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
        if response.status_code == 503:
            return []
        # TODO create the bankentry with the response.
        return BankEntry()

    def areQuotesAvailable(self):
        payload = {'fromCountryCode': 'DK',
                   'toCountryCode': 'DE',
                   'fromCurrencyCode': 'DKK',
                   'toCurrencyCode': 'EUR',
                   'amount': '100',
                   'feeType': 'Shared',
                   'side': 'Buy',
                   'paymentType': 'Spot'}
        response = requests.get('https://api.novemberfirst.com/v1/quote', params=payload)

        if response.status_code == 200:
            return Response(
                response='ok',
                status=200)
        else:
            return Response(
                response='service not available',
                status=200)
