from flask import Flask, request, json

from src import MSQuotesService, N1QuotesService
from src.received_info import ReceivedInfo


app = Flask(__name__)


@app.route('/n1quote')
def get_n1_quote():  # TODO parameters
    n1 = N1QuotesService.N1QuotesService()
    response = n1.get_quote('DK', 'DE', 'EUR', 'SEK', '1000')
    return response.text


@app.route('/msquote')
def get_ms_quote():  # TODO parameters
    ms = MSQuotesService.MSQuotesService()
    response = ms.get_ms_result('DK', 'DKK', 'EUR', 3, 1000)
    return json.dumps(response)


@app.route('/calculate')
def calculate():
    n1_quotes = get_n1_quote()
    ms_quotes = get_ms_quote()

@app.route('/banksuppliers', methods=['GET'])
def get_data_fe():
    posted_data = request.get_json()
    #info = ReceivedInfo(**posted_data)

    from_country = request.values.get('fromCountry')
    to_country = request.values.get('toCountry')
    from_currency = request.values.get('fromCurrency')
    to_currency = request.values.get('toCurrency')
    amount = request.values.get('amount')
    frequency = request.values.get('frequency')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
