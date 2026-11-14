# FAQ

## Using GeoTALOS

### I can't see a dataset, map or annotation set that a colleague made.

Check that you have the same **organization** selected. Everything belongs to one organization, and you only see the one you are in. See [Organizations, projects and roles](../concepts/organizations.md).

### A button is missing, or I get "Insufficient permissions".

Your role is too low for that action. Viewers can only look; members can create, edit and run; deleting datasets, maps, models, projects and workflows needs an admin. Ask an admin of your organization to change your role.

### All my images show the same date on the timeline.

GeoTALOS could not find a capture date, so it used the upload time. Put the date in each file name (for example `2024-05-12_site_a.tif`) and upload again. See [Capture dates](../user-guide/uploading-imagery.md#capture-dates).

### My upload says "Upload failed".

The file could not be read as a georeferenced raster. Open it in QGIS: if it does not appear in the right place, it has no location data. Export it as a GeoTIFF with the correct coordinate system and try again.

### My imagery loads slowly when I zoom out.

The file is a plain GeoTIFF, not a Cloud Optimized GeoTIFF. Convert it with `gdal_translate -of COG input.tif output.tif`, or in QGIS with the `COG` format option, and upload it again. See [Making files load fast](../user-guide/uploading-imagery.md#making-files-load-fast).

### NDVI and the other indices are greyed out or look wrong.

They need a near-infrared band. Standard RGB drone cameras do not record one. If your imagery is multispectral, check that the right bands are picked in the index settings. See [Temporal analysis](../user-guide/temporal-analysis.md).

### I switched on a reference layer but see nothing.

Each layer only draws within a zoom range and a region. Zoom in or out, or move to the area it covers. See [Reference layers](../user-guide/reference-layers.md).

### My reference layers were off after I reloaded the page.

That is expected: which reference layers are on is not saved with the map. Switch them on again.

### The model found things that are not there, or missed some.

Model results are drafts. Delete false detections, add missed ones and verify the rest. Raising the minimum score in the layer panel hides the least confident predictions first. See [Reviewing annotations](../user-guide/reviewing-annotations.md).

### A workflow will not start: "Graph validation failed".

A node is missing a connection or a setting. The message says which. Every required input needs a connected line, and every required setting needs a value. See [Building workflows](../user-guide/building-workflows.md).

### My scheduled workflow never runs.

Check that it is **Active**, not Draft or Paused, and that the Trigger node is set to **recurring** with a valid cron expression and the right timezone. See [Automation](../user-guide/automation.md).

### I added Send Email but no email arrives.

Send Email is not built yet. Use **Send Webhook** for notifications.

### Can I upload GeoJSON labels as a dataset?

No. Datasets are for imagery. Import labels into an annotation set as a GeoJSON FeatureCollection instead.

## Running GeoTALOS

### `docker compose up` stops with "GEOOPS_SERVICE_API_TOKEN must be set".

Set `GEOOPS_SERVICE_API_TOKEN` in `.env` to any random string. See [Local setup](../developer/local-setup.md).

### I have no GPU. Can I still run GeoTALOS?

Yes. Only `geoops-service` (model training) wants a GPU, and it falls back to CPU, slowly. Everything else runs on CPU. To test inference without a model server, set `mock_raw_output` on a model. See [Adding a model](../developer/adding-a-model.md).

### Martin keeps restarting with "schema public was not found".

The application database migrations have not run yet. They run automatically through `app-db-migrate` before Martin starts. Check its logs with `docker compose logs app-db-migrate`.

### Migration 074 fails on my existing database.

It creates the `reference` schema and needs permission to do so. Run this once, then migrate again:

```sql
GRANT CREATE ON DATABASE geoplat TO app_user;
```

New databases get this from the init script.

### `alembic heads` shows two heads.

Two migrations share the same parent, usually after merging branches. Renumber yours to follow the current head with a new revision ID. See [Adding a migration](../developer/database.md#adding-a-migration).

### Shell scripts fail with errors like `$'\r': command not found`.

The files were checked out with Windows line endings. The repository's `.gitattributes` forces Unix line endings for shell scripts; re-clone, or run `git add --renormalize .` after pulling it.

### The logs show an error about `annotation_statistics`.

A scheduled task refreshes a materialized view called `annotation_statistics`, but no migration creates it, so the refresh fails every hour. It does not affect the rest of the platform.

### Reference layers are missing from the list.

Their data files are not in Git. Build or download them with the scripts in `scripts/reference_layers/`. See [Tiles, caching and reference layers](../developer/tiles.md).

### I can reach Martin directly on its port.

Martin should not be exposed, because it bypasses row-level security. Keep its `ports:` mapping commented out in `docker-compose.yml`. The API reaches it inside the Docker network. See [Multi-tenancy](../developer/multi-tenancy.md).
