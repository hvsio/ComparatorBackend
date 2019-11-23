from interface import Interface, implements
from flask import Response, json
from src.models.bank_entry import BankEntrySchema


class IBankSupplierService(Interface):

    def get_supplier(self, from_country, to_country, from_currency, to_currency, volume, nr_transactions):
        pass


class BankSupplierService(implements(IBankSupplierService)):
    def __init__(self, margin_saver_quote_service, n1_quote_service):
        self.__MarginSaverQuoteService = margin_saver_quote_service
        self.__N1QuoteService = n1_quote_service

    def get_supplier(self, from_country, to_country, from_currency, to_currency, volume, nr_transactions):
        # TODO call asynchronous n1_suppliers and bank_supplier
        bankSuppliers = self.__N1QuoteService.get_quote(from_country, to_country, to_currency, from_currency, volume)
        bankSuppliers.extend(self.__MarginSaverQuoteService.get_margin_saver_quotes(from_country, from_currency,
                                                                                    to_currency, volume,
                                                                                    nr_transactions))
        schema = BankEntrySchema(many=True)

        return Response(
            response=schema.dumps(bankSuppliers, indent=2),
            status=200,
            mimetype='application/json')
