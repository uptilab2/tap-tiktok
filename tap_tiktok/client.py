
import singer
import requests
import time
import tempfile
import csv
import json
import backoff
import io
from datetime import datetime, timedelta

logger = singer.get_logger()
BASE_API_URL = 'https://ads.tiktok.com/open_api/v1.1'
POLLING_TIME = 60 # 1 minute is the recommandation


class ClientHttpError(Exception):
    pass

class ClientTooManyRequestError(Exception):
    pass

class ClientHttp5xxError(Exception):
    pass

class ClientExpiredError(Exception):
    pass

class TiktokClient:
    """
        Handle tiktok consolidated reporting request
        ressource : https://ads.tiktok.com/marketing_api/docs?rid=l3f3i273f9k&id=1685752851588097
    """
    def __init__(self, advertiser_id, access_token):
        self.advertiser_id = advertiser_id
        self.access_token = access_token
        self.expires = None
        self.session = requests.Session()
    
    def __exit__(self, *args):
        self.session.close()
        
    @backoff.on_exception(backoff.expo, (ClientTooManyRequestError, ClientExpiredError), max_tries=7)
    def do_request(self, url, **kwargs):

        req = requests.get

        if not kwargs.get('headers'):
            kwargs['headers'] = {"Access-Token": self.access_token, "Content-Type": "application/json"}
        if not kwargs.get('params'):
            kwargs['params'] = {"advertiser_id": self.advertiser_id}
        
        response = req(url=url, **kwargs)
        logger.info(f'request api: {url}, response status: {response.status_code}')
        if response.status_code == 200 or response.status_code == 202:
            return response

        #handle error
        error_response = response.json()
        if response.status_code == 429:
            raise ClientTooManyRequestError(f'Too many requests, retry ..')
        elif response.status_code == 401:
            raise ClientExpiredError(f'Token is expired, retry ..')
        else:
            message = error_response['error']['errors'][0]['message']
            raise ClientHttpError(f'{response.status_code}: {message}')

    def request_report(self):
        params = {
            "advertiser_id": self.advertiser_id,
            "report_type": ,
            "start_date": "2020-10-10",
            "end_date": "2020-11-10",
            "page": 1,
            "page_size": 100
        }
        response = self.do_request(f"{BASE_API_URL}/reports/integrated/get/", params=params)
        resp = response.json()
        logger.critical(resp)
        return resp


