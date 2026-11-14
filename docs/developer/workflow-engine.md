# The workflow engine

A workflow (called a **pipeline** in the code) is a graph built in the ReactFlow editor and stored as JSON. The engine validates the graph, turns it into a run with one step per node, and executes the steps on Celery as their inputs become ready.

Code: `app/automation/` (engine, registry, nodes, adapters) and `app/workers/automation/` (Celery tasks, scheduler).

## Node types

Each node type is registered with the `@node(...)` decorator and declares:

| Field | Meaning |
|---|---|
| `type`, `label`, `category` | Identity and where it appears in the editor |
| `inputs`, `outputs` | Typed handles, for example `dataset_items`, `annotation_set`, `model` |
| `config_schema` | The settings the user fills in |
| `executor` | The function that does the work |
| `status` | `implemented` or `placeholder` |

`GET /api/v1/automation/node-catalog` returns every node type grouped by category, which is what the editor shows.

### Catalog

There are 52 node types. Those marked *(placeholder)* appear in the catalog but are not implemented yet.

| Category | Nodes |
|---|---|
| Triggers | Trigger, On Dataset Ingested, On Annotation Created, On Threshold Breach |
| Data source | Select Data Source, Select Annotation Set, STAC Search, AOI Filter, Search Map AOI Resources, Load Saved AOI Timeline |
| ML annotation | Run Inference, Cascading Models *(placeholder)*, Active Learning Selector *(placeholder)* |
| Map overlay | Overlay on Map, Overlay Dataset on Map, Export Annotations, Export Dataset Items, Before/After Comparison *(placeholder)* |
| Analysis | Area Calculation, Timeseries Analysis, Aggregate Model Runs, Zonal Statistics, Anomaly Detection, Change Detection, Object State Tracking |
| Data operations | Filter Annotations, Merge Annotation Sets, Vectorize Raster Mask, Rasterize Annotation Set, Review Queue *(placeholder)*, Status Transition *(placeholder)* |
| Quality (IoU) | Ground Truth Comparison, Multi-Model IoU Comparison, IoU Threshold Gate, Spatial Rule Checker, Duplicate Detection, Raster Mask Metrics, Inter-Annotator Agreement *(placeholder)*, Consensus Builder *(placeholder)*, Confusion Matrix *(placeholder)*, Annotator Scoring *(placeholder)* |
| Output | Send Webhook, Generate Report, Send Email *(placeholder)*, In-App Notification *(placeholder)* |
| Advanced | Multi-Sensor Fusion, Cloud Masking, Temporal Compositing, Compliance Check, Self-Improving Alert, Domain Adaptation, Hypothesis Test *(all placeholders)* |

## Validation

`validate_graph` runs before every run, and on demand through `POST /api/v1/automation/pipelines/{id}/validate`. It checks that:

1. every node type exists in the registry,
2. every edge connects real handles on its source and target nodes,
3. handle types match across each edge,
4. every required input has an incoming edge,
5. the graph has no cycles (Kahn's algorithm, which also gives the execution order), and
6. required config fields are set.

A graph that fails any check never starts, so no imagery is read and no model is run.

## How a run executes

1. `create_run` makes an `AutomationRun` and one `AutomationRunStep` per node, all `pending`.
2. Root nodes (no incoming edges) are dispatched to Celery as `execute_step` on the `automation` queue.
3. When a step completes, its outputs are stored and each downstream node whose inputs are all complete is dispatched (`resolve_step_inputs` gathers them from the upstream steps).
4. The run finishes when every step is done, or fails when a step fails.

### Long-running steps

Inference, exports and similar work can take minutes. Instead of blocking a worker, the executor starts a Job and returns `DeferToJob(job_id)`. The step becomes `waiting_for_job`. When the job finishes, `resume_after_job` marks the step complete and dispatches the next nodes. The user sees progress in the run panel throughout.

### Statuses

| Object | Statuses |
|---|---|
| Pipeline | `draft`, `active`, `paused`, `archived` |
| Run | `pending`, `running`, `completed`, `failed`, `cancelled` |
| Step | `pending`, `running`, `completed`, `failed`, `skipped`, `waiting_for_job` |

## Triggers

Every pipeline has a `trigger_type`:

| Trigger | How it starts |
|---|---|
| `manual` | `POST /api/v1/automation/pipelines/{id}/run` |
| `schedule` | A cron expression. Activating the pipeline adds a Celery Beat entry (`automation-pipeline-{id}`); pausing, archiving or deleting it removes the entry. |
| `event` | `dispatch_event` finds the organization's active pipelines whose trigger matches an application event, such as a dataset being ingested or an annotation being created, and starts a run for each. |

## Model output adapters

Models return different formats. Adapters in `app/automation/adapters/` turn each format into GeoTALOS annotations with geometry, label, confidence and provenance:

| Adapter | Input format |
|---|---|
| `yolo_adapter` | YOLO detections (boxes) |
| `sam3_adapter` | SAM3 masks |
| `crown_adapter` | Crown centre detections |
| `coco_adapter` | COCO-style annotations |
| `geojson_adapter` | GeoJSON features |
| `platform_adapter` | GeoTALOS' own format |

`geo_utils` georeferences pixel coordinates using the image metadata. See [Adding a model](adding-a-model.md).

## API summary

| Method and path | Purpose |
|---|---|
| `GET /node-catalog` | Node types by category |
| `GET`, `POST /pipelines` | List or create pipelines |
| `GET`, `PATCH`, `DELETE /pipelines/{id}` | Read, update or delete (delete needs admin) |
| `POST /pipelines/{id}/validate` | Validate the graph |
| `POST /pipelines/{id}/duplicate` | Copy a pipeline |
| `POST /pipelines/{id}/run` | Start a run |
| `GET /pipelines/{id}/runs` | Run history |
| `GET /runs/{run_id}`, `/runs/{run_id}/steps` | Run and step detail |
| `GET /runs/{run_id}/steps/{step_id}/download` | Download a step's output file |
| `POST /runs/{run_id}/cancel`, `/runs/{run_id}/retry` | Cancel or retry |

All paths are under `/api/v1/automation`.

## Adding a node type

1. Write an executor in the right module under `app/automation/nodes/`.
2. Decorate it with `@node(type=..., category=..., label=..., inputs=[...], outputs=[...], config_schema={...})`, using existing handle types so it connects to other nodes.
3. For long work, start a Job and return `DeferToJob(job_id)` instead of blocking.
4. Add tests, then check it appears in `/node-catalog` and validates in the editor.
