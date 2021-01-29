# tap-tiktok

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from Tiktok Ads API (https://ads.tiktok.com/marketing_api/homepage)
- Extracts the Tiktok Ads API reporting capabilities:
  - Auction Ads
  - Reservation Ads
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

### Config
```
{
  "access_token": string, 
  "data_level": [one of : AD, ADGROUP, ADVERTISER, CAMPAIGN]
  "id_dimension": [one of : 
      - for audience : gender, age, country_code, ac, language, platform, interest_category, placement
      - for playable material : playable_id, country_code
  ]
  "start_date": YYYY-MM-DD,
  "advertiser_id": coma separated string
}
```


---

Copyright &copy; 2018 Stitch, Reeport.io
