# Tiles, caching and reference layers

GeoTALOS never sends a whole image or a whole annotation set to the browser. Everything on the map is cut into tiles and only the tiles on screen are loaded.

| What | Tile type | Served by | Through |
|---|---|---|---|
| Imagery (COGs) | Raster (PNG, JPEG, WebP) | TiTiler | `/api/v1/tiles/...` |
| Annotation sets (private) | Vector (MVT, `.pbf`) | Martin from PostGIS | `/api/v1/annotation-sets/{set_id}/tiles/{z}/{x}/{y}.pbf` |
| Reference layers (public) | Vector (MVT) | Martin from PostGIS or PMTiles | `/api/v1/reference-layers/{name}/tiles/{z}/{x}/{y}.pbf` |

## Raster tiles

COGs stay in MinIO and TiTiler reads only the bytes needed for each tile. The API forwards requests such as:

- `/api/v1/tiles/collections/{collection_id}/items/{item_id}/{z}/{x}/{y}.{fmt}` for one scene
- `/api/v1/tiles/collections/{collection_id}/{z}/{x}/{y}.{fmt}` for a whole dataset
- `/api/v1/tiles/mosaic/{searchid}/{z}/{x}/{y}.{fmt}` for a mosaic of a STAC search

Raster and vector requests share one forwarding helper (`forward_tile`), so errors and headers are handled the same way.

## Annotation vector tiles

### Why tiles instead of GeoJSON

Loading a whole annotation set as GeoJSON sends every feature on every request. For a 2,000-polygon set in the same session:

| Path | Bytes | Time (p50) |
|---|---|---|
| GeoJSON, whole set | 870,522 | 729 ms |
| MVT, one zoom 14 screen (15 tiles) | 92,171 | 380 ms |
| MVT, same screen right after an edit | 92,171 | 471 ms |
| MVT, one zoom 16 screen (24 tiles) | 20,061 | 566 ms |

Most of the per-tile time (about 23 ms) is the authentication and organization check; generating a tile adds about 6 ms. The `/features` GeoJSON endpoint still exists for exports and small sets.

### How a request is served

1. `require_org_role("org:viewer")` checks the token and organization.
2. The annotation set is loaded **for that organization**. A set from another organization, or a deleted one, returns 404.
3. Tile coordinates are validated (zoom 0 to 22, `x` and `y` inside the zoom level), otherwise 422.
4. The cache key is built: `tile:{org_id}:{set_id}:{tile_version}:{z}:{x}:{y}`.
5. On a cache miss, the API asks Martin for `annotation_set_mvt/{z}/{x}/{y}?set_id=...&v={tile_version}` and stores the result.
6. The response goes out as `application/x-protobuf` with `Cache-Control: private, no-store`, so browsers and shared proxies never keep a copy.

Martin connects with a role that bypasses row-level security, so it is never exposed on a host port. Step 2 is the only thing standing between a caller and another organization's annotations. See [Multi-tenancy](multi-tenancy.md).

### `tile_version` and cache invalidation

Every annotation set has a `tile_version` (migration 071). PostgreSQL triggers advance it on any insert, update, delete or move of an annotation, from any code path: the API, bulk imports, inference and analysis.

Because the version is part of the cache key, an edit makes all old keys unreachable. Nothing is purged on write and no TTL is needed to decide freshness. The version is also passed to Martin (`v=`), because Martin caches by URL and would otherwise keep serving stale bytes.

!!! note "Concurrency"
    The trigger locks the set row with `FOR NO KEY UPDATE`. The first version used `FOR UPDATE`, which deadlocked two concurrent imports into the same set because each INSERT already holds a KEY SHARE lock through the foreign key. Two concurrency tests cover this.

### Redis tile cache

- Runs as its own Redis instance (`redis-tiles`, set with `TILE_CACHE_REDIS_URL`), so tile bytes can never evict Celery queue or result data.
- If it is empty or down, tiles are still served straight from Martin.
- A repeated tile request went from about 228 ms to 22 ms locally.

### What each tile feature carries

The `annotation_set_mvt` function (migrations 072 and 073) puts all annotation data on each feature as flat values:

`id`, `class_id`, `confidence`, `annotation_set_id`, `dataset_item_id`, `created_by_user_id`, `created_by_job_id`, `created_at`, `updated_at`, `review_status`, `aoi_id`, `aoi_name`, `source`, `source_type`, `verified`, `model_id`, `model_name`, and `aoi_bbox` as a JSON string (tiles cannot hold arrays).

This made tiles larger: about +2 KB at zoom 14 and under +1 KB at zoom 16 on a fully populated set. If anything needs trimming later, `created_at` and `updated_at` are the first candidates.

## Reference layers

Public context layers are global and read-only: every signed-in user, in any organization, can see them.

| Layer | Storage | Notes |
|---|---|---|
| Ramsar wetland sites | PostGIS table `reference.ramsar` | Served live by `reference.ramsar_mvt()`, with a simplified geometry used at zoom 6 and below. 7,458 rows. |
| COFOPRI native communities, RAISG protected areas, RAISG mining, GFW mining concessions, GFW logging concessions, HydroRIVERS, USGS MRDS | PMTiles in the MinIO `reference-tiles` bucket | Built with Tippecanoe (579 MB in total). Martin reads them over S3 with a read-only MinIO user. |

- `GET /api/v1/reference-layers` lists the layers and their tile URLs.
- Only names on an **allowlist** are forwarded to Martin. Anything else, including path tricks, returns 404, so private annotation sources cannot be reached through this route.
- Small layers that change suit PostGIS. Large, static layers suit PMTiles.

### Rebuilding the layers

The data files are not in Git. Scripts in `scripts/reference_layers/` rebuild them:

| Script | Does |
|---|---|
| `load_ramsar.sh` | Loads Ramsar into PostGIS |
| `build_pmtiles.sh` | Builds the seven PMTiles files with Tippecanoe |
| `upload_pmtiles.sh` | Uploads them to the `reference-tiles` bucket |

The README there lists each dataset's source. Licences are in [Data sources and licences](../reference/data-sources.md).

### Adding a layer

1. **Small layer:** load it into a table in the `reference` schema with a GiST index, and add an MVT function for Martin.
2. **Large layer:** build a PMTiles file with Tippecanoe and upload it to `reference-tiles`.
3. Add the layer name to the `REFERENCE_LAYERS` allowlist in `app/api/v1/endpoints/reference_layers.py`.
4. Add the source and licence to the scripts README and to [Data sources and licences](../reference/data-sources.md).
