# Glossary

Terms used in GeoTALOS and these docs, in alphabetical order.

**Acquisition date** (capture date)
: The date an image was taken. GeoTALOS uses it to order imagery in time. See [Capture dates](../user-guide/uploading-imagery.md#capture-dates).

**Annotation**
: A shape on the map with a label, such as a point on a palm crown or a polygon around a water body. See [Annotation sets](../concepts/annotations.md).

**Annotation class**
: One label annotations can have, such as "Palm tree". Classes belong to an annotation schema.

**Annotation schema**
: The list of classes a project uses.

**Annotation set**
: A group of annotations, such as all palm crowns found by one model run on one site.

**Annotation set collection**
: A group of annotation sets, used for example to build a training dataset.

**AOI (area of interest)**
: A study area you draw and save on the map. Searches, model runs and reports can be limited to it. See [Areas of interest](../concepts/aois.md).

**Backbone and head**
: In model training, the backbone is a large pretrained model that turns images into features; the head is a small part trained for your task. GeoTALOS keeps the backbone (DINOv2) fixed and trains only the head. See [Model training pipeline](../developer/training-pipeline.md).

**Band**
: One layer of measurements in an image. A normal photo has red, green and blue bands; multispectral imagery also has bands such as near-infrared.

**Basemap**
: The background map under your imagery, such as streets or satellite.

**Bbox prompt**
: A box you draw around an example object to show a prompt-based model, such as SAM3, what to look for.

**COG (Cloud Optimized GeoTIFF)**
: A GeoTIFF arranged so that only the part on screen needs to be read. GeoTALOS stores imagery as COGs. See [Making files load fast](../user-guide/uploading-imagery.md#making-files-load-fast).

**Confidence**
: How sure a model is about one prediction, from 0 to 1.

**CRS (coordinate reference system)**
: How coordinates map to places on Earth. GeoTALOS stores annotations in WGS 84 (EPSG:4326).

**Dataset**
: A collection of imagery, such as all drone flights over one site. See [Datasets and the data library](../concepts/datasets.md).

**Dataset item**
: One image inside a dataset.

**F1 score**
: A single number combining precision and recall. Higher is better, 1 is perfect.

**GeoJSON**
: A common file format for shapes and their properties. GeoTALOS imports and exports annotations as GeoJSON.

**GeoTIFF**
: An image file that also records where on Earth it belongs.

**Ground truth**
: Annotations checked by an expert and treated as correct, used to measure how well a model did.

**GSD (ground sample distance)**
: The size of one pixel on the ground, for example 5 cm.

**Inference**
: Running a trained model on imagery to get predictions. See [Running models](../user-guide/running-models.md).

**IoU (intersection over union)**
: How much a predicted shape overlaps the true shape, from 0 (no overlap) to 1 (identical).

**Job**
: A long task, such as ingestion or inference, that runs in the background while you keep working.

**MVT (vector tile)**
: Map data cut into tiles that keep shapes and properties instead of pixels. GeoTALOS draws annotations from vector tiles. See [Tiles](../developer/tiles.md).

**NDVI**
: Normalized Difference Vegetation Index, a measure of vegetation greenness from the red and near-infrared bands. See [Temporal analysis](../user-guide/temporal-analysis.md) for NDVI and the other indices.

**Node**
: One step in a workflow, such as Select Data Source or Run Inference.

**Organization**
: Your team's private workspace in GeoTALOS. See [Organizations, projects and roles](../concepts/organizations.md).

**Orthomosaic**
: One large, map-accurate image stitched from many drone photos.

**Patch**
: A small piece of an image sent to a model. Large images are split into patches.

**Pipeline**
: The app's name for a workflow.

**PMTiles**
: A single file holding a whole set of map tiles. Large reference layers are stored this way.

**Precision**
: Of everything the model found, the share that was correct.

**Project**
: A study inside an organization, holding its maps, datasets and workflows.

**Provenance**
: The record of how a result was made: imagery, model, workflow settings and review decisions. See [Provenance](../concepts/provenance.md).

**Recall**
: Of everything that should have been found, the share the model found.

**Reference layer**
: A public map layer, such as Ramsar wetlands, that any organization can switch on for context. See [Reference layers](../user-guide/reference-layers.md).

**Review status**
: Whether an annotation set is Raw, Corrected or Verified. See [Reviewing annotations](../user-guide/reviewing-annotations.md).

**Role**
: What a member may do: viewer, member or admin.

**Row-level security**
: A database rule that only lets each organization see its own rows. See [Multi-tenancy](../developer/multi-tenancy.md).

**SAM3**
: Segment Anything Model 3, a model that outlines objects from a text description or example boxes.

**STAC (SpatioTemporal Asset Catalog)**
: A standard catalogue format for imagery. GeoTALOS registers every uploaded image in a STAC catalogue.

**Temporal Playback**
: Stepping through an AOI's imagery in date order. See [Temporal analysis](../user-guide/temporal-analysis.md).

**Threshold**
: A cut-off value, such as a minimum confidence or index value, below which things are hidden or ignored.

**Tile**
: One small square of a map at one zoom level. Maps load as tiles so only the visible part is fetched.

**Trigger**
: What starts a workflow: a manual click, a schedule or an event. See [Automation](../user-guide/automation.md).

**Verified**
: Checked and confirmed by an expert.

**Webhook**
: A message GeoTALOS sends to another system's web address when a workflow finishes.

**Workflow**
: A saved procedure built from connected nodes. See [Building workflows](../user-guide/building-workflows.md).

**YOLO**
: A family of fast object detection models. GeoTALOS uses YOLO for detections such as palm crowns.
