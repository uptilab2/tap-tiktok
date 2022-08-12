#!/usr/bin/env python3
import sys
import json
import singer
from datetime import datetime, timedelta
from tap_tiktok.discover import discover
from tap_tiktok.client import TiktokClient, DATE_FORMAT


logger = singer.get_logger()


REQUIRED_CONFIG_KEYS = [
    "access_token",
    "advertiser_id",
]


def do_discover():

    logger.info('Starting discover')
    catalog = discover()
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    logger.info('Finished discover')


def sync(client, config, state, catalog):
    """ Sync data from tap source """
    # Loop over selected streams in catalog
    for stream in catalog.get_selected_streams(state):
        stream_id = stream.tap_stream_id
        logger.info("Syncing stream:" + stream_id)

        singer.write_schema(
            stream_name=stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )

        yesterday = datetime.now() - timedelta(1)
        day = state.get(stream_id) or config.get('start_date')
        day = day and datetime.strptime(day, DATE_FORMAT) or yesterday
        day = day - timedelta(int(config.get('window_size', '0')))

        while day <= yesterday:
            tap_data = client.request_report(stream, day)
            singer.write_records(stream_id, tap_data)
            state[stream_id] = day.strftime(DATE_FORMAT)
            singer.write_state(state)
            day += timedelta(1)

    return


@singer.utils.handle_top_exception(logger)
def main():
    # Parse command line arguments
    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)
    config = parsed_args.config
    with TiktokClient(
        config['access_token'],
        config['advertiser_id']
    ) as client:
        if parsed_args.discover:
            do_discover()
        elif parsed_args.catalog:
            sync(
                client=client,
                config=config,
                catalog=parsed_args.catalog,
                state=parsed_args.state or {}
            )


if __name__ == "__main__":
    main()
