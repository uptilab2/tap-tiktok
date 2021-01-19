
import singer
import requests


logger = singer.get_logger()
BASE_API_URL = 'https://ads.tiktok.com/open_api/v1.1'

# query limits
QUERIES_SECOND = 10
QUERIES_MINUTE = 600
QUERIES_DAY = 864000


class ClientHttpError(Exception):
    pass


class TiktokClient:
    """
        Handle tiktok consolidated reporting request
        ressource : https://ads.tiktok.com/marketing_api/docs?rid=l3f3i273f9k&id=1685752851588097
    """
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        logger.info("client closed")

    def __init__(self, access_token, advertiser_ids, data_level, id_dimension, time_dimension):
        self.access_token = access_token
        self.advertiser_ids = advertiser_ids
        self.data_level = data_level
        self.id_dimension = id_dimension
        self.time_dimension = time_dimension

    def do_request(self, url, params={}):
        headers = {"Access-Token": self.access_token, "Content-Type": "application/json"}
        params = {"advertiser_id": self.advertiser_ids[0], **params}
        response = requests.get(
            url=url,
            headers=headers,
            json=params
        )
        logger.info(f'request api: {url}, response status: {response.status_code}')

        result = response.json()
        if response.status_code == 429:
            raise ClientHttpError('Too many requests, retry ..')
        elif response.status_code == 401:
            raise ClientHttpError('Token is expired, retry ..')
        elif response.status_code == 200 or response.status_code == 202:
            if not result.get("data") and result.get("message"):
                raise ClientHttpError(f"[{result.get('code', 0)}] {result['message']}")
        return result["data"]

    def request_report(self, stream):
        service_type, report_type = stream.tap_stream_id.upper().split('_')
        mdata = singer.metadata.to_map(stream.metadata)[()]
        logger.info(" ")
        logger.info(" ")
        logger.info(" ")
        logger.info(mdata["data_level"][self.data_level].get("unsupported_metrics", []))
        logger.info([
                m
                for m in stream.schema.properties.keys()
                if m not in mdata["data_level"][self.data_level].get("unsupported_metrics", [])
            ])
        logger.info(" ")
        logger.info(" ")
        logger.info(" ")
        params = {
            "report_type": report_type,
            "service_type": service_type,
            "data_level": self.data_level,
            "dimensions": [self.id_dimension, self.time_dimension],
            "metrics": [
                m
                for m in stream.schema.properties.keys()
                if m not in mdata["data_level"][self.data_level].get("unsupported_metrics", [])
            ],
            "start_date": "2021-01-18",
            "end_date": "2021-01-18",
            "page": 1,
            "page_size": 100
        }
        data = []
        total_page = 2
        while total_page > params["page"]:
            result = self.do_request(f"{BASE_API_URL}/reports/integrated/get/", params=params)
            data += result["list"]
            params["page"] += 1
            total_page = result["page_info"]["total_page"]

        return data
