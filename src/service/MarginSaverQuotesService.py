import json
from src.models.bank_entry import BankEntry
from interface import implements, Interface
import requests


class IMarginSaverQuotes(Interface):
    def get_margin_saver_quotes(self, from_country, from_currency, to_currency, volume, nr_of_transactions):
        pass


class MarginSaverQuotesService(implements(IMarginSaverQuotes)):

    def get_margin_saver_quotes(self, from_country, from_currency, to_currency, volume, nr_of_transactions):
        payload = {
            'country': from_country,
            'fromCur': from_currency,
            'toCur': to_currency
        }
        # response = requests.get('http://107.178.213.12:5000/banksbuyrate', params=payload)
        response = requests.get('http://localhost:5000/banksbuyrate', params=payload)

        responses = json.loads(response.text)
        bankSuppliers = []
        fee_response = requests.get('http://35.193.212.114:8000/fees/' + from_country)
        fee_1 = fee_response.json()
        # TODO missing to check the countrys if its sepa or international payment.
        if from_currency == 'EUR' and to_currency == 'EUR':
            fee = fee_1[0].get('sepa', '')
        else:
            fee = fee_1[0].get('intl', '')

        for entry in responses:
            bank_offer = BankEntry(entry['name'], entry['exchangeratebuy'], fee, nr_of_transactions, volume,
                                   from_currency, to_currency)
            bankSuppliers.append(bank_offer)

        print(bankSuppliers)
        return bankSuppliers
