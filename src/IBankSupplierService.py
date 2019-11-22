import json

from interface import Interface, implements
from src.bank_entry import BankEntry


class IBankSupplierService(Interface):

    def get_supplier(self, to_country, from_country, to_currency, from_currency, amount, frequency):
        pass


class BankSupplierService(implements(IBankSupplierService)):
    def __init__(self, ms_quote_service, n1_quote_service):
        self.MSQuoteService = ms_quote_service
        self.N1QuoteService = n1_quote_service

    def get_n1_supplier(self, to_country, from_country, to_currency, from_currency, amount, frequency):
        response = self.N1QuoteService.get_quote(to_country, from_country, to_currency, from_currency, amount,
                                                 frequency)

    def get_bank_supplier(self, country, from_currency, to_currency):
        response = self.MSQuoteService.get_ms_result(country, from_currency, to_currency)

