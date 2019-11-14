from IN1Quotes import IN1Quotes
from interface import implements
import requests

class N1Quotes(implements(IN1Quotes)):

    def get_quote(self, from_country_code, to_country_code, from_currency_code, to_currency_code, amount):
        payload = {"fromCountryCode": from_country_code,
                   "toCountryCode": to_country_code,
                   "fromCurrencyCode": from_currency_code,
                   "toCurrencyCode": to_currency_code,
                   "amount": amount,
                   "feeType": "Shared",
                   "side": "Buy",
                   "paymentType": "Spot"}
        response = requests.get("https://api.novemberfirst.com/v1/quote", params=payload)
        return response


if __name__ == '__main__':
    n1 = N1Quotes()
    response = n1.get_quote("DK", "DE", "EUR", "SEK", "1000")
    print(response.text)
