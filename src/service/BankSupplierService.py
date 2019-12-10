from interface import Interface, implements
from flask import Response, json
from src.models.SepaCountries import SepaCountries
from src.models.bank_entry import BankEntrySchema
from src.service.MarginsQuotesService import MarginSaverQuotesService
from src.service.N1QuotesService import N1QuotesService


class IBankSupplierService(Interface):

    def get_supplier(self, from_country, to_country, from_currency, to_currency, volume, nr_transactions):
        pass

    def are_quotes_available(self):
        pass

    def allowed_currencies(self, country_iso):
        pass


class BankSupplierService(implements(IBankSupplierService)):
    def __init__(self, margin_saver_quote_service=MarginSaverQuotesService(), n1_quote_service=N1QuotesService()):
        self.__MarginSaverQuoteService = margin_saver_quote_service
        self.__N1QuoteService = n1_quote_service

    def get_supplier(self, from_country, to_country, from_currency, to_currency, volume, nr_transactions):
        bankSuppliers = [self.__N1QuoteService.get_quote(from_country,
                                                         to_country,
                                                         from_currency,
                                                         to_currency,
                                                         volume,
                                                         nr_transactions)]

        # if N1 can not get quote we dont search for other banks.
        if not bankSuppliers[0]:
            return Response(
                response=json.dumps({'status': 'service not available'}),
                status=503,
                mimetype='application/json')

        bankSuppliers.extend(self.__MarginSaverQuoteService.get_margin_saver_quotes(from_country,
                                                                                    from_currency,
                                                                                    to_country,
                                                                                    to_currency,
                                                                                    volume,
                                                                                    nr_transactions))
        schema = BankEntrySchema(many=True)

        return Response(
            response=schema.dumps(bankSuppliers, indent=2),
            status=200,
            mimetype='application/json')

    def are_quotes_available(self):
        return self.__N1QuoteService.are_quotes_available()

    def allowed_currencies(self, country_iso):
        response = self.__N1QuoteService.available_currencies(country_iso)
        return response
