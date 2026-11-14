# Data ingestion

Imagery enters GeoTALOS in two stages: the browser uploads the file to object storage, then a background job validates it and registers it in the STAC catalog.

## 1. Upload: multipart, straight to storage

Large rasters are uploaded in parts so a failed part can be retried without starting over.

| Step | Endpoint |
|---|---|
| Start an upload and get presigned URLs for the first parts | `POST /api/v1/datasets/{dataset_id}/uploads/initiate` |
| Get URLs for more parts | `POST /api/v1/datasets/{dataset_id}/uploads/{upload_id}/part-urls` |
| Finish the upload and queue ingestion | `POST /api/v1/datasets/{dataset_id}/uploads/{upload_id}/complete` |
| Cancel an upload | `DELETE /api/v1/datasets/{dataset_id}/uploads/{upload_id}` |

- Parts are **50 MiB** each, and the first response already carries URLs for **50 parts**, enough for files under about 2.5 GB in one round trip.
- The browser `PUT`s each part to MinIO using a presigned URL, so file bytes do not pass through the API. A proxy route (`PUT .../parts/{part_number}`) exists for setups where the browser cannot reach MinIO directly.
- S3 limits apply: at most 10,000 parts, so about 488 GiB per file.

## 2. Ingestion job

Completing the upload queues `ingest_dataset` on the `ingestion` queue (`app/workers/ingestion/tasks.py`). For each GeoTIFF it:

1. **Validates** the file (`validate_cog`).
2. **Reads metadata**: bounds, CRS, bands, data type and acquisition date (`extract_cog_metadata`).
3. **Builds a STAC Item** and upserts it into pgSTAC, inside one STAC Collection per dataset.
4. **Creates a `DatasetItem`** row in the application database, with the acquisition date cached as `item_datetime`.
5. **Computes summary metadata** for the dataset (band counts, native CRS) and sets its status.

### Validation

GeoTALOS accepts any valid GeoTIFF but tells you when it is not cloud optimised.

| Result | Cause |
|---|---|
| **Rejected** | GDAL cannot open the file, or it has no raster bands |
| **Ingested with a warning** | Not tiled, block size larger than 512 px, no overviews, or no compression |

Files with warnings still work but tile slowly. Convert them to COGs (for example `gdal_translate -of COG in.tif out.tif`) and upload again for best performance.

### Acquisition dates

Temporal features depend on each scene's date. The ingestion job looks for it in this order:

1. A timestamp at the start of the filename: `YYYYMMDDTHHMMSSZ_name.tif` (or a start and end pair)
2. GeoTIFF metadata tags such as `TIFFTAG_DATETIME`, `ACQUISITIONDATETIME`, `DATE`, `acquisition_date`, and Earth Engine's `system:time_start`
3. A date in the filename: `YYYY-MM-DD`, then `YYYYMMDD`, then `YYYY-MM`
4. Otherwise, the **current time** (a warning is logged)

!!! tip
    Put the acquisition date in the filename, for example `2024-05-12_site_a.tif`. Otherwise every scene may get the upload time and appear on the same date in temporal views.

### ZIP uploads

A ZIP of `.tif` files is ingested in one job:

- **Flat or single-folder ZIP:** every file goes into the dataset you uploaded to.
- **Multi-folder ZIP:** each top-level folder becomes its own dataset and STAC Collection.

## Dataset status

| Status | Meaning |
|---|---|
| `pending` | Dataset created, no file yet |
| `ingesting` | The ingestion job is running |
| `ready` | Registered in STAC; tiles are available |
| `failed` | Ingestion or validation failed |

The job also publishes a `job.completed` or `job.failed` event, which workflows and webhooks can react to.

## Serving the imagery

Rasters are never converted into tile pyramids. They stay in MinIO as COGs, and TiTiler reads only the parts needed for each map tile. Per-item rendering settings are available from `GET /api/v1/datasets/{dataset_id}/items/{item_id}/tile-config`.
