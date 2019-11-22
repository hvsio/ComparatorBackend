import json
from src.bank_entry import BankEntry
from interface import implements, Interface
import requests


class IMSQuotes(Interface):
    def get_ms_result(self, country, from_currency, to_currency, nr_of_transactions, volume):
        pass


class MSQuotesService(implements(IMSQuotes)):

    def get_ms_result(self, country, from_currency, to_currency, nr_of_transactions, volume):
        payload = {
            'country': country,
            'fromCur': from_currency,
            'toCur': to_currency
        }
        response = requests.get('http://107.178.213.12:5000/banksbuyrate', params=payload)
        responses = json.loads(response.text)
        list = []
        # TODO get fees from scrapper controller
        fee_response = requests.get('http://35.193.212.114:8000/fees/' + country)
        fee_1 = fee_response.json()

        if from_currency == 'EUR' and to_currency == 'EUR':
            fee = fee_1[0].get('sepa', '')
        else:
            fee = fee_1[0].get('intl', '')

        for entry in responses:

            bank_offer = BankEntry(entry['name'], entry['exchangeratebuy'], int(fee), nr_of_transactions, volume)
            list.append(bank_offer)

        print(list)
        return list
