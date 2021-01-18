

STREAMS = {
    "service_type": {
        "AUCTION": {
            "report_type": {
                "BASIC": {
                    "data_level": ["AUCTION_AD", "AUCTION_ADGROUP", "AUCTION_ADVERTISER", "AUCTION_CAMPAIGN"],
                    "dimensions": ["advertiser_id", "campaign_id", "adgroup_id", "ad_id", "stat_time_day", "stat_time_hour"]
                },
                "AUDIENCE": {
                    "data_level": ["AUCTION_AD", "AUCTION_ADGROUP", "AUCTION_ADVERTISER", "AUCTION_CAMPAIGN"],
                    "dimensions": ["advertiser_id", "campaign_id", "adgroup_id", "ad_id", "stat_time_day", "stat_time_hour", "gender", "age", "country_code", "ac", "language", "platform", "interest_category", "placement"]
                },
                "PLAYABLE_MATERIAL": {
                    "dimensions": ["playable_id", "country_code	"]
                },
            }
        },
        "RESERVATION": {
            "report_type": {
                "BASIC"{
                    "data_level": {
                        "RESERVATION_AD",
                        "RESERVATION_ADVERTISER",
                        "RESERVATION_CAMPAIGN",
                    },
                    "dimensions": ["advertiser_id", "campaign_id", "adgroup_id", "ad_id", "stat_time_day", "stat_time_hour"]
                },
            }
        },
    }
}