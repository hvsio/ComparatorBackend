from flask import Flask, request, json, Response
from src.service.BankSupplierService import BankSupplierService
from src.service.MarginsQuotesService import MarginSaverQuotesService
from src.service.ScrapperControllerConnection import ScrapperConfigConnection
from src.service.N1QuotesService import N1QuotesService
from src.models.SepaCountries import SepaCountries

app = Flask(__name__)

bank_supplier_service = BankSupplierService()
scrapper_connection = ScrapperConfigConnection()


@app.route('/banksuppliers', methods=['GET'])
def get_data_fe():
    response = bank_supplier_service.get_supplier(request.values.get('fromCountry'),
                                                  request.values.get('toCountry'),
                                                  request.values.get('fromCurrency'),
                                                  request.values.get('toCurrency'),
                                                  float(request.values.get('volume')),
                                                  float(request.values.get('nrTransactions')))

    return response


@app.route('/available', methods=['GET'])
def is_quote_service_available():
    return bank_supplier_service.are_quotes_available()


@app.route('/fromcountries', methods=['GET'])
def get_from_countries():
    return Response(response=json.dumps(SepaCountries, indent=2),
                    status=200,
                    mimetype='application/json')


@app.route('/allowedcurrencies', methods=['GET'])
def get_allowed_currencies():
    return scrapper_connection.get_currencies_with_response()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=13022)
