# API endpoints

The backend is a FastAPI application. Every route below is under **`/api/v1`**.

## Interactive reference

FastAPI generates the full, always-current reference from the code:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

Use these for request and response schemas. This page explains how the API is organised and the conventions every route follows.

## Calling the API

Send the Clerk session token as a bearer token:

```bash
curl -H "Authorization: Bearer $CLERK_TOKEN" \
     http://localhost:8000/api/v1/datasets?limit=20
```

The token must carry an active organization. Requests without one get `403 Organization context required`; requests below the route's minimum role get `403 Insufficient permissions`. See [Multi-tenancy](multi-tenancy.md).

## Conventions

| Topic | Rule |
|---|---|
| Paging | `limit` (default 20, max 100) and `offset` (default 0) on list routes |
| Not found | Missing resources and resources from another organization both return `404`, so IDs from other organizations cannot be probed |
| Validation | Invalid input returns `400` or `422` with a reason, for example an invalid geometry or a confidence outside 0 to 1 |
| Deleting | `DELETE` soft-deletes; `/purge` routes remove data for good. Deleting datasets, annotation sets, maps, models, projects and workflows needs the admin role; members can delete single annotations. |
| Long work | Returns `202 Accepted` with a job. Poll the job or listen on the event stream. |

## Route groups

### Data

| Prefix | Purpose |
|---|---|
| `/datasets` | Datasets, their items, multipart uploads, tile config, raster values |
| `/stac` | STAC search and items |
| `/storage/download-url` | Short-lived download links for stored files |
| `/projects` | Projects and the datasets and annotation sets in them |

### Annotations

| Prefix | Purpose |
|---|---|
| `/annotation-schemas`, `/annotation-classes` | Class lists that annotations and models use |
| `/annotation-sets` | Annotation sets, review status, GeoJSON features, vector tiles, purge |
| `/annotation-sets/{set_id}/annotations` | Create, update and delete annotations in a set |
| `/maps/{map_id}/annotations` | Create annotations directly on a map |
| `/annotation-set-collections` | Groups of annotation sets, used for training datasets |

### Maps

| Prefix | Purpose |
|---|---|
| `/maps` | Maps |
| `/maps/{map_id}/layers` | Layers on a map |
| `/maps/{map_id}/aois` | Saved areas of interest, AOI resource search and timelines |
| `/basemaps`, `/styles`, `/tile-sources`, `/feature-layers` | Map building blocks |
| `/reference-layers` | Public reference layers and their tiles |
| `/tiles` | Raster tiles from TiTiler |

### Models, jobs and workflows

| Prefix | Purpose |
|---|---|
| `/models` | Registered models. See [Adding a model](adding-a-model.md). |
| `/inference/adapters` | Output adapters and their settings |
| `/jobs` | Start inference (`POST /jobs/inference`), read a job, retry it |
| `/automation` | Workflows, runs and steps. See [The workflow engine](workflow-engine.md). |
| `/embeddings` | Embedding bank, similarity search, AOI scan, anomaly scan |
| `/dino` | Training datasets, training runs, reports, ONNX export. See [Model training pipeline](training-pipeline.md). |
| `/sam3` | SAM3 segmentation helpers |
| `/yolo` | YOLO base weights |

### Organization and system

| Prefix | Purpose |
|---|---|
| `/organizations`, `/organization-members` | Organization settings and membership (changes need admin) |
| `/users` | Users |
| `/auth/sync` | Syncs the signed-in user and organization from Clerk |
| `/webhooks/clerk` | Receives Clerk events (signed with `CLERK_WEBHOOK_SECRET`) |
| `/events` | Live event stream (below) |
| `/health` | Health check |

## Jobs

Long operations (ingestion, inference, export, training) create a job and return `202` straight away:

1. Read the job with `GET /api/v1/jobs/{job_id}` until its status is `completed` or `failed`.
2. Results are in the job's `config.result`, or as a `job_outputs` row (for example, the new annotation set).
3. `POST /api/v1/jobs/{job_id}/retry` runs a failed job again.

## Live events

`GET /api/v1/events` is a Server-Sent Events stream for the caller's organization, so the UI can update without polling.

- Filter with `topics`, a comma-separated list of prefixes such as `automation,job`.
- After a dropped connection, send the `Last-Event-ID` header to replay what was missed.
- Events include `job.completed` and `job.failed`, and workflow run progress.

```bash
curl -N -H "Authorization: Bearer $CLERK_TOKEN" \
     "http://localhost:8000/api/v1/events?topics=job,automation"
```
