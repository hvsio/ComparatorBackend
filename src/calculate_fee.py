import requests



class CalculateFee:

    def get_fee(self):
        payload = {}
        response = requests.get(' ', params=payload)
        return response

    def calculate_fees(self, frequency):
        imported_fee = self.getFee
        return imported_fee * frequency

    def calculate_n1_fees(self, imported_fee, frequency):
        return imported_fee * frequency
