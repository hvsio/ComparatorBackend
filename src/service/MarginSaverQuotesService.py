import json
import sys

from src.models.bank_entry import BankEntry
from interface import implements, Interface
from src.environment.enviroment import Config
from src.models.SepaCountries import SepaCountries
import requests


class IMarginSaverQuotes(Interface):
    def get_margin_saver_quotes(self, from_country, from_currency, to_country, to_currency, volume, nr_of_transactions):
        pass

    def is_sepa_payment(self, from_country, to_country, from_currency, to_currency):
        pass


class MarginSaverQuotesService(implements(IMarginSaverQuotes)):

    def __init__(self):
        Config.initialize()
        self.margin_service_url = Config.cloud('MARGIN_SAVER') if (
                len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'MARGIN_SAVER')
        self.scrapper_config_url = Config.cloud('SCRAPPER_CONFIG') if (
                len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'SCRAPPER_CONFIG')

    def get_margin_saver_quotes(self, from_country, from_currency, to_country, to_currency, volume, nr_of_transactions):
        payload = {
            'country': from_country,
            'fromCur': from_currency,
            'toCur': to_currency
        }
        response = requests.get(self.margin_service_url + '/banksbuyrate', params=payload)

        responses = json.loads(response.text)
        bankSuppliers = []
        fee_response = requests.get(self.scrapper_config_url + '/fees/' + from_country)
        fee_1 = fee_response.json()

        if not len(fee_1) == 0:
            if self.is_sepa_payment(from_country, to_country, from_currency.to_currency):
                fee = fee_1[0].get('sepa', '')
            else:
                fee = fee_1[0].get('intl', '')
        else:  # in case that the bank fee is not added in scrapper config service.
            fee = 0

        for entry in responses:
            bank_offer = BankEntry(entry['name'], entry['exchangeratebuy'], fee, nr_of_transactions, volume,
                                   from_currency, to_currency)
            bankSuppliers.append(bank_offer)

        return bankSuppliers

    def is_sepa_payment(self, from_country, to_country, from_currency, to_currency):
        if from_currency != to_currency != 'EUR':
            return False
        if not SepaCountries.__contains__(from_country) or not SepaCountries.__contains__(to_country):
            return False
        return True
