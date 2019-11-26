import json
import sys

from src.models.bank_entry import BankEntry
from interface import implements, Interface
from src.environment.enviroment import Config
from src.models.SepaCountries import SepaCountries
from src.service.ScrapperControllerConnection import ScrapperConfigConnection

import requests


class IMarginSaverQuotes(Interface):
    def get_margin_saver_quotes(self,
                                from_country,
                                from_currency,
                                to_country,
                                to_currency,
                                volume,
                                nr_of_transactions):
        pass


class MarginSaverQuotesService(implements(IMarginSaverQuotes)):

    def __init__(self, scrapper_controller_connection=ScrapperConfigConnection()):
        Config.initialize()

        self.margin_service_url = Config.cloud('MARGIN_SAVER') if (
                len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'MARGIN_SAVER')

        self.scrapper_config_connection = scrapper_controller_connection

    def get_margin_saver_quotes(self,
                                from_country,
                                from_currency,
                                to_country,
                                to_currency,
                                volume,
                                nr_of_transactions):
        payload = {
            'country': from_country,
            'fromCurrency': from_currency,
            'toCurrency': to_currency
        }
        response = requests.get(self.margin_service_url + '/banksbuyrate', params=payload)

        responses = json.loads(response.text)
        bankSuppliers = []

        transaction_fee_info = self.scrapper_config_connection.get_fees(from_country)

        if not len(transaction_fee_info) == 0:
            if self.is_sepa_payment(from_country,
                                    to_country,
                                    from_currency,
                                    to_currency):
                transaction_fee = transaction_fee_info[0].get('sepa', '')
            else:
                transaction_fee = transaction_fee_info[0].get('intl', '')
        else:  # in case that the bank fee is not added in scrapper config service.
            transaction_fee = 0

        for entry in responses:
            bank_offer = BankEntry(entry['name'],
                                   entry['exchangeratebuy'],
                                   transaction_fee,
                                   nr_of_transactions,
                                   volume,
                                   from_currency,
                                   to_currency)
            bankSuppliers.append(bank_offer)

        return bankSuppliers

    def is_sepa_payment(self, from_country, to_country, from_currency, to_currency):
        if from_currency != to_currency != 'EUR':
            return False
        if not SepaCountries.__contains__(from_country) or not SepaCountries.__contains__(to_country):
            return False
        return True
