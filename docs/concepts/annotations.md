# Annotation sets

An **annotation** is a shape on the map with a label, such as a point on a palm crown or a polygon around a water body. Annotations are grouped into **annotation sets**, for example "Palm crowns, field site A, 2025".

## Where annotations come from

- **Model predictions.** When a model runs, GeoTALOS turns its output (boxes, masks or points) into annotations placed at the right location on the map.
- **Drawing by hand.** You can draw and label annotations yourself with the drawing tools.
- **Importing.** You can bring in existing annotations, for example from GeoJSON.

Each annotation keeps its label, its confidence score (for model predictions), who or what created it, and when.

## From prediction to evidence

Model output is a starting point, not a final answer. GeoTALOS treats predictions as **draft** annotations that an expert checks. While reviewing you can confirm correct predictions, remove false ones, change labels and reshape outlines.

Each annotation set has a review status:

| Status | Meaning |
|---|---|
| **Raw** | Straight from a model or import, not yet checked. |
| **Corrected** | Someone has started fixing it: removing, relabelling or reshaping annotations. |
| **Verified** | Checked by an expert and ready to use as evidence. |

Reviewed annotations can then be used for area calculations, change detection, reports and export. See [Reviewing annotations](../user-guide/reviewing-annotations.md).
