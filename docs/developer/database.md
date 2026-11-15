# Database schema and migrations

GeoTALOS uses two PostgreSQL databases (see [Architecture](architecture.md)):

- **app-db**: PostgreSQL with PostGIS and pgvector. Everything below lives here.
- **stac-db**: pgSTAC, the imagery catalog. It is managed by pgSTAC's own migrations (`stac-db-migrate`), not Alembic.

## Conventions

| Convention | Detail |
|---|---|
| Primary keys | UUID (`id`) |
| Tenancy | Tenant-scoped tables have `organization_id` and row-level security policies. See [Multi-tenancy](multi-tenancy.md). |
| Timestamps | `created_at` and `updated_at`, timezone-aware |
| Soft delete | `deleted_at` on datasets, annotation sets, annotations, maps, models and others. `DELETE` sets it; separate `/purge` endpoints remove rows for good (admin only). |
| Geometry | PostGIS, SRID 4326 (WGS 84 longitude and latitude) |
| Flexible settings | JSONB columns such as `config`, `metadata`, `output_config` |

## Tables by area

| Area | Tables |
|---|---|
| Identity and tenancy | `organizations`, `users`, `organization_members` |
| Projects | `projects`, `project_datasets`, `project_annotation_sets` |
| Imagery | `datasets`, `dataset_items` (one row per scene, linked to a STAC Item) |
| Annotations | `annotation_schemas`, `annotation_classes`, `annotation_sets`, `annotations`, `annotation_set_collections`, `annotation_set_collection_items` |
| Maps | `maps`, `map_layers`, `map_aois`, `map_annotation_sets`, `spatial_bookmarks`, `basemaps`, `styles`, `tile_sources`, `feature_layers` |
| Models and jobs | `ai_models`, `model_class_mappings`, `jobs`, `job_outputs` |
| Workflows | `automation_pipelines`, `automation_runs`, `automation_run_steps` |
| Embeddings and training | `embeddings`, `embedding_tiles`, `dino_datasets`, `dino_tuned_configs` (in the `geoops` package) |
| Audit | `activity_logs` |
| Reference layers | `reference.ramsar` in the separate `reference` schema |

### Key tables

**`annotations`**: `annotation_set_id`, `class_id`, `dataset_item_id`, `geometry` (any geometry type, SRID 4326), `confidence`, `properties` (JSONB), `created_by_user_id` or `created_by_job_id`, timestamps and `deleted_at`.

**`annotation_sets`**: groups annotations. Holds `review_status` (`raw`, `corrected`, `verified`), `tile_version` for tile caching, and an extent kept up to date by a trigger.

**`dataset_items`**: one scene, with its `stac_item_id`, `s3_uri`, `filename` and acquisition date (`item_datetime`).

**`jobs`**: long-running work (ingestion, inference, export, training) with a status and a JSONB `config` that also stores results.

## Database-side logic

Some rules live in the database so that every write path follows them, including bulk SQL from workers:

| Migration | What it adds |
|---|---|
| `019`, `020` | Row-level security policies |
| `042` | `annotation_set_mvt()`, the function Martin turns into vector tiles |
| `047` | Trigger that keeps each annotation set's extent current |
| `049` to `055` | pgvector, embeddings and scan cache tables |
| `071` | Triggers that advance `tile_version` on any annotation change |
| `072`, `073` | Tile attributes for review status and all annotation fields |
| `074` | The `reference` schema and the Ramsar layer |

## Migrations

Migrations are in `alembic/versions/`, named `NNN_<revision>_<description>.py`, and run automatically by the `app-db-migrate` service on `docker compose up`.

To run them by hand:

```bash
docker compose exec api alembic upgrade head
docker compose exec api alembic heads      # must show exactly one head
```

### Adding a migration

1. Pull the latest `main` first. Other branches add migrations too, and two migrations with the same parent create two heads.
2. Create it: `docker compose exec api alembic revision -m "short description"`, then rename the file to the next number.
3. Set `down_revision` to the current head and use a new revision ID. Never reuse an ID from another branch.
4. Write `downgrade()` as well, and test both directions on a fresh database:

    ```bash
    alembic upgrade head && alembic downgrade -1 && alembic upgrade head
    ```

5. Check `alembic heads` shows one head before opening a PR.

!!! warning "Existing databases"
    Migration `074` creates a schema as `app_user`. On a database created before it, run `GRANT CREATE ON DATABASE geoplat TO app_user;` once. New databases get this from the init script.
