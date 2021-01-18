import os
import json
import singer

logger = singer.get_logger()

possible_params = {
    "service_type": ["AUCTION", "RESERVATION"],
    "report_type": ["BASIC", "AUDIENCE", "PLAYABLE_MATERIAL"],
    "data_level": ["AUCTION_AD", "AUCTION_ADGROUP", "AUCTION_ADVERTISER", "AUCTION_CAMPAIGN", "RESERVATION_AD", "RESERVATION_ADVERTISER", "RESERVATION_CAMPAIGN"]
}

AVAILABLE_STREAMS = {
    "RESERVATION": ["BASIC"],
    "AUCTION": ["BASIC", "AUDIENCE", "PLAYABLE_MATERIAL"]
}

DIMENSIONS = ['advertiser_id', 'campaign_id', 'adgroup_id', 'ad_id', 'stat_time_day', 'stat_time_hour']


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def get_schemas():
    schemas = {}
    metadata = {}
    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = json.load(file)
    return schemas, metadata
