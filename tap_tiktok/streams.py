import os
import singer
import hashlib
import json
from copy import copy
from datetime import datetime, timedelta


logger = singer.get_logger()


possible_params : {
    "service_type": ["AUCTION", "RESERVATION"],
    "report_type": ["BASIC", "AUDIENCE", "PLAYABLE_MATERIAL"],
    "data_level": ["AUCTION_AD", "AUCTION_ADGROUP", "AUCTION_ADVERTISER", "AUCTION_CAMPAIGN", "RESERVATION_AD", "RESERVATION_ADVERTISER", "RESERVATION_CAMPAIGN"]
}

AVAILABLE_STREAMS = {
    "RESERVATION": ["BASIC"],
    "AUCTION", ["BASIC", "AUDIENCE", "PLAYABLE_MATERIAL"]
}
