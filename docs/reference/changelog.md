# Changelog

Notable changes to GeoTALOS and these docs, newest first. Pull request numbers refer to [GeoTalosProd](https://github.com/spygaurad/GeoTalosProd) (backend) and [GeoTalosUI](https://github.com/spygaurad/GeoTalosUI) (frontend).

## November 2026

**Documentation**

- This documentation site, with Key Concepts, a User Guide for ecologists, a Developer Guide, Tutorials and Reference.

**Annotation vector tiles and reference layers** (backend #39, UI #5)

- Annotation sets draw from vector tiles for the visible area instead of loading the whole set, behind an authenticated endpoint that checks the organization.
- `tile_version` and a separate Redis tile cache keep tiles fresh after edits without purging.
- Tiles carry every annotation field as flat values.
- Eight public reference layers: Ramsar in PostGIS, seven larger layers as PMTiles in object storage, with a **Reference layers** toggle on the map.
- Annotation input is now validated: invalid geometry and confidence outside 0 to 1 return a clear error instead of being stored or failing.

## October 2026

- **Model training pipeline**: build datasets from reviewed annotations, train DINOv2 heads and YOLO models on a GPU service, read reports and export to ONNX.
- **Embeddings**: similarity search, AOI scans and anomaly detection (migrations 049 to 070).
- **Interactive mode** and **Train Head** panels on the map, and an AOI data picker.

## August 2026

- **Fresh-clone startup fixes** (backend #32): a migration permission fix and Unix line endings for shell scripts, so the stack starts from a fresh clone on any platform.

## June 2026

- The platform is renamed **GeoTALOS** (backend #29).
- **Annotations on the map** (UI #3).
- Project README and documentation pages (backend #28, #30, #31).

## May 2026

- **AOI-based inference**: clip imagery to an AOI before running a model (backend #21).
- **Workflow automation**: the visual pipeline engine and its nodes (backend #22).
- **Saved AOIs** on maps, and STAC-wide AOI search with prompt support for models such as SAM3 (backend #23, #24).
- Duplicating pipelines across maps (backend #25).
- **Annotation set collections** and deleting annotations (backend #26).
- **Multi-model comparison** nodes (backend #27).

## March 2026

- First release: database schema, Clerk sign-in, core API, row-level security by organization, pagination and soft delete (backend #2 to #13).
- Background jobs, the STAC imagery catalog, PostgreSQL 17 and Martin (backend #8, #9, #14).
- **Dataset upload** (backend #16).
- Annotation sets on map layers; annotation, style and schema endpoints (backend #17, #18).
- **Map layout** and map enhancements (UI #1, #2).
