from singer import metadata
from singer.catalog import Catalog, CatalogEntry, Schema
from tap_tiktok.schema import get_schemas


def discover():
    schemas, field_metadata = get_schemas()
    catalog = Catalog([])

    for stream_name, schema_dict in schemas.items():
        schema = Schema.from_dict(schema_dict)
        mdata = metadata.to_map(field_metadata.get(stream_name, {}))

        catalog.streams.append(CatalogEntry(
            stream=stream_name,
            tap_stream_id=stream_name,
            key_properties=[],
            schema=schema,
            metadata=metadata.to_list(mdata)
        ))

    return catalog
