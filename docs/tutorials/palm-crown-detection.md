# Palm crown detection

Turn a drone orthomosaic into a reviewed map of palm crowns. This is the simplest complete GeoTALOS workflow: one image, one model, one review.

| | |
|---|---|
| **You will** | Run a palm detection model on an orthomosaic, review the detections and export the result |
| **You need** | A drone orthomosaic of palm forest (GeoTIFF), and a palm detection model registered in your organization |
| **Based on** | The palm crown detection workflow in the GeoTALOS paper (Figure 5) |

In the paper, the image is `FCAT1.tif` from a dataset called "Palm COG Orthomosaics", and the model is a YOLO detector called "Crown Center Detection". Use your own names below.

!!! note "No palm model in the list?"
    Models are set up per organization. Ask your administrator to register one. See [Adding a model](../developer/adding-a-model.md).

## Step 1: Upload the orthomosaic

1. Go to **Datasets** and upload your GeoTIFF as **Imagery**.
2. Name the dataset, for example "Palm COG Orthomosaics".
3. Wait for "Dataset ingested and ready for visualization."

Details: [Uploading imagery](../user-guide/uploading-imagery.md).

## Step 2: Open it on a map

1. In your project, open **Maps** and create a map, for example "Palm Study".
2. Add the dataset from the **Library**.
3. Zoom in until you can see individual crowns.

> **Screenshot:** the orthomosaic on the map, zoomed in to show palm crowns.

## Step 3: Draw an area of interest

Draw a polygon or rectangle around the part of the forest you want to survey. Start small (a few hectares) for your first run, so it finishes quickly.

## Step 4: Run the model

**On the map** (for one image):

1. Select the AOI and open **Run Inference**.
2. Choose your palm model and your dataset.
3. Click **Run on AOI**.

**As a workflow** (to reuse it, as in the paper):

1. In the project's **Automations** tab, create a pipeline.
2. Add and connect three nodes: **Select Data Source** → **Run Inference** → **Overlay on Map**. This is the **Inference on an AOI** recipe.
3. In **Select Data Source**, pick the dataset, the image and the AOI.
4. In **Run Inference**, pick the palm model.
5. In **Overlay on Map**, pick the map ("Palm Study").
6. Save and run.

> **Screenshot:** the three-node workflow from Figure 5 of the paper.

When the run finishes, the detections appear on the map as a new annotation layer of palm crowns.

## Step 5: Review the detections

The detections are drafts, drawn with a dashed outline. Check them:

1. Set **Boxes with a score of at least** to a higher value first, to see the most confident detections.
2. For each detection: **Verify annotation** if it is a palm, **Delete annotation** if it is not.
3. Draw any palms the model missed and save them with **Add Annotation**.
4. When the area is done, set the annotation set's status to **Verified**.

> **Screenshot:** reviewed crowns, verified ones solid, drafts dashed.

Details: [Reviewing annotations](../user-guide/reviewing-annotations.md).

## Step 6: Export the result

On the annotation set's layer, click **Download GeoJSON**. Open the file in QGIS or a field app to plan field visits or count palms by area.

## Next

- [Multi-AOI palm analysis](multi-aoi-palm-analysis.md): run the same model over several areas and get one report
- [Automation](../user-guide/automation.md): run it every time a new orthomosaic arrives
