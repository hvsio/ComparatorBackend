from interface import Interface, implements
from src.environment.enviroment import Config
import sys
import urllib
from flask import request, json
import requests


class IFeeCalculatorService(Interface):

    def get_fees(self, country, currency):
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

    def get_fees(self, country, currency):
        fees_response = requests.get(self.scrapper_config_url + '/fees/' + country).json()
        margin_currency = fees_response[0].get('currency', '')
        if currency != margin_currency:
            mid_rate = self.__get_midrate(margin_currency, currency)
            fees_response[0]['sepa'] = fees_response[0].get('sepa', '') * mid_rate
            fees_response[0]['intl'] = fees_response[0].get('intl', '') * mid_rate
            fees_response[0]['currency'] = currency

        return fees_response

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
