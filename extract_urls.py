#!/usr/bin/env python3

from cortexutils.responder import Responder
from thehive4py.api import TheHiveApi
from thehive4py.query import Eq, And


class ExtractUrls(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.case_id = self.get_param('data.id')
        self.data_type = self.get_param('dataType', default='unknown')
        self.thehive_url = self.get_param('config.thehive_url')
        self.thehive_key = self.get_param('config.thehive_key')
        self.thehive_api = TheHiveApi(self.thehive_url, self.thehive_key)
        self.check_tlp = self.get_param('config.check_tlp', default=True)
        self.max_tlp = self.get_param('config.max_tlp', default=2)

    def run(self):
        Responder.run(self)

        query = And(Eq('dataType', 'url'), Eq('ioc', True))  # optional filtering by URL and IOC status, redundant with line 45 for demonstration
        response = self.thehive_api.get_case_observables(self.case_id, query=query)  # query the API for observables attached to the case
        observables = response.json()  # regardless of the thehive4py's documentation, the line above actually returns <class 'requests.models.Response'>, so we need to get the JSON object from it

        # essentially equivalent to the thehive4py version above:
        # import requests
        # url = self.thehive_url + '/api/case/artifact/_search'
        # query = {'query': {'_and': ({'_parent': {'_type': 'case', '_query': {'_id': self.case_id}}}, {'_and': ({'_field': 'dataType', '_value': 'url'}, {'_field': 'ioc', '_value': True})})}}
        # response = requests.post(url, json=query, headers={'Authorization': f'Bearer {self.thehive_key}'}, verify=False)
        # observables = response.json()

        extracted_urls = extract_urls(observables)  # replace this with mailing the observables or whatever you want to do

        self.report({'message': 'URLs extracted', 'urls': extracted_urls})  # the urls attribute is optional, this line is minimally: self.report({'message': ''})

    def operations(self, raw):
        return [self.build_operation('AddTagToCase', tag='ExtractUrls:UrlsExtracted')]  # optional


def extract_urls(observables):
    # replace all this with emailing the observables or whatever you want to do. Don't forget to add a check to compare observable['tlp] against self.max_tlp if that's a thing you want to do

    for observable in observables:
        if observable['ioc'] and observable['dataType'] == 'url':  # optional filtering by URL and IOC status, redundant with line 22 for demonstration
            # observables will be dict objects that look like:
            {'_id': '~28720', 'id': '~28720', 'createdBy': 'thehive@thehive.local', 'createdAt': 1629316150415, '_type': 'case_artifact', 'dataType': 'url', 'data': 'https://www.test.com/ioc.html', 'startDate': 1629316150415, 'tlp': 2, 'tags': ['test'], 'ioc': True, 'sighted': True, 'message': '', 'reports': {}, 'stats': {}, 'ignoreSimilarity': False}

        return [observable['data'] for observable in observables if observable['ioc'] and observable['dataType'] == 'url']  # optionally hand these back for the responder report


if __name__ == '__main__':
    ExtractUrls().run()
