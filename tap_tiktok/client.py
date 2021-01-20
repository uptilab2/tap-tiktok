
import singer
import requests
import time


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
        logger.info(result)
        if response.status_code == 429:
            raise ClientHttpError('Too many requests, retry ..')
        elif response.status_code == 401:
            raise ClientHttpError('Token is expired, retry ..')
        elif response.status_code == 200 or response.status_code == 202:
            if not result.get("data") and result.get("message"):
                raise ClientHttpError(f"[{result.get('code', 0)}] {result['message']}")
        return result["data"]

    def request_report(self, stream):
        service_type, report_type = stream.tap_stream_id.upper().split('_', 1)
        mdata = singer.metadata.to_map(stream.metadata)[()]
        has_data_level = self.data_level and self.data_level in mdata.get("data_level", {})
        dimensions = []
        if has_data_level:
            dimensions = [f"{self.data_level.split('_')[-1].lower()}_id", self.time_dimension]
        if self.id_dimension and self.id_dimension in mdata.get("dimensions", []):
            dimensions.append(self.id_dimension)
        params = {
            "report_type": report_type,
            "service_type": service_type,
            "dimensions": dimensions,
            "metrics": [
                m
                for m in stream.schema.properties.keys()
                if m not in mdata.get("data_level", {}).get(self.data_level, {}).get("unsupported_metrics", [])
            ],
            "start_date": "2021-01-18",
            "end_date": "2021-01-18",
            "page": 1,
            "page_size": 100
        }
        if has_data_level:
            params["data_level"] = self.data_level
        data = []
        total_page = 2
        while total_page > params["page"]:
            if params["page"] > 1:
                time.sleep(1/QUERIES_SECOND)
            result = self.do_request(f"{BASE_API_URL}/reports/integrated/get/", params=params)
            data += parse_results(result["list"])
            params["page"] += 1
            total_page = result["page_info"]["total_page"]

        return data


def parse_results(result):
    return [
        {
            **r["metrics"],
            **r["dimensions"]
        }
        for r in result
    ]
