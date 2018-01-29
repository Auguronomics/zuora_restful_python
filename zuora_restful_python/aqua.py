"""
    Class AQuA

    wraps the Zuora rest api with OAutv2 authentication
"""

# pylint: disable=C0111,R0904,R0913

import datetime
import json
import time
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

ZUORA_CHUNKSIZE = 50


def _unpack_response(operation, path, response):
    if path != '/object/invoice/':
        assert response.status_code == 200, \
            '{} to {} failed: {}'.format(operation, path, response.content)
    if path.startswith('/file/'):
        return response

    return json.loads(response.text)


class AQuA(object):
    """
    instantiates a connection to Zuora service
    """

    def __init__(self, client_id, client_secret, endpoint='production', header={}):

        client = BackendApplicationClient(client_id=client_id)
        self.oauth = OAuth2Session(client=client)
        self.token = self.oauth.fetch_token(token_url='https://rest.zuora.com/oauth/token',
                                            client_id=client_id, client_secret=client_secret)
        self.headers = header

        if endpoint == 'production':
            self.endpoint = 'https://www.zuora.com/apps/api/'
        elif endpoint == 'sandbox':
            self.endpoint = 'https://apisandbox.zuora.com/apps/api'
        else:
            self.endpoint = endpoint

    def _get(self, path, payload=None):
        response = self.oauth.request('GET', self.endpoint + path,
                                      headers=self.headers,
                                      data=payload)
        return _unpack_response('GET', path, response)

    def _post(self, path, payload):
        response = self.oauth.request('POST', self.endpoint + path,
                                      data=json.dumps(payload),
                                      headers=self.headers)
        return _unpack_response('POST', path, response)

    def query(self, payload):
        response = self._post("/batch-query/", payload)

        return response

    def jobs(self, job_id):
        response = self._get("/batch-query/jobs/{}".format(job_id), payload={})

        return response

    def download(self, file_id):
        response = self._get("/file/{}".format(file_id), file_id)

        return response
