

STREAMS = {
    "service_type": {
        "AUCTION": {
            "report_type": {
                "BASIC": {
                    "data_level": {
                        "AUCTION_AD": {
                            "unsupported_metrics": ['stat_time_day', 'profile_visites', 'cost_per_total_ratings', 'profile_visites_rate',
                                                    'comments', 'advertiser_id', 'shares', 'aeo_type', 'stat_time_hour',
                                                    'app_event_cost_per_add_to_cart', 'likes'],
                            "supported_dimensions": ["ad_id"]
                        },
                        "AUCTION_ADGROUP": {
                            "unsupported_metrics": ["ad_id", 'stat_time_day', 'ad_text', 'adgroup_id', 'cost_per_total_ratings', 'profile_visites_rate',
                                                    'shares', 'advertiser_id', 'ad_name', 'comments', 'stat_time_hour', 'profile_visites',
                                                    'app_event_cost_per_add_to_cart', 'likes'],
                            "supported_dimensions": ["adgroup_id"],
                        },
                        "AUCTION_ADVERTISER": {
                            "unsupported_metrics": ["ad_id", 'stat_time_day', 'profile_visites', 'ad_text', 'adgroup_id', 'cost_per_total_ratings',
                                                    'profile_visites_rate', 'campaign_id', 'shares', 'advertiser_id', 'adgroup_name', 'ad_name',
                                                    'comments', 'stat_time_hour', 'aeo_type', 'campaign_name', 'app_event_cost_per_add_to_cart',
                                                    'likes'],
                            "supported_dimensions": ["advertiser_id"],
                        },
                        "AUCTION_CAMPAIGN": {
                            "unsupported_metrics": ["ad_id", 'stat_time_day', 'ad_text', 'adgroup_id', 'cost_per_total_ratings', 'profile_visites_rate',
                                                    'campaign_id', 'shares', 'advertiser_id', 'adgroup_name', 'ad_name', 'comments', 'stat_time_hour',
                                                    'aeo_type', 'profile_visites', 'app_event_cost_per_add_to_cart', 'likes'],
                            "supported_dimensions": ["campaign_id"],
                        }
                    },
                    "dimensions": ["advertiser_id", "campaign_id", "adgroup_id", "ad_id", "stat_time_day", "stat_time_hour"]
                },
                "AUDIENCE": {
                    "data_level": {
                        "AUCTION_AD": {},
                        "AUCTION_ADGROUP": {},
                        "AUCTION_ADVERTISER": {},
                        "AUCTION_CAMPAIGN": {}
                    },
                    "dimensions": ["advertiser_id", "campaign_id", "adgroup_id", "ad_id", "stat_time_day", "stat_time_hour",
                                   "gender", "age", "country_code", "ac", "language", "platform", "interest_category", "placement"]
                },
                "PLAYABLE_MATERIAL": {
                    "dimensions": ["playable_id", "country_code	"]
                },
            }
        },
        "RESERVATION": {
            "report_type": {
                "BASIC": {
                    "data_level": {
                        "RESERVATION_AD",
                        "RESERVATION_ADVERTISER",
                        "RESERVATION_CAMPAIGN",
                    },
                    "dimensions": ["advertiser_id", "campaign_id", "adgroup_id", "ad_id", "stat_time_day", "stat_time_hour"]
                },
            },
            "lifetime": False
        },
    }
}
