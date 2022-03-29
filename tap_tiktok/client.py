
import singer
import requests


logger = singer.get_logger()
BASE_API_URL = 'https://ads.tiktok.com/open_api/v1.2'

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

    def __init__(self, access_token, advertiser_id):
        self.access_token = access_token
        self.advertiser_ids = advertiser_id.split(",")

    @singer.utils.ratelimit(600, 60)
    def do_request(self, url, params={}):
        headers = {"Access-Token": self.access_token, "Content-Type": "application/json"}
        response = requests.get(
            url=url,
            headers=headers,
            json=params
        )
        logger.info(f'request api - response status: {response.status_code}')

        result = response.json()
        if response.status_code == 429:
            raise ClientHttpError('Too many requests')
        elif response.status_code == 401:
            raise ClientHttpError('Token is expired')
        elif response.status_code == 200 or response.status_code == 202:
            if not result.get("data") and result.get("message"):
                raise ClientHttpError(f"[{result.get('code', 0)}] {result['message']}")
        return result["data"]

    def request_report(self, stream, day):
        mdata = singer.metadata.to_map(stream.metadata)[()]
        data = []
        date = day.strftime(DATE_FORMAT)
        date_time = day.strftime("%Y-%m-%d 00:00")
        logger.info(f"Request for date {date}")
        for advertiser_id in self.advertiser_ids:
            logger.info(f"advertiser {advertiser_id}")
            params = {
                "advertiser_id": advertiser_id,
                "metrics": [
                    m
                    for m in stream.schema.properties.keys()
                    if m not in mdata.get("dimensions", [])
                    and m != "date"
                ],
                "start_date": date,
                "end_date": date,
                "page": 1,
                "page_size": 1000
            }
            params.update(mdata)

            total_page = 2
            while total_page >= params["page"]:
                logger.info(f"...page {params['page']}/{total_page}...")
                result = self.do_request(f"{BASE_API_URL}/reports/integrated/get/", params=params)
                data += parse_results(result["list"], date_time)
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
