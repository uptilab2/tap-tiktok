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
  "start_date": string (YYYY-MM-DD),
  "advertiser_id": comma separated string
}
```


---

Copyright &copy; 2018 Stitch, Reeport.io
