# Model training pipeline

!!! note "Draft"
    This page is written from the code (`geoops/` and `geoops-service/`). Suraj Prasai will confirm the workflow and add details.

GeoTALOS can train new models from the annotations your team has reviewed. Training keeps a pretrained **backbone** (DINOv2) fixed and trains a small **head** for the task, so each new class only needs its own head, not a new full model.

## Parts

| Part | Where | Does |
|---|---|---|
| Train Head panel | GeoTalosUI | Lets a user pick reviewed annotations, build a training dataset and start a run |
| `geoops` package | GeoTalosProd (`geoops/`) | API under `/api/v1/dino`, dataset export, Celery tasks on the `training` queue |
| `geoops-service` | Separate container, port 8020 | GPU service that trains, evaluates and exports models |

`geoops-service` has its own image so PyTorch and Transformers stay out of the API and worker images. It needs an NVIDIA GPU with the NVIDIA Container Toolkit and falls back to CPU (slowly) if none is visible. Every route except `/health` needs the bearer token set in `GEOOPS_SERVICE_API_TOKEN`.

## Backbones and model kinds

| Backbone key | Model | Feature size |
|---|---|---|
| `dinov2-vits14` (default) | `facebook/dinov2-small` | 384 |
| `dinov2-vitb14` | `facebook/dinov2-base` | 768 |

| Kind | Trains |
|---|---|
| `fcos` (default) | An object detection head on the DINOv2 backbone |
| `classify` | A classification head on the same tiles |
| `segment` | A segmentation head |
| `yolo` | A YOLO model fine-tuned from pretrained weights (Ultralytics), in two stages |

## Workflow

1. **Build a dataset.** `POST /api/v1/dino/datasets` exports tiles and labels from an annotation set collection, for one or more classes and AOIs. This runs as a background job. Training never builds a dataset implicitly.
2. **Check it.** `GET /api/v1/dino/datasets/{id}/items` lists the exported tiles so you can check them. `POST /api/v1/dino/datasets/{id}/rebuild` rebuilds it after fixing annotations. A `classify` dataset can be derived from an existing detection dataset so both share the same tiles.
3. **Train.** `POST /api/v1/dino/finetune` starts a job. The `run_dino_train` Celery task calls `geoops-service` `POST /train`, which trains, evaluates on the test split and stores the weights in object storage.
4. **Read the report.** `GET /api/v1/dino/runs/{job_id}/report` returns loss curves, metrics and timings. `GET /api/v1/dino/runs` lists earlier runs for a class.
5. **Use or export the model.** The trained head is registered as a model linked to its backbone (`ai_models.backbone_model_id`), so it can run in inference and workflows. `POST /api/v1/dino/runs/{job_id}/model/onnx` exports it as ONNX.

## Tuning

A training request can ask for:

- **Hyperparameter tuning** with Optuna (`tune_trials`), which tries different settings and keeps the best by test-split evaluation.
- **Several seeds** (`seeds`), to check that a result is stable and not a lucky run.
- **Early stopping** (`patience`, `min_epochs`) for the DINOv2 heads.

Tuned settings are saved per dataset (`GET /api/v1/dino/datasets/{id}/tuned-config`) and reused on later runs.

## Other `geoops-service` routes

| Route | Purpose |
|---|---|
| `GET /backbones`, `GET /yolo/bases` | Available backbones and pretrained YOLO weights |
| `POST /infer`, `POST /eval` | Run or evaluate a trained head |
| `POST /embed`, `POST /embed/batch` | Image embeddings, used by similarity search and anomaly detection |
| `POST /sam3/boxes-masks`, `/sam3/point`, `/sam3/segment-tile` | SAM3 segmentation from boxes, points or a tile |
| `POST /autoannotate` | Automatic annotation of a tile |
| `POST /export-onnx` | ONNX export |

## Related

- [Adding a model](adding-a-model.md): registering external models
- [Annotation sets](../concepts/annotations.md): why reviewed annotations make better training data
