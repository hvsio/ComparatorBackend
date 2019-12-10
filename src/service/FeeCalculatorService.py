from interface import Interface, implements
from src.environment.enviroment import Config
from src.models.SepaCountries import SepaCountries
import sys
import urllib
from flask import request, json
import requests


class IFeeCalculatorService(Interface):

    def get_fees(self, from_country, to_country, from_currency, to_currency):
        pass


class FeeCalculatorService(implements(IFeeCalculatorService)):
    def __init__(self):
        Config.initialize()
        self.scrapper_config_url = Config.cloud('SCRAPPER_CONFIG') if (
                len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'SCRAPPER_CONFIG')
        self.midrate_api = Config.cloud('EXCHANGE_RATE_API') if (
                len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'EXCHANGE_RATE_API')

    def get_fees(self, from_country, to_country, from_currency, to_currency):
        transaction_fee_info = requests.get(self.scrapper_config_url + '/fees/' + from_country).json()
        if len(transaction_fee_info) == 0: # the case that we dont have a fee at scrapper controller
            return 0

        margin_currency = transaction_fee_info[0].get('currency', '')

        if from_currency != margin_currency:
            mid_rate = self.__get_midrate(margin_currency, from_currency)
            transaction_fee_info[0]['sepa'] = transaction_fee_info[0].get('sepa', '') * mid_rate
            transaction_fee_info[0]['intl'] = transaction_fee_info[0].get('intl', '') * mid_rate
            transaction_fee_info[0]['currency'] = to_currency

        if self.__is_sepa_payment(from_country, to_country, from_currency, to_currency):
            return transaction_fee_info[0].get('sepa', '')
        else:
            return transaction_fee_info[0].get('intl', '')

    def __get_midrate(self, from_currency, to_currency):
        url = self.midrate_api + '/latest?base='
        # json_data = self.__get_response(url + fromCurrency)
        operUrl = urllib.request.urlopen(url + from_currency)
        if operUrl.getcode() == 200:
            data = operUrl.read()
            json_data = json.loads(data)
        else:
            print("Error receiving data", operUrl.getcode())
            return 0
        try:
            exchangerate = json_data['rates'][to_currency]
        except Exception as E:
            print(E)
            return 1
        return exchangerate

    def __is_sepa_payment(self, from_country, to_country, from_currency, to_currency):
        if from_currency != to_currency != 'EUR':
            return False
        if not SepaCountries.__contains__(from_country) or not SepaCountries.__contains__(to_country):
            return False
        return True
