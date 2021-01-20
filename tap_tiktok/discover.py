from singer import get_logger
from singer.catalog import Catalog, CatalogEntry, Schema
from tap_tiktok.schema import get_schemas

logger = get_logger()


def discover(config):
    schemas, field_metadata = get_schemas()
    catalog = Catalog([])

    for stream_name, schema_dict in schemas.items():
        schema = Schema.from_dict(schema_dict)
        mdata = field_metadata.get(stream_name, {})
        mdata["selected"] = config['service_type'] == mdata['service_type'] and config['report_type'] == mdata['report_type']

        catalog.streams.append(CatalogEntry(
            stream=stream_name,
            tap_stream_id=stream_name,
            key_properties=[],
            schema=schema,
            metadata=[{"metadata": mdata, "breadcrumb": []}]
        ))

    return catalog
