# Adding a model

GeoTALOS does not bundle models. A model is an HTTP endpoint you register, plus an **adapter** that turns its output into GeoTALOS annotations. Adding a model of a supported format is configuration only; no backend code changes.

## How inference works

`ModelManager.run_job` (`app/services/model_manager.py`) is the single code path for every model:

```text
for each dataset item in the job:
    split the image (or the AOI inside it) into patches
    for each patch:
        fetch the patch as PNG from TiTiler
        POST it to the model's endpoint_url
        the adapter converts the response to the platform format
    merge duplicate detections across neighbouring patches (per class)
    keep predictions whose class is mapped and above the threshold
    write them as annotations into a new annotation set
```

The job runs on the `inference` queue, so the map stays responsive.

## 1. Expose an endpoint

The model must accept a JSON `POST` (the method can be changed) with this body:

| Field | Content |
|---|---|
| `patch_image_base64`, `patch_image_format` | The patch as a base64 PNG |
| `patch` | The patch's bounding box and pixel size |
| `georef_metadata` | Georeferencing details of the source image |
| `dataset_item_id`, `stac_item_id`, `s3_uri`, `filename` | Which image the patch came from |
| `prompt_payload` | Prompts for promptable models such as SAM3, otherwise `{}` |

It returns JSON in any format an adapter understands (see below).

## 2. Register it

`POST /api/v1/models` creates a row in `ai_models`. The important fields:

| Field | Purpose |
|---|---|
| `name`, `version`, `framework`, `type`, `description` | Shown in the model picker |
| `endpoint_url` | Where patches are sent |
| `request_config` | `method` (default `POST`), `timeout_seconds` (default 60), and an optional `payload` merged into every request body |
| `auth_config` | `bearer_token`, sent as `Authorization: Bearer ...` |
| `output_config` | Which adapter to use and how to cut patches (below) |
| `annotation_schema_id` | The annotation classes this model's labels map to |

### `output_config`

| Key | Meaning |
|---|---|
| `adapter` | Adapter name, for example `yolo_to_platform`. Default `platform_passthrough`. |
| `adapter_config` | Settings for that adapter, such as `category_map` and `min_score` |
| `patch_size_px` | Patch size in pixels |
| `patch_size_m` | Patch size in metres, converted to pixels per image. Better for models trained at a fixed ground resolution. |
| `patch_sizes_m` | Several sizes, to scan each image at more than one scale |
| `max_patches_per_item` | Upper limit on patches per image |
| `mock_raw_output` | A fixed response used instead of calling the endpoint, useful for testing without a GPU |

!!! tip "Testing without a model server"
    Set `output_config.mock_raw_output` to a sample response. Inference then runs end to end (patches, adapter, annotations) without contacting any endpoint.

## 3. Map labels to classes

Model labels become annotation classes in one of two ways:

1. **Explicit mappings** in `model_class_mappings` (label, class, confidence threshold). These win when present.
2. Otherwise, `adapter_config.category_map` values are matched by name against the classes of the model's annotation schema, with `adapter_config.min_score` as the threshold.

Predictions whose label is not mapped are dropped.

## Adapters

All adapters produce the same platform format:

```json
{
  "format_version": "1.0",
  "predictions": [
    {"label": "palm", "confidence": 0.91, "geometry": {...}, "properties": {...}}
  ],
  "metadata": {"adapter_used": "yolo_to_platform"}
}
```

| Name | Accepts |
|---|---|
| `platform_passthrough` | Responses already in the platform format |
| `geojson_to_platform` | A GeoJSON FeatureCollection (`label_field`, `score_field` configurable) |
| `yolo_to_platform` | YOLO `[class, cx, cy, w, h, conf]` detections |
| `coco_to_platform` | COCO-style annotations |
| `crown_to_platform` | Tree crown centre detections |
| `sam3_to_platform` | SAM3 masks, including text and box prompts |

`GET /api/v1/inference/adapters` lists them with their config schemas, which the admin UI uses.

### Writing a new adapter

Only needed for an output format none of the above handles.

1. Create `app/automation/adapters/<name>_adapter.py` with `convert(raw, config, context) -> dict` returning the platform format. Use `geo_utils` to turn pixel coordinates into map coordinates.
2. Register an `OutputAdapter` in `ADAPTER_REGISTRY` (`app/automation/adapters/__init__.py`) with a name, label, `supported_formats` and a JSON `config_schema`.
3. Optional hooks:
    - `request_enricher` adds model-specific fields to the request body.
    - `prompt_resolver` turns a static prompt into a per-patch prompt, for example clipping a box drawn on the map into that patch's pixels. Returning `None` skips the patch.
4. Add tests with a recorded model response.

## Using the model

Once registered, the model appears in the **Run Inference** node of the workflow editor and in map inference. Deleting a model needs the admin role.

For training your own heads on GeoTALOS annotations, see [Model training pipeline](training-pipeline.md).
