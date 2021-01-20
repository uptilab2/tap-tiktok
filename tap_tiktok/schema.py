import os
import json
import singer
from tap_tiktok.streams import STREAMS

logger = singer.get_logger()


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

        service, report = file_raw.upper().split("_", 1)
        metadata[file_raw] = STREAMS["service_type"].get(service, {}).get("report_type", {}).get(report, {})
        metadata[file_raw]["service_type"] = service
        metadata[file_raw]["report_type"] = report
    return schemas, metadata
