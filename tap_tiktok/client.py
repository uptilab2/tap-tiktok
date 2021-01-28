
import singer
import requests
import time
from datetime import datetime, timedelta


logger = singer.get_logger()
BASE_API_URL = 'https://ads.tiktok.com/open_api/v1.1'

# query limits
QUERIES_SECOND = 10
QUERIES_MINUTE = 600
QUERIES_DAY = 864000

DATE_FORMAT = "%Y-%m-%d"


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

    def __init__(self, access_token, advertiser_ids, data_level, id_dimension, start_date):
        self.access_token = access_token
        self.advertiser_ids = advertiser_ids
        self.data_level = data_level.upper()
        self.id_dimension = id_dimension
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)

    def do_request(self, url, params={}):
        headers = {"Access-Token": self.access_token, "Content-Type": "application/json"}
        params = {"advertiser_id": self.advertiser_ids[0], **params}
        response = requests.get(
            url=url,
            headers=headers,
            json=params
        )
        logger.info(f'request api - response status: {response.status_code}')

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
        service_type, report_type = stream.tap_stream_id.upper().split('_', 1)
        mdata = singer.metadata.to_map(stream.metadata)[()]
        
        data_level = f"{service_type}_{self.data_level}"
        has_data_level = data_level and data_level in mdata.get("data_level", {})

        dimensions = []
        if has_data_level:
            dimensions.append(f"{self.data_level.lower()}_id")
        if self.id_dimension and self.id_dimension in mdata.get("dimensions", []):
            dimensions.append(self.id_dimension)

        yesterday = datetime.now() - timedelta(1)
        start_date = self.start_date or yesterday
        data = []
        for day in [start_date + timedelta(days=x) for x in range((yesterday-start_date).days + 1)]:
            date = day.strftime(DATE_FORMAT)
            logger.info(f"Request for date {date}")
            params = {
                "report_type": report_type,
                "service_type": service_type,
                "dimensions": dimensions,
                "metrics": [
                    m
                    for m in stream.schema.properties.keys()
                    if m not in mdata.get("data_level", {}).get(data_level, {}).get("unsupported_metrics", [])
                ],
                "start_date": date,
                "end_date": date,
                "page": 1,
                "page_size": 100
            }
            logger.critical(params)
            if has_data_level:
                params["data_level"] = data_level
            
            total_page = 2
            while total_page >= params["page"]:
                logger.info(f"...page {params['page']}/{total_page}...")
                if params["page"] > 1:
                    time.sleep(1/QUERIES_SECOND)
                result = self.do_request(f"{BASE_API_URL}/reports/integrated/get/", params=params)
                data += parse_results(result["list"], date)
                params["page"] += 1
                total_page = result["page_info"]["total_page"]

        return data


def parse_results(result, date):
    return [
        {
            "date": date,
            **{
                key: val
                for key, val in r["metrics"].items()
                if val != "-"
            },
            **r["dimensions"]
        }
        for r in result
    ]
