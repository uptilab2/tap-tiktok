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
        service, report = file_raw.upper().split("_", 1)
        with open(path) as file:
            report_stream = STREAMS["service_type"].get(service, {}).get("report_type", {}).get(report, {})
            for dim in report_stream.get("dimensions", [None]):
                dims = [] if not dim else dim.split(",")
                for level, infos in report_stream.get("data_level", {None: {}}).items():
                    dimensions = {
                        "date": {"type": ["null", "string"], "format": "date-time"},
                        **{
                            d: {"type": ["null", "string"]}
                            for d in dims
                        }
                    }
                    if level:
                        dimensions[f"{level.lower()}_id"] = {"type": ["null", "integer"]}

                    file.seek(0)
                    schema_data = json.load(file)

                    schema_data["properties"] = {
                        key: val
                        for key, val in schema_data["properties"].items()
                        if key not in infos.get("unsupported_metrics", [])
                    }
                    schema_data["properties"].update(dimensions)

                    schema_id = file_raw
                    if level:
                        schema_id += f"_{level.lower()}"
                    if dims:
                        schema_id += f"_{'_'.join(dims)}"
                    schemas[schema_id] = schema_data
                    metadata[schema_id] = {
                        "service_type": service,
                        "report_type": report,
                        "dimensions": [d for d in dimensions if d != "date"]
                    }
                    if level:
                        metadata[schema_id]["data_level"] = f"{service}_{level}"
    return schemas, metadata
