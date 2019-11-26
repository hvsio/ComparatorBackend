from interface import Interface, implements
from src.environment.enviroment import Config
from flask import Response, json
import sys
import requests


class IScrapperConfigConnection(Interface):
    def get_currencies_with_response(self):
        pass

    def get_fees(self, country):
        pass


class ScrapperConfigConnection(implements(IScrapperConfigConnection)):
    def __init__(self):
        Config.initialize()
        self.scrapper_config_url = Config.cloud('SCRAPPER_CONFIG') if (
                len(sys.argv) > 1 and sys.argv[1] == 'cloud') else Config.dev(
            'SCRAPPER_CONFIG')

    def get_currencies_with_response(self):
        request = requests.get(self.scrapper_config_url + '/currencies')
        return Response(
            response=json.dumps(request.json(), indent=2),
            status=request.status_code,
            mimetype='application/json')

    def get_fees(self, country):
        fees_response = requests.get(self.scrapper_config_url + '/fees/' + country)
        return fees_response.json()
