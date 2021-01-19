#!/usr/bin/env python3
import sys
import json
import singer
from tap_tiktok.discover import discover
from tap_tiktok.client import TiktokClient


API_URL = "https://ads.tiktok.com/open_api"
logger = singer.get_logger()


REQUIRED_CONFIG_KEYS = [
    "access_token",
    "advertiser_ids",
]


def do_discover(config):

    logger.info('Starting discover')
    catalog = discover(config)
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    logger.info('Finished discover')


def sync(client, config, state, catalog):
    """ Sync data from tap source """
    # Loop over selected streams in catalog
    for stream in catalog.get_selected_streams(state):
        logger.info("Syncing stream:" + stream.tap_stream_id)

        bookmark_column = stream.replication_key
        is_sorted = True  # TODO: indicate whether data is sorted ascending on bookmark value

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )

        # TODO: delete and replace this inline function with your own data retrieval process:
        tap_data = client.request_report(stream)
        max_bookmark = None
        for row in tap_data:
            # TODO: place type conversions or transformations here

            # write one or more rows to the stream:
            singer.write_records(stream.tap_stream_id, [row])
            if bookmark_column:
                if is_sorted:
                    # update bookmark to latest value
                    singer.write_state({stream.tap_stream_id: row[bookmark_column]})
                else:
                    # if data unsorted, save max value until end of writes
                    max_bookmark = max(max_bookmark, row[bookmark_column])
        if bookmark_column and not is_sorted:
            singer.write_state({stream.tap_stream_id: max_bookmark})
    return


@singer.utils.handle_top_exception(logger)
def main():
    # Parse command line arguments
    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)
    config = parsed_args.config
    with TiktokClient(
        config['access_token'],
        config['advertiser_ids'],
        config['data_level'],
        config['id_dimension'],
        config['time_dimension']
    ) as client:
        if parsed_args.discover:
            do_discover(config)
        elif parsed_args.catalog:
            sync(
                client=client,
                config=config,
                catalog=parsed_args.catalog,
                state=parsed_args.state or {}
            )


if __name__ == "__main__":
    main()
