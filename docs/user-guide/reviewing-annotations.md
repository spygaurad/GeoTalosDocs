# Reviewing annotations

Model predictions are drafts. Before you use them for counts, maps or reports, an expert checks them: keeps the right ones, removes the wrong ones and adds what the model missed. This page shows how.

## Drafts and verified annotations look different

On the map:

- **Draft** annotations (from a model, not yet checked) have a dashed, lighter outline.
- **Verified** annotations have a solid, thicker outline and a fuller fill.

Colours always follow the class, so a verified palm and a draft palm share a colour but not a line style.

> **Screenshot:** draft and verified palm crowns side by side.

## Review one annotation at a time

Click an annotation on the map. Its details appear in the panel: **Class**, **Schema**, **Confidence** and where it came from. A small popup offers two actions:

| Action | Use it when | What happens |
|---|---|---|
| **Verify annotation** | The prediction is correct | It moves into the verified set for this layer and switches to the solid style. |
| **Delete annotation** | The prediction is wrong (a false detection) | Click once, then click again to confirm. It is removed from the set. |

A verified annotation cannot be verified again. To undo a verification, delete it from the verified set.

## Add what the model missed

1. Open the annotation drawing tools and choose a shape (point, polygon, rectangle and so on).
2. Draw the missing object on the map. The panel shows **Geometry ready to save**.
3. Pick the annotation class.
4. Click **Add Annotation**.

To fix a wrong outline, delete the annotation and draw it again.

## Make large sets easier to review

In the annotation set's layer panel:

- **Boxes with a score of at least**: hide predictions below a confidence score, so you start with the ones the model is surest about.
- **Classes shown**: show only the classes you are reviewing now.
- **View**: show masks, bounding boxes or both.
- **Layer opacity**: see the imagery under the annotations.

## Mark the whole set

Each annotation set has a review status, shown on its layer card and in the Library:

| Status | Shown as | Meaning |
|---|---|---|
| **Raw** | Raw | Straight from a model or import, not checked |
| **Corrected** | ML annotated · human corrected | Someone has fixed parts of it |
| **Verified** | Human verified | Fully checked and ready to use as evidence |

Change the status from the set's layer card when your review reaches that stage. In the **Library** you can filter annotation sets by **Verified**, **Corrected** or **Raw**.

## Export the reviewed result

Use **Download GeoJSON** on the annotation set to take the result into QGIS, ArcGIS or a field app.

## Import existing labels

If you already have labels from another tool, import them into an annotation set as a GeoJSON FeatureCollection. You can then review and verify them like model output.

## Why review matters

Verified annotations are the input for:

- reliable counts, areas and reports,
- comparing a model against ground truth ([Multi-prompt segmentation](../tutorials/multi-prompt-segmentation.md) shows how),
- training better models for your own classes ([Model training pipeline](../developer/training-pipeline.md)).

GeoTALOS records who verified or changed each annotation and when. See [Provenance](../concepts/provenance.md).
