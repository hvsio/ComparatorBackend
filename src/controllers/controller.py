from flask import Flask, request, json
from src.service.BankSupplierService import BankSupplierService
from src.service.MarginSaverQuotesService import MarginSaverQuotesService
from src.service.N1QuotesService import N1QuotesService

app = Flask(__name__)

n1QuotesService = N1QuotesService()
bankSupplierService = BankSupplierService(MarginSaverQuotesService(), n1QuotesService)


@app.route('/banksuppliers', methods=['GET'])
def get_data_fe():
    response = bankSupplierService.get_supplier(request.values.get('fromCountry'),
                                                request.values.get('toCountry'),
                                                request.values.get('fromCurrency'),
                                                request.values.get('toCurrency'),
                                                float(request.values.get('volume')),
                                                float(request.values.get('nrTransactions')))

    return response


@app.route('/available', methods=['GET'])
def is_quote_service_available():
    return n1QuotesService.are_quotes_available()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=13022)
